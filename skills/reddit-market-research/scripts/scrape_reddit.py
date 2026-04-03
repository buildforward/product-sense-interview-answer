#!/usr/bin/env python3
"""
Reddit Market Research Scraper
Scrapes top posts and full comment trees from subreddits.
Supports subreddit discovery by topic, auto-adjusting timeframes,
pagination beyond 100 posts, and recursive comment extraction.
"""

import json
import time
import urllib.request
import urllib.parse
import sys
import os
import argparse
from datetime import datetime

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
REQUEST_DELAY = 3  # seconds between requests — be polite to Reddit

# Reddit occasionally blocks one domain but not another.
# We try www first, then fall back to old.reddit.com.
BASE_DOMAINS = ["https://www.reddit.com", "https://old.reddit.com"]


def make_request(url, max_retries=3):
    """Make a rate-limited request to Reddit's JSON API.
    Automatically retries with alternate domains on 403."""
    # Build list of URLs to try (original + alternate domains)
    urls_to_try = [url]
    for domain in BASE_DOMAINS:
        for other_domain in BASE_DOMAINS:
            if domain != other_domain and url.startswith(domain):
                alt = url.replace(domain, other_domain, 1)
                if alt not in urls_to_try:
                    urls_to_try.append(alt)

    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

    for try_url in urls_to_try:
        for attempt in range(max_retries):
            try:
                time.sleep(REQUEST_DELAY)
                req = urllib.request.Request(try_url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = 60 * (attempt + 1)
                    print(f"  [rate-limited] waiting {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                elif e.code == 403:
                    print(f"  [403] {try_url} — trying next domain...", file=sys.stderr)
                    break  # skip to next domain
                else:
                    print(f"  [HTTP {e.code}] {try_url}", file=sys.stderr)
                    if attempt < max_retries - 1:
                        time.sleep(5)
            except Exception as e:
                print(f"  [error] {e}", file=sys.stderr)
                if attempt < max_retries - 1:
                    time.sleep(5)
    return None


# ---------------------------------------------------------------------------
# Subreddit discovery
# ---------------------------------------------------------------------------

def search_subreddits(query, limit=10):
    """Search Reddit for subreddits matching a query string."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.reddit.com/subreddits/search.json?q={encoded}&limit={limit}"
    data = make_request(url)
    if not data:
        return []

    results = []
    for child in data.get("data", {}).get("children", []):
        sub = child["data"]
        results.append({
            "name": sub["display_name"],
            "subscribers": sub.get("subscribers", 0),
            "description": sub.get("public_description", "")[:200],
            "active_users": sub.get("accounts_active", 0),
        })

    results.sort(key=lambda x: x["subscribers"], reverse=True)
    return results


def try_direct_subreddit(name):
    """Try to access a subreddit directly by name (bypass search)."""
    info = get_subreddit_info(name)
    if info and info["subscribers"] > 0:
        return {
            "name": info["name"],
            "subscribers": info["subscribers"],
            "description": info.get("description", "")[:200],
            "active_users": info.get("active_users", 0),
        }
    return None


def expand_topic_keywords(topic):
    """Generate search variations from a broad topic string."""
    words = topic.lower().split()
    queries = [topic]  # original query first

    # Add individual significant words (skip very short ones)
    for w in words:
        if len(w) > 3 and w not in queries:
            queries.append(w)

    # Common suffixes that create subreddit names
    for suffix in ["", "advice", "help", "tips", "community", "support"]:
        candidate = topic.replace(" ", "") + suffix
        if candidate not in queries:
            queries.append(candidate)

    return queries


def _relevance_score(sub_name, sub_desc, topic):
    """Score how relevant a subreddit is to the search topic (0-100)."""
    name_lower = sub_name.lower()
    topic_lower = topic.lower()
    topic_words = set(topic_lower.split())
    desc_lower = (sub_desc or "").lower()

    score = 0

    # Direct name match is strongest signal
    if topic_lower.replace(" ", "") == name_lower:
        score += 50
    elif topic_lower.replace(" ", "") in name_lower:
        score += 35
    elif any(w in name_lower for w in topic_words if len(w) > 3):
        score += 20

    # Description relevance
    for w in topic_words:
        if len(w) > 3 and w in desc_lower:
            score += 5

    return score


def discover_subreddits(topic, max_results=5):
    """Find the best subreddits for a broad topic using keyword expansion
    and relevance filtering to avoid returning generic mega-subs."""
    all_subs = {}

    # Strategy 1: Try direct subreddit name lookups (most precise)
    direct_names = [
        topic.replace(" ", ""),
        topic.replace(" ", "_"),
        topic.replace(" ", ""),  # e.g. "remote work" -> "remotework"
    ]
    # Also try each word as a subreddit name
    for w in topic.split():
        if len(w) > 3:
            direct_names.append(w)

    print(f"Trying direct subreddit lookups...")
    for name in direct_names[:5]:
        print(f"  Trying: r/{name}")
        sub = try_direct_subreddit(name)
        if sub:
            key = sub["name"].lower()
            if key not in all_subs or sub["subscribers"] > all_subs[key]["subscribers"]:
                all_subs[key] = sub
                print(f"    Found: r/{sub['name']} ({sub['subscribers']:,} subscribers)")

    # Strategy 2: Search API with keyword expansion
    queries = expand_topic_keywords(topic)
    print(f"Searching with {len(queries)} keyword variations...")
    for q in queries[:5]:
        print(f"  Searching: '{q}'")
        results = search_subreddits(q)
        for r in results:
            key = r["name"].lower()
            if key not in all_subs or r["subscribers"] > all_subs[key]["subscribers"]:
                all_subs[key] = r

    # Strategy 3: Filter by relevance to remove generic mega-subs
    scored = []
    for sub in all_subs.values():
        rel = _relevance_score(sub["name"], sub.get("description", ""), topic)
        scored.append((rel, sub))

    # Sort by relevance first, then by subscribers within similar relevance
    scored.sort(key=lambda x: (x[0], x[1]["subscribers"]), reverse=True)

    # Filter: only keep subs with some relevance (score > 0)
    # Exception: if nothing has relevance, fall back to top by subscribers
    relevant = [(r, s) for r, s in scored if r > 0]
    if not relevant:
        relevant = scored

    ranked = [s for _, s in relevant[:max_results]]

    if ranked:
        print(f"\nTop {len(ranked)} relevant subreddits:")
        for s in ranked:
            rel = _relevance_score(s["name"], s.get("description", ""), topic)
            print(f"  r/{s['name']}  ({s['subscribers']:,} subs, relevance={rel})")

    return ranked


# ---------------------------------------------------------------------------
# Subreddit metadata
# ---------------------------------------------------------------------------

def get_subreddit_info(subreddit):
    """Fetch metadata for a subreddit (subscriber count, etc.)."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    data = make_request(url)
    if not data:
        return None

    sub = data.get("data", {})
    return {
        "name": sub.get("display_name", subreddit),
        "subscribers": sub.get("subscribers", 0),
        "active_users": sub.get("accounts_active", 0),
        "description": sub.get("public_description", ""),
    }


def auto_time_filter(subscribers):
    """Pick a time window that should yield ~100 posts given subreddit size."""
    if subscribers > 2_000_000:
        return "week"
    elif subscribers > 500_000:
        return "month"
    elif subscribers > 100_000:
        return "month"
    elif subscribers > 20_000:
        return "year"
    else:
        return "all"


# ---------------------------------------------------------------------------
# Post scraping (with pagination)
# ---------------------------------------------------------------------------

def get_top_posts(subreddit, time_filter="month", target=100):
    """Fetch up to `target` top posts, paginating as needed."""
    posts = []
    after = None

    while len(posts) < target:
        batch = min(100, target - len(posts))
        url = (
            f"https://www.reddit.com/r/{subreddit}/top.json"
            f"?t={time_filter}&limit={batch}&raw_json=1"
        )
        if after:
            url += f"&after={after}"

        data = make_request(url)
        if not data:
            break

        children = data.get("data", {}).get("children", [])
        if not children:
            break

        for child in children:
            p = child["data"]
            posts.append({
                "id": p["id"],
                "title": p.get("title", ""),
                "author": p.get("author", "[deleted]"),
                "score": p.get("score", 0),
                "num_comments": p.get("num_comments", 0),
                "selftext": p.get("selftext", ""),
                "permalink": f"https://www.reddit.com{p.get('permalink', '')}",
                "created_utc": p.get("created_utc", 0),
                "link_flair_text": p.get("link_flair_text", ""),
            })

        after = data.get("data", {}).get("after")
        if not after:
            break

        print(f"  ... {len(posts)} posts fetched", file=sys.stderr)

    return posts[:target]


# ---------------------------------------------------------------------------
# Comment scraping (recursive tree extraction)
# ---------------------------------------------------------------------------

def extract_comments(node, depth=0):
    """Recursively extract comments from Reddit's nested JSON."""
    comments = []

    if isinstance(node, dict):
        kind = node.get("kind", "")
        data = node.get("data", {})

        if kind == "more":
            return comments  # skip collapsed "load more" stubs

        if data.get("body"):
            comments.append({
                "author": data.get("author", "[deleted]"),
                "score": data.get("score", 0),
                "body": data.get("body", ""),
                "depth": depth,
                "id": data.get("id", ""),
            })

        # Recurse into replies
        replies = data.get("replies", "")
        if isinstance(replies, dict):
            for child in replies.get("data", {}).get("children", []):
                comments.extend(extract_comments(child, depth + 1))

        # Recurse into children (listing objects)
        for child in data.get("children", []):
            if isinstance(child, dict):
                comments.extend(extract_comments(child, depth))

    elif isinstance(node, list):
        for item in node:
            comments.extend(extract_comments(item, depth))

    return comments


def get_post_comments(post_id, subreddit):
    """Fetch the full comment tree for a single post."""
    url = (
        f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
        f"?limit=500&depth=10&sort=top&raw_json=1"
    )
    data = make_request(url)
    if not data or not isinstance(data, list) or len(data) < 2:
        return []

    comments = []
    listing = data[1]
    for child in listing.get("data", {}).get("children", []):
        comments.extend(extract_comments(child))

    return comments


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def scrape_subreddit(subreddit, num_posts=100, time_filter=None, output_dir="."):
    """Scrape a single subreddit: posts + all comment trees."""

    info = get_subreddit_info(subreddit)
    if not info:
        print(f"Could not access r/{subreddit}", file=sys.stderr)
        return None

    subs = info["subscribers"]
    tf = time_filter or auto_time_filter(subs)

    print(f"\nr/{subreddit}  |  {subs:,} subscribers  |  time_filter={tf}")
    print(f"Fetching top {num_posts} posts...")

    posts = get_top_posts(subreddit, tf, num_posts)
    if not posts:
        # Fallback to longer window
        for fallback in ["month", "year", "all"]:
            if fallback != tf:
                print(f"  No posts with '{tf}', trying '{fallback}'...")
                posts = get_top_posts(subreddit, fallback, num_posts)
                if posts:
                    tf = fallback
                    break
    if not posts:
        print(f"  No posts found for r/{subreddit}.", file=sys.stderr)
        return None

    print(f"Got {len(posts)} posts. Fetching comments...")
    total_comments = 0
    for i, post in enumerate(posts):
        short_title = post["title"][:55]
        print(f"  [{i+1}/{len(posts)}] {short_title}... ({post['num_comments']} comments)")
        comments = get_post_comments(post["id"], subreddit)
        post["comments"] = comments
        total_comments += len(comments)

    result = {
        "subreddit": subreddit,
        "info": info,
        "time_filter": tf,
        "scraped_at": datetime.utcnow().isoformat() + "Z",
        "total_posts": len(posts),
        "total_comments": total_comments,
        "posts": posts,
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"reddit_{subreddit}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nDone  r/{subreddit}: {len(posts)} posts, {total_comments} comments -> {out_path}")
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Reddit Market Research Scraper — scrape posts + comments for pain-point analysis"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--subreddit", "-s", help="Subreddit name (without r/)")
    group.add_argument("--topic", "-t", help="Broad topic — will auto-discover subreddits")

    parser.add_argument("--posts", "-n", type=int, default=100, help="Posts to scrape per subreddit (default 100)")
    parser.add_argument(
        "--time",
        choices=["hour", "day", "week", "month", "year", "all"],
        help="Time filter (auto-detected if omitted)",
    )
    parser.add_argument("--output", "-o", default="./reddit_data", help="Output directory")
    parser.add_argument(
        "--max-subreddits", type=int, default=3,
        help="When using --topic, how many subreddits to scrape (default 3)",
    )

    args = parser.parse_args()

    if args.subreddit:
        scrape_subreddit(args.subreddit, args.posts, args.time, args.output)
    else:
        # Discover subreddits, then scrape each
        subs = discover_subreddits(args.topic, max_results=args.max_subreddits)
        if not subs:
            print("No subreddits found. Try a more specific topic.", file=sys.stderr)
            sys.exit(1)

        print(f"\nDiscovered {len(subs)} subreddits:")
        for i, s in enumerate(subs):
            print(f"  {i+1}. r/{s['name']}  ({s['subscribers']:,} subscribers)")
        print()

        # Save discovery results
        os.makedirs(args.output, exist_ok=True)
        with open(os.path.join(args.output, "subreddit_discovery.json"), "w") as f:
            json.dump(subs, f, indent=2)

        for s in subs:
            scrape_subreddit(s["name"], args.posts, args.time, args.output)


if __name__ == "__main__":
    main()
