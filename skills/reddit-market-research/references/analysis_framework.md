# Pain Point Analysis Framework

This document describes how to analyze scraped Reddit data to identify underserved pain points worth building products for. The analysis happens in four passes — each pass narrows the focus and increases the rigor.

## Table of Contents
1. [Pass 1: Landscape Scan](#pass-1-landscape-scan)
2. [Pass 2: Thematic Clustering](#pass-2-thematic-clustering)
3. [Pass 3: Deep Extraction](#pass-3-deep-extraction)
4. [Pass 4: Scoring and Ranking](#pass-4-scoring-and-ranking)
5. [Output Format](#output-format)

---

## Pass 1: Landscape Scan

**Goal:** Build a mental map of the community — what people talk about, the emotional register, the vocabulary they use.

Read through all posts (titles + body text) and the top 10-15 highest-scored comments per post. Don't analyze yet — just absorb.

Pay attention to:
- **Recurring themes**: What topics come up across multiple posts?
- **Emotional intensity**: Which posts/comments have raw frustration, desperation, or "this changed my life" energy?
- **Workarounds**: What janky solutions have people built for themselves? These signal real need.
- **Vocabulary**: What domain-specific terms, slang, or shorthand does this community use? (e.g., "doom pile," "body doubling," "spoon theory")

Write a brief landscape summary (5-10 bullet points) before proceeding.

---

## Pass 2: Thematic Clustering

**Goal:** Group the raw data into 15-25 candidate pain point themes.

Use keyword-based scanning across ALL comments (not just top-level). For each candidate theme, search for relevant keywords and count:
- Number of distinct comments mentioning it
- Total upvotes on those comments
- Number of distinct posts where it appears

Good keyword categories to scan for:

### Functional pain points
- Task management: `task, todo, list, forget, remind, calendar, planner, organize, priorit, deadline`
- Focus/attention: `focus, distract, concentrate, attention, drift, zone out, hyperfocus`
- Time: `time blind, late, running late, lost time, schedule, routine, hours passed`
- Decision-making: `decide, decision, overwhelm, paralyz, stuck, freeze, which one, too many options`
- Memory: `forgot, forget, remember, memory, lost track, where did, misplac`

### Emotional/social pain points
- Relationships: `partner, spouse, marriage, divorce, friend, lonely, misunderstood`
- Self-worth: `shame, guilt, lazy, failure, stupid, broken, not enough`
- Masking/burnout: `mask, pretend, exhaust, burnout, tired of, keeping up`

### System/tool pain points
- What they use: `app, tool, system, alarm, timer, notion, todoist, reminder, pomodoro`
- What fails: `doesn't work, stopped working, gave up on, abandoned, tried everything`
- What they wish existed: `wish there was, if only, someone should build, why isn't there`

Adjust these categories based on the specific community. A fitness subreddit needs different keywords than a mental health one.

For each theme, log:
```
Theme: [name]
Mentions: [count]
Aggregate upvotes: [sum]
Posts appearing in: [count / total posts]
Representative quotes: [3-5 highest-scored]
```

Discard any theme with fewer than 3 mentions or that appears in only 1 post — it's an individual complaint, not a pattern.

---

## Pass 3: Deep Extraction

**Goal:** For each surviving theme (aim for 12-18), extract the nuanced pain point beneath the surface complaints.

For each theme, read ALL the matching comments in full (not just previews). Look for:

### The real problem vs. the stated problem
People describe symptoms, not root causes. "I can't remember to take my medication" might really be "my morning has no consistent anchor point." The stated problem suggests a reminder app. The real problem suggests a routine-builder. Always dig one level deeper.

### Workarounds reveal willingness to pay
If someone describes a 5-step workaround they've built (spreadsheets + alarms + sticky notes + an accountability partner), that's strong signal that:
1. The pain is real enough to invest significant effort
2. No existing tool solves it adequately
3. A product that replaces the workaround has clear value

### Emotional weight = severity indicator
Comments that contain these patterns indicate high severity:
- Personal stories of loss (jobs, relationships, self-esteem)
- "I almost [severe consequence]" language
- Multiple people saying "this is me" or "I feel seen"
- Long, detailed comments (people invest writing effort proportional to pain)

### Disagreement reveals complexity
When comments debate a topic, both sides reveal real needs. For example, "medication is the only answer" vs. "medication isn't enough, I need systems too" reveals that neither medication nor pure productivity tools fully serve this audience.

For each theme, write:
```
Theme: [name]
Surface complaint: [what people say]
Root problem: [what's actually going on]
Severity evidence: [quotes showing impact]
Existing workarounds: [what people do today]
Emotional register: [frustration / desperation / resignation / anger / hope]
```

---

## Pass 4: Scoring and Ranking

**Goal:** Score each theme on four dimensions and produce the final ranked list of 10.

### Dimension 1: Signal Strength (1-10)
How much evidence exists in the data?

| Score | Criteria |
|-------|----------|
| 8-10  | 50+ mentions, appears in >50% of posts, top comments (100+ pts) discuss it |
| 5-7   | 15-49 mentions, appears in 25-50% of posts, mid-tier comments discuss it |
| 2-4   | 5-14 mentions, appears in <25% of posts, mostly deep-thread comments |
| 1     | <5 mentions, could be noise |

### Dimension 2: Severity & Commonality (1-10)
How painful is this, and for how many people?

| Score | Criteria |
|-------|----------|
| 8-10  | Life-altering consequences (lost jobs, broken relationships, health impact). Comes up daily for affected people. |
| 5-7   | Significant friction. Multiple-times-a-week problem. Emotional comments with personal stories. |
| 2-4   | Annoying but manageable. People have workarounds that mostly work. |
| 1     | Minor irritation, rarely has real consequences. |

### Dimension 3: Wedge Viability (1-10)
Is this narrow enough to build a focused v1 product around?

| Score | Criteria |
|-------|----------|
| 8-10  | Single, well-defined use case. Clear trigger moment ("when X happens, I need Y"). Could be an MVP in 2-4 weeks. |
| 5-7   | Defined but requires a few features working together. 1-2 month MVP. |
| 2-4   | Broad problem requiring a platform. Hard to know where to start. |
| 1     | "Solve ADHD" level of vague. |

### Dimension 4: Underserved by Existing Solutions (1-10)
This is the most important dimension. Even a 10/10 pain point is worthless if a good solution exists.

| Score | Criteria |
|-------|----------|
| 8-10  | No product addresses this. Or, existing products address it so poorly that people have given up on them. Comments explicitly say "I've tried everything." |
| 5-7   | Tools exist but miss a key nuance. The community has specific complaints about existing tools. Adaptation of a generic tool required. |
| 2-4   | Decent tools exist. The gap is incremental, not fundamental. |
| 1     | Well-served market. Multiple mature products compete. |

### Composite scoring
```
Final Score = (Signal * 0.15) + (Severity * 0.25) + (Wedge * 0.25) + (Underserved * 0.35)
```

The weighting deliberately emphasizes "underserved" — it's better to find a moderate pain point with zero solutions than a massive pain point with ten competitors.

---

## Output Format

The final deliverable is a ranked list of 10 pain points. For each:

```markdown
### [Rank]. [Pain Point Name] — [One-line product concept]

**Composite Score:** X.X/10
| Signal | Severity | Wedge | Underserved |
|--------|----------|-------|-------------|
| X/10   | X/10     | X/10  | X/10        |

**The problem:** [2-3 sentences explaining the root problem, not just the symptom]

**Evidence from the data:**
- "[Exact quote]" ([score]pts, Post #X)
- "[Exact quote]" ([score]pts, Post #X)
- "[Exact quote]" ([score]pts, Post #X)
- Appeared in X/Y posts, Z total mentions

**Why existing tools fail:** [What exists today and specifically why it doesn't work for this audience. Name actual tools if commenters mentioned them.]

**Product concept:** [3-5 sentences describing a specific, buildable product. What's the trigger moment? What does the user do? What's the outcome? How is this different from what exists?]

**Wedge strategy:** [How to enter this market with a focused v1. What's the smallest thing you could ship?]
```

End with a summary comparison table:

```markdown
| # | Pain Point | Signal | Severity | Wedge | Underserved | Composite |
|---|-----------|--------|----------|-------|-------------|-----------|
| 1 | ...       | X      | X        | X     | X           | X.X       |
...
```

---

## Common Pitfalls

1. **Don't confuse volume with pain.** A topic might have 200 mentions because it's fun to discuss, not because it's painful. Look for emotional weight, not just frequency.

2. **Don't mistake venting for a product opportunity.** "I hate my brain" is valid pain but not a product wedge. Look for pain attached to a *specific, recurring moment* — that's where products live.

3. **Watch for survivorship bias.** Reddit commenters are people who found the subreddit, can articulate their problems, and have time to write. The people with the worst outcomes may not be posting at all.

4. **Don't over-index on upvotes.** The most-upvoted comments tend to be relatable and funny. The most *actionable* pain points are often in mid-range comments (20-100 pts) where people share detailed personal experiences.

5. **Check if "underserved" really means "underserved."** Before scoring something 10/10 underserved, do a quick search. Sometimes great tools exist but this community just hasn't heard of them.
