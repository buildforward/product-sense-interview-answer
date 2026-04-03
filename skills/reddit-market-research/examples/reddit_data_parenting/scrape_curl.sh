#!/bin/bash
# Reddit scraper using curl - fallback when Python urllib gets blocked
# Usage: bash scrape_curl.sh <subreddit> <time_filter> <num_posts> <output_dir>

SUBREDDIT="${1:-toddlers}"
TIME_FILTER="${2:-month}"
NUM_POSTS="${3:-100}"
OUTPUT_DIR="${4:-./reddit_data_parenting}"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

mkdir -p "$OUTPUT_DIR"

echo "=== Scraping r/$SUBREDDIT (top/$TIME_FILTER, $NUM_POSTS posts) ==="

# Step 1: Fetch posts (paginated)
POSTS_FILE="$OUTPUT_DIR/posts_${SUBREDDIT}.json"
echo "[]" > "$POSTS_FILE"

AFTER=""
FETCHED=0
while [ $FETCHED -lt $NUM_POSTS ]; do
    BATCH=$((NUM_POSTS - FETCHED))
    if [ $BATCH -gt 100 ]; then BATCH=100; fi

    URL="https://www.reddit.com/r/$SUBREDDIT/top.json?t=$TIME_FILTER&limit=$BATCH&raw_json=1"
    if [ -n "$AFTER" ]; then
        URL="${URL}&after=$AFTER"
    fi

    echo "  Fetching posts (offset=$FETCHED)..."
    sleep 3
    RESPONSE=$(curl -s -H "User-Agent: $UA" "$URL")

    if echo "$RESPONSE" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
        # Extract post data
        echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
children = data.get('data',{}).get('children',[])
posts = []
for c in children:
    p = c['data']
    posts.append({
        'id': p['id'],
        'title': p.get('title',''),
        'author': p.get('author','[deleted]'),
        'score': p.get('score',0),
        'num_comments': p.get('num_comments',0),
        'selftext': p.get('selftext',''),
        'permalink': p.get('permalink',''),
        'created_utc': p.get('created_utc',0),
        'link_flair_text': p.get('link_flair_text',''),
    })
# Append to existing file
existing = json.load(open('$POSTS_FILE'))
existing.extend(posts)
json.dump(existing, open('$POSTS_FILE','w'), indent=2, ensure_ascii=False)
after = data.get('data',{}).get('after','')
print(f'{len(posts)} posts fetched, after={after}')
"
        AFTER=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('after','') or '')")
        NEW=$(echo "$RESPONSE" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('data',{}).get('children',[])))")
        FETCHED=$((FETCHED + NEW))

        if [ -z "$AFTER" ] || [ "$NEW" -eq 0 ]; then
            echo "  No more posts available."
            break
        fi
    else
        echo "  ERROR: Invalid JSON response. Reddit may be blocking."
        echo "$RESPONSE" | head -100
        break
    fi
done

echo "  Total posts: $FETCHED"

# Step 2: Fetch comments for each post
echo ""
echo "  Fetching comments for $FETCHED posts..."

python3 << 'PYEOF'
import json, subprocess, time, sys

subreddit = "$SUBREDDIT"  # will be replaced by bash
output_dir = "$OUTPUT_DIR"
ua = "$UA"

# Actually use the variables properly
PYEOF

# Use a python script that reads the posts file and fetches comments via curl
python3 - "$POSTS_FILE" "$OUTPUT_DIR" "$SUBREDDIT" "$UA" << 'PYEOF'
import json, subprocess, time, sys, os

posts_file = sys.argv[1]
output_dir = sys.argv[2]
subreddit = sys.argv[3]
ua = sys.argv[4]

posts = json.load(open(posts_file))
print(f"  Fetching comments for {len(posts)} posts...")

for i, post in enumerate(posts):
    pid = post['id']
    permalink = post['permalink']
    title = post['title'][:55]
    print(f"  [{i+1}/{len(posts)}] {title}... ({post['num_comments']} comments)")

    time.sleep(3)
    url = f"https://www.reddit.com{permalink}.json?limit=500&depth=10&sort=top&raw_json=1"

    result = subprocess.run(
        ['curl', '-s', '-H', f'User-Agent: {ua}', url],
        capture_output=True, text=True, timeout=30
    )

    try:
        data = json.loads(result.stdout)
    except:
        print(f"    ERROR: Could not parse response")
        post['comments'] = []
        continue

    # Extract comments recursively
    def extract(node, depth=0):
        comments = []
        if isinstance(node, dict):
            kind = node.get('kind','')
            d = node.get('data',{})
            if kind == 'more':
                return comments
            if d.get('body'):
                comments.append({
                    'author': d.get('author','[deleted]'),
                    'score': d.get('score',0),
                    'body': d.get('body',''),
                    'depth': depth,
                    'id': d.get('id',''),
                })
            replies = d.get('replies','')
            if isinstance(replies, dict):
                for child in replies.get('data',{}).get('children',[]):
                    comments.extend(extract(child, depth+1))
            for child in d.get('children',[]):
                if isinstance(child, dict):
                    comments.extend(extract(child, depth))
        elif isinstance(node, list):
            for item in node:
                comments.extend(extract(item, depth))
        return comments

    comments = []
    if isinstance(data, list) and len(data) > 1:
        for child in data[1].get('data',{}).get('children',[]):
            comments.extend(extract(child))

    post['comments'] = comments
    print(f"    -> {len(comments)} comments")

# Save final output
total_comments = sum(len(p.get('comments',[])) for p in posts)
output = {
    'subreddit': subreddit,
    'total_posts': len(posts),
    'total_comments': total_comments,
    'posts': posts,
}

out_path = os.path.join(output_dir, f'reddit_{subreddit}.json')
json.dump(output, open(out_path, 'w'), indent=2, ensure_ascii=False)
print(f"\n  DONE: {len(posts)} posts, {total_comments} comments -> {out_path}")
PYEOF
