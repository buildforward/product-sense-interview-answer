---
name: reddit-market-research
description: >
  Scrape Reddit communities to identify underserved pain points and product opportunities.
  Use this skill whenever the user wants to: find product ideas from Reddit, analyze a subreddit
  for unmet needs, discover what people are struggling with in a community, do market research
  on Reddit, find pain points for a topic, identify gaps in existing tools, or turn Reddit
  complaints into product concepts. Also triggers on: "scrape reddit", "what are people
  complaining about", "what do people need", "underserved problems", "product opportunities
  from reddit", "analyze r/", or any request involving Reddit data collection and analysis
  for product ideation — even if the user just names a topic without mentioning Reddit
  (e.g., "find pain points in the ADHD space" or "what should I build for remote workers").
---

# Reddit Market Research — Pain Point Discovery

This skill scrapes Reddit posts and comments, then runs a structured 4-pass analysis to identify the 10 most promising underserved pain points a builder could turn into a product.

## When to use this skill

- User provides a **subreddit** (e.g., "analyze r/ADHD")
- User provides a **broad topic** (e.g., "find product ideas for remote workers") — you'll discover the right subreddits yourself
- User asks for pain points, unmet needs, product gaps, or market research tied to a community

## Workflow Overview

```
1. CLARIFY   →  Subreddit or topic? Any vertical focus? (15 seconds)
2. SCRAPE    →  Run the scraper script (5-30 minutes depending on volume)
3. ANALYZE   →  4-pass analysis on the scraped data (the core of this skill)
4. DELIVER   →  Ranked list of 10 pain points with product concepts
```

---

## Step 1: Clarify the Target

Before scraping, confirm two things:

**A) Subreddit vs. topic**

| User says | What to do |
|-----------|-----------|
| "r/ADHD" or "the ADHD subreddit" | Use that subreddit directly with `--subreddit` |
| "ADHD" or "people with ADHD" | Use `--topic` to auto-discover relevant subreddits, then let the user confirm which to scrape |
| "remote work productivity tools" | Use `--topic` with the full phrase; expand keywords if needed |

When the user provides only a topic, the scraper searches Reddit and returns the top subreddits by subscriber count. Present these to the user and ask which to include before proceeding — or, if the top picks seem obviously right, proceed and note which subreddits you chose.

**B) Any vertical filter?**

Sometimes the user wants pain points in a specific product category (e.g., "productivity tools" or "mobile apps" or "AI plugins"). Note this — it doesn't change the scraping, but it focuses Pass 3-4 of the analysis. If the user doesn't specify, analyze all categories.

---

## Step 2: Scrape Reddit

The scraper lives at `scripts/scrape_reddit.py` (relative to this skill). It handles:
- Subreddit discovery via keyword expansion (when `--topic` is used)
- Auto-adjusting the time window based on subreddit size (large subs use shorter windows)
- Pagination to get up to 100 posts
- Recursive extraction of full comment trees (up to depth 10)
- Rate limiting to avoid Reddit API blocks

### Running the scraper

Pick the right invocation:

```bash
# When user gave a specific subreddit
python3 <skill-path>/scripts/scrape_reddit.py \
  --subreddit <name> \
  --posts 100 \
  --output ./reddit_data

# When user gave a broad topic
python3 <skill-path>/scripts/scrape_reddit.py \
  --topic "<topic>" \
  --posts 100 \
  --max-subreddits 3 \
  --output ./reddit_data
```

The scraper defaults to 100 posts per subreddit. For very active subreddits (>1M subscribers), consider using `--time week` or `--time month` to keep the data recent and relevant.

**Output:** One JSON file per subreddit in the output directory, e.g., `reddit_ADHD.json`. Each file contains the subreddit metadata, all posts, and all extracted comments with scores and nesting depth.

### If scraping fails

Reddit aggressively rate-limits and blocks automated requests. The scraper has built-in domain fallback (www.reddit.com -> old.reddit.com) and retries, but if you still get 403s:

1. **Wait and retry** — Reddit blocks are usually temporary (5-15 minutes). Increase REQUEST_DELAY in the script to 5 seconds.
2. **Install `requests` library** — sometimes `urllib` gets blocked where `requests` doesn't: `pip install requests`, then modify the scraper's `make_request` to use `requests.get()` with a session.
3. **Use browser tools** — if Chrome extension (mcp__Claude_in_Chrome) is available, navigate to the subreddit and extract data via `get_page_text` or `javascript_tool`. This is the most reliable approach since it uses the user's authenticated browser session.
4. **Use WebSearch for discovery** — when the subreddit search API is blocked but you need to find subreddits for a topic, use WebSearch with queries like `"best subreddits for [topic]" site:reddit.com` or `"r/ [topic] subreddit"`.
5. **Ask the user** — if they have pre-scraped data (like a JSON file), use that directly. Tell them to run the scraper manually: `python3 scripts/scrape_reddit.py --subreddit NAME --output ./reddit_data`
6. **Partial scrape** — if scraping worked for some posts but not all, proceed with what you have. Even 20-30 posts with good comment trees can produce useful analysis.

### Validating the scrape

After scraping, run a quick sanity check:

```bash
python3 -c "
import json, os, sys
for f in sorted(os.listdir('./reddit_data')):
    if f.startswith('reddit_') and f.endswith('.json'):
        data = json.load(open(f'./reddit_data/{f}'))
        posts = data.get('posts', [])
        comments = sum(len(p.get('comments', [])) for p in posts)
        print(f'{f}: {len(posts)} posts, {comments} comments')
"
```

Target: at least 50 posts and 1,000+ total comments for meaningful analysis. If below this, expand the time window or add more subreddits.

---

## Step 3: Analyze the Data

