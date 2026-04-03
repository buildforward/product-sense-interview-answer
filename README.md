# AI PM Skills

No-slop PM skills for real product judgment. Curated list of sharp PM skills that challenge your thinking. Cover product strategy, decision-making, and career growth. Built by a staff PM with 10+ yoe.

---

## Skills

| Skill | What It Does | Try It |
|---|---|---|
| [Product Sense Interview](skills/product-sense-interview-answer/) | Generates a structured, spoken-register PM interview script with 6 timed sections, prioritization logic, and MVP framing | *"How would you improve YouTube?"* |
| [Strategic Debate](skills/strategic-debate/) | Stress-tests your product decision by staging a sharp debate between two famous strategic thinkers (e.g., Jobs vs. Andreessen) | *"Debate this: should we launch a freemium tier?"* |
| [Reddit Market Research](skills/reddit-market-research/) | Scrapes Reddit communities to surface underserved pain points, ranked by frequency and severity, with product opportunity concepts | *"Find product ideas from r/ADHD"* |

---

## Product Sense Interview Answer

Turns open-ended PM interview questions into a complete spoken-answer script with a consistent 6-section flow: Clarification, Strategic Rationale, Product Goal, Market Segmentation, Pain Points, and Solutions. Each section has hard word budgets, MECE lists, and fixed transitions for delivery under pressure.

Example prompts: *"Design a fire alarm for the deaf"*, *"What would you build next for DoorDash?"*, *"How would you grow Duolingo?"*

[Full details and examples](skills/product-sense-interview-answer/)

---

## Strategic Debate

Takes a product decision, PRD, or strategy and stages a genuine 2-person debate between strategic thinkers from a roster of 8 personas (Musk, Jobs, Bezos, Munger, Thiel, Andreessen, Zhang Yiming, Sun Tzu). Auto-selects the sharpest pairing for your input type. Ends with a Decision Brief: where they agree, the core trade-off, and a concrete first move.

Example prompts: *"Stress test my idea to add social features to a fitness app"*, *"What would Bezos and Thiel think about this pricing strategy?"*

[Full details](skills/strategic-debate/)

---

## Reddit Market Research

Scrapes Reddit posts and full comment trees from target subreddits, then runs a 4-pass analysis (Landscape Scan, Thematic Clustering, Deep Extraction, Scoring) to produce a ranked list of 10 underserved pain points with evidence quotes and product concepts.

Example prompts: *"Analyze r/Parenting for product opportunities"*, *"What are freelancers struggling with on Reddit?"*

[Full details and examples](skills/reddit-market-research/)

---

## How to Use

### Claude Cowork (recommended)

1. Download this repo as a ZIP from GitHub
2. In Claude Cowork, open **Customize** (bottom-left) → **+** next to Personal plugins → **Upload plugin**
3. Drop the ZIP — all three skills become available via the `/` command

### Claude.ai Chat

1. Download the `SKILL.md` file for the skill you want
2. Start a new conversation and attach it
3. Ask your question

### Claude Code (CLI)

```bash
claude --context skills/product-sense-interview-answer/SKILL.md "How would you improve Spotify?"
```

### ChatGPT / Other Platforms

Each skill is a standalone markdown file (`SKILL.md`). Paste it into any system prompt, knowledge field, or `.cursorrules` file and the agent will apply the framework automatically.

---

## Repo Structure

```
ai-pm-skills/
├── skills/
│   ├── product-sense-interview-answer/   # PM interview script generator
│   │   ├── SKILL.md
│   │   ├── examples/
│   │   └── README.md
│   ├── strategic-debate/                 # Decision stress-testing via debate
│   │   ├── SKILL.md
│   │   └── examples/
│   └── reddit-market-research/           # Reddit pain point discovery
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── examples/
├── instruction-screenshot/               # Setup guide images
└── README.md
```

---

## License

MIT
