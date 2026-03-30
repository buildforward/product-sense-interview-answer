# Product Sense Interview

A skill for answering PM product sense and product design interview questions in a structured, interview-ready format.

It turns open-ended prompts like "Design a product for X" or "How would you improve X?" into a complete spoken-response script with a consistent 6-section flow, fixed transitions, prioritization logic, and clear MVP framing.

## What This Skill Does

- Answers product sense / product design interview prompts end to end
- Produces a spoken-register response instead of raw notes
- Forces a consistent structure so answers are easier to deliver live
- Emphasizes market rationale, segmentation, pain points, and solution tradeoffs
- Uses explicit prioritization criteria instead of vague brainstorming

## Best For

Use this skill for prompts such as:

- "Design a product for travelers with flight anxiety"
- "How would you improve Spotify for college students?"
- "What would you build next for DoorDash?"
- "Build a feature for Instagram creators"
- "Help me answer this PM interview question"

## Output Structure

The skill generates answers in 6 timed sections:

1. Clarify
2. Rationale
3. Product Goal
4. Market Segmentation
5. Pain Points
6. Solution

Each section has rules for pacing, content, and phrasing so the final answer sounds like an actual interview response rather than a messy framework dump.

## What Makes It Different

- Spoken-answer oriented: optimized for saying the answer out loud
- Fixed transitions: creates cleaner delivery under interview pressure
- MECE lists: reduces overlap across segments, pain points, and solutions
- Prioritization built in: forces explicit tradeoffs on reach, impact, fit, frequency, severity, and effort
- Strong PM structure: balances user insight with business and strategic reasoning

## Example Prompt

```text
Use $product-sense-interview to answer: How would you improve LinkedIn for new college graduates?
```

## Install In Codex

If this repo is published on GitHub, install the skill with:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <your-github-username>/product-sense-interview-repo \
  --path product-sense-interview
```

After installing, restart Codex to pick up the new skill.

## Repo Layout

```text
product-sense-interview/
  README.md
  SKILL.md
```

## Good To Know

- This skill is designed for product sense / product design style questions, not behavioral interviews.
- It is best when you want a polished, interview-ready answer rather than a loose brainstorming outline.
- You can customize the tone, phrasing, or evaluation criteria by editing `SKILL.md`.