This is where the real value is created. Read `references/analysis_framework.md` for the full methodology. Here's the condensed version:

### Pass 1: Landscape Scan

Read all posts (titles + bodies) and the top 10-15 comments per post. Build a mental map:
- What topics keep coming up?
- What's the emotional temperature?
- What workarounds have people built?
- What community-specific vocabulary exists?

Use a script to extract an overview efficiently:

```bash
python3 -c "
import json
data = json.load(open('./reddit_data/reddit_<SUBREDDIT>.json'))
for i, post in enumerate(data['posts']):
    print(f'=== POST {i+1}: {post[\"title\"][:80]} ===')
    print(f'Score: {post[\"score\"]} | Comments: {len(post[\"comments\"])}')
    print(f'Body: {post[\"selftext\"][:300]}')
    print()
    top = sorted([c for c in post['comments'] if c['depth'] == 0], key=lambda x: x['score'], reverse=True)
    for c in top[:12]:
        print(f'  [{c[\"score\"]}pts] u/{c[\"author\"]}: {c[\"body\"][:200]}')
    print('---')
    print()
"
```

Write a 5-10 bullet landscape summary before continuing.

### Pass 2: Thematic Clustering

Search ALL comments for keyword patterns to identify candidate themes. This catches patterns that aren't visible in top comments alone.

```bash
python3 -c "
import json, re
data = json.load(open('./reddit_data/reddit_<SUBREDDIT>.json'))

# Adapt these keyword groups to the specific community
themes = {
    'theme_name': r'keyword1|keyword2|keyword3',
    # ... add 10-20 theme patterns
}

for label, pattern in themes.items():
    compiled = re.compile(pattern, re.IGNORECASE)
    hits = []
    for i, post in enumerate(data['posts']):
        for c in post['comments']:
            if compiled.search(c['body']) and len(c['body']) > 50:
                hits.append((c['score'], c['body'][:200], i+1))
    hits.sort(reverse=True)
    if len(hits) >= 3:  # minimum threshold
        print(f'### {label.upper()} ({len(hits)} mentions)')
        for score, body, pnum in hits[:5]:
            print(f'  [{score}pts|P{pnum}] {body}')
        print()
"
```

Choose keyword groups that are relevant to the specific community. The reference doc (`references/analysis_framework.md`) has suggested categories, but adapt them — a fitness community needs different keywords than a mental health or developer community.

Discard themes with fewer than 3 mentions or that appear in only 1 post.

### Pass 3: Deep Extraction

For each surviving theme (12-18), read ALL matching comments in full. The reference doc explains how to:
- Separate the **stated problem** from the **root problem** (always dig one level deeper)
- Identify **workarounds** (signal of willingness to pay)
- Gauge **severity** from emotional weight and personal stories
- Find **complexity** in disagreements between commenters

This is the most important pass. Spend time here. The quality of the final output depends on how well you understand the nuance beneath surface-level complaints.

### Pass 4: Scoring and Ranking

Score each theme on four dimensions (detailed rubrics in `references/analysis_framework.md`):

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| **Signal Strength** | 15% | Volume and quality of evidence in the data |
| **Severity & Commonality** | 25% | How painful and how widespread |
| **Wedge Viability** | 25% | Can you build a focused v1 product for this? |
| **Underserved** | 35% | Do existing solutions fail this audience? |

```
Composite = (Signal * 0.15) + (Severity * 0.25) + (Wedge * 0.25) + (Underserved * 0.35)
```

"Underserved" is weighted heaviest because even a huge pain point is worthless if good solutions exist. Before giving a high "underserved" score, think critically about whether tools already exist for this.

If the user specified a vertical filter in Step 1 (e.g., "productivity tools only"), apply it here — only rank pain points that fit within that vertical.

---

## Step 4: Deliver the Output

Present the final ranked list of 10 pain points. For each pain point, include:

1. **Name and one-line product concept**
2. **Composite score** with individual dimension scores
3. **The problem** — root cause, not just symptom (2-3 sentences)
4. **Evidence** — 3-5 exact quotes with upvote counts and post numbers
5. **Why existing tools fail** — name specific tools if commenters mentioned them
6. **Product concept** — specific and buildable (trigger moment, user action, outcome, differentiation)
7. **Wedge strategy** — the smallest viable v1 you could ship

End with a summary comparison table showing all 10 pain points side by side with their scores.

See `references/analysis_framework.md` → "Output Format" section for the exact template.

---

## Adapting to Different Subreddit Sizes

| Subreddit size | Typical scrape | Analysis notes |
|---------------|---------------|----------------|
| >1M subscribers | 100 posts from last week/month | Massive comment volume. Focus on top-voted comments and look for agreement patterns. |
| 200K-1M | 100 posts from last month | Good balance. Full analysis approach works well. |
| 50K-200K | 100 posts from last 3-6 months | May need wider time window. Community vocabulary is more niche — pay attention to it. |
| <50K | 100 posts all-time | Smaller dataset but often more passionate community. Every comment matters more. Workarounds mentioned here tend to be more creative. |

---

## Key Principles

**Mid-range comments are gold.** The highest-voted comments (500+ pts) are relatable one-liners. The most actionable pain points live in comments with 10-100 upvotes where people share detailed personal experiences and workarounds.

**Workarounds > complaints.** "I hate this" tells you there's pain. "I built a spreadsheet that tracks X and then I set 3 alarms for Y" tells you there's a product.

**The gap between knowing and doing.** For many communities (health, productivity, finance), people know what to do but can't execute. Products that bridge the knowing-doing gap are more valuable than products that provide more information.

**One community at a time.** Even if you scraped 3 subreddits, the best pain points are usually the ones that show up in all of them. Cross-subreddit signal is strong signal.
