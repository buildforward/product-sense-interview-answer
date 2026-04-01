---
name: product-sense-interview
description: "Use this skill when the user asks to answer any product design or product sense PM interview question end to end. Triggers on a wide range of question types including but not limited to: 'design a product for X', 'how would you improve X', 'what would you build next for X', 'how would you grow X', 'build a feature for X', 'what would you change about X', 'help me answer this PM question', 'walk me through how to design / improve / build X', or any question framed as a product challenge for a company or category. If the user pastes or describes a product sense or product design interview question — even without explicitly saying 'interview' — use this skill. Produces a complete spoken-register interview script structured into 6 timed sections. Never skip sections. Never include internal reasoning steps in the output. Always use the fixed scripts verbatim."
---

# Product Sense Interview Skill

## Core Rules

1. **Separate internal reasoning from spoken output.** Steps marked `[INTERNAL]` are used to reason but must NOT appear in the final script. Steps marked `[OUTPUT]` must appear in the answer.
2. **Use fixed scripts verbatim.** Every section has canonical opener/transition phrases. Do not paraphrase them.
3. **Write conversationally.** Short sentences. Natural spoken rhythm. Use bullet points for all enumerated sub-content (players, segments, pain points, solutions). Keep narrative framing and transitions in prose.
4. **Use bold for prioritization conclusions.** When stating a rating — impact, effort, frequency, severity — bold the label. E.g., "**High user impact** — solves the core pain directly. **Medium effort** — software only, no new infra."
5. **Maintain MECE** in all lists: ecosystem players, segments, pain points, solutions.
6. **Honor the word budgets below.** These are hard ceilings, not targets. Less is more.

---

## Word Budgets by Section

These account for thinking time and interviewer interaction within the total time allocation.

| Section | Total time | Speaking time | Word budget |
|---|---|---|---|
| 1. Clarify | 2 min | ~1 min | ~130 words |
| 2. Rationale | 5 min | ~4 min | ~520 words |
| 3. Product Goal | 2 min | ~1.5 min | ~200 words |
| 4. Segmentation | 5 min | ~3.5 min | ~450 words |
| 5. Pain Points | 10 min | ~7 min | ~910 words |
| 6. Solution | 15 min | ~10 min | ~1,300 words |

---

## Workflow

Given `QUESTION`, execute the following 6 sections in order.

---

### SECTION 1 — Clarify (~2 min | ~130 words)

**[INTERNAL]** Identify ambiguities across four dimensions: definition, product/platform scope, time horizon, other constraints (geo, user type, business model). Pick the 2 most impactful to raise. If the user's question does not specify a company name, one of the assumptions must state: "Since no specific company was mentioned, I'll assume we're a startup exploring this space."

**[OUTPUT — FIXED OPENER]**
> "Before I dive in, I'd like to ask a couple of clarifying questions to make sure I'm solving the right problem."

**[OUTPUT]** State both questions and assumptions as bullets:
- **[Question 1]** — "I'll assume [X]."
- **[Question 2]** — "I'll assume [Y]."

**[OUTPUT — FIXED CLOSE]**
> "I'll proceed with those assumptions — let me know if you'd like me to adjust."

---

### SECTION 2 — Rationale (~5 min | ~520 words)

**[OUTPUT — FIXED TRANSITION]**
> "Now let me walk through my rationale for why this is worth building."

**[OUTPUT] Market:** Bullets with bold labels. No specific numbers — make the case with qualitative signals only.
- **Big market:** 1–2 sentences on size signal — industry trends, behavioral shifts, macro tailwinds.
- **Why important?** 1 sentence. Personal and social dimension.
- **Why now?** 1 sentence. What's changed recently that makes this more urgent?

**[INTERNAL]** Map competitors into broad categories, identify top 2–3 names, identify the gap.

**[OUTPUT] Company Fit:** Bullets with bold labels. Keep each point to 1–2 tight sentences. If no specific company was named in the question (i.e., startup assumption is in effect), skip "Mission fit" and "Business objective" — these require a known company to be meaningful.
- **Mission fit:** How this serves the company's mission.
- **Business objective:** How this product contributes to a specific business goal — e.g., revenue, retention, growth, or cost-cutting.
- **Competitive landscape:** Broad category first, then top 2–3 names.
- **Market gap:** What they all fail to do.
- **Unique strength:** One specific, non-generic company advantage.

**[OUTPUT] 1-Line Thesis:** One crisp sentence that sets up everything that follows.

---

### SECTION 3 — Product Goal (~2 min | ~200 words)

**[OUTPUT — FIXED TRANSITION]**
> "With that rationale in mind, here's the product goal I'd orient the team around."

**[INTERNAL]** Synthesize rationale into a north star. ≤ 20 words. Active voice. Outcome-oriented — not a feature description. Do NOT describe the solution or mechanism in the goal. Keep it at the level of user outcome and broader impact.

Format guide: "Help [user] [achieve outcome], so that [broader impact]."

**[OUTPUT]** State the one-line vision. Then 1–2 sentences describing what success looks like for the user — observable behavior or outcome, not product features.

---

### SECTION 4 — Market Segmentation (~5 min | ~450 words)

**[OUTPUT — FIXED OPENER]**
> "Next, I'll segment the market. Before diving in, I want to lay out my prioritization logic so we can evaluate as we go. I'll prioritize based on: Reach, Impact, and Strategic Fit with the product goal and company strengths."

**[INTERNAL]** Think broadly about the ecosystem — not just end-users but also supply-side players, demand-side players, supporting roles, and enabling parties (e.g., creators, merchants, moderators, advertisers, caregivers, intermediaries, platform operators). List 5 that are meaningfully distinct. Score each on Reach, Impact, Strategic Fit. Rank objectively — the top player may not score highest on every dimension, and that's fine. Do not inflate ratings to justify the pick.

Choose segmentation dimensions that genuinely change the user's needs — dimensions where different segments have distinct behaviors, different pain intensity, and would require meaningfully different product solutions. Good dimensions often include: goal-based (life stage, health/edu/finance goal), industry/domain, consequence-based (stakes level), constraint-based (expertise, budget, team size). Avoid dimensions that: (1) would share the same product solution across segments, (2) artificially cut off the user journey or solution space (e.g., "activity mode" splits a PM's workflow into slices that should be served holistically), or (3) are demographic cuts that don't change product needs. Use judgment — the best dimension depends on the specific question.

**[OUTPUT] Ecosystem Players:** List all 5 as bullets. Think broadly — include supply-side, demand-side, supporting, and enabling roles. For each, add a parenthetical indicating their role in the ecosystem.
- [Player 1 — archetype name] (e.g., end-user, supply-side, enabler, intermediary, support role)
- [Player 2]
- [Player 3]
- [Player 4]
- [Player 5]

**[INTERNAL]** Score the top 2–3 candidates on Reach, Impact, Strategic Fit. Compare them honestly — the top pick may not score highest on every dimension.

**[OUTPUT]** State the chosen player with per-criteria ratings and a 1-sentence rationale. Be honest — if the top pick doesn't score highest on every dimension, say so explicitly.

"I'd focus on [Player X]. **Reach: [high/medium/low]** — [why]. **Impact: [high/medium/low]** — [why]. **Strategic fit: [high/medium/low]** — [why]."

**[OUTPUT] Primary Dimension — [Name]:** Why this dimension matters in 1 sentence. Then MECE segments as bullets, then the chosen segment with bold ratings.
- [Segment A]
- [Segment B]
- [Segment C]

"I'd prioritize [Segment X]. **Reach: high** — [why]. **Impact: high** — [why]. **Strategic fit: high** — [why]."

**[OUTPUT] Secondary Dimension — [Name]:** Same format. End with:
> "So my target segment is [X]."

**[OUTPUT] Persona:** Two tight lines. One sentence for who they are (demographics + context). One sentence for what they care about (motivation or priority) — do not explain why they care about it. No pain points.

---

### SECTION 5 — Pain Points (~10 min | ~910 words)

**[INTERNAL]** Map the user journey into 4–6 stages. Identify 10 MECE pain points across it. Each must reflect a distinct emotional state.

**[OUTPUT]** Organize by journey stage. Each pain point is a bullet — short phrase or 1 tight sentence. Add a specific example only when it makes the pain immediately vivid; keep it to a clause, not a paragraph.

Example format:
- **Can't find the right option** — too many choices, no signal on what fits her situation
- **Fit is a gamble** — size varies wildly across brands, she's returned 3 pairs this year

**[OUTPUT — FIXED TRANSITION]**
> "I'll prioritize pain points by two dimensions: frequency — how often users encounter this — and severity — how much it blocks the job to be done, how underserved it is by existing solutions, and the emotional toll it takes."

**[INTERNAL]** Rank all 10 on frequency × severity. Severity is determined by three factors in this order: (1) how much the pain blocks the user's job to be done, (2) how underserved the pain is — index higher on pain points where existing solutions don't address the problem well, so the resulting solution is differentiated rather than a copycat, and (3) the emotional toll it takes on the user. Identify #1.

**[OUTPUT]** Name the top pain point. Then explain why it wins in exactly two parts: (1) **Frequency** — how often and in what situations users hit this, and (2) **Severity** — one tight sentence covering all three factors: how it blocks the job, how underserved it is, and the emotional toll. Keep severity to 1–2 sentences max — do not elaborate each factor into its own paragraph.

---

### SECTION 6 — Solution (~15 min | ~1,300 words)

**[OUTPUT]** Name 3 distinct, MECE solutions as bullets. Each solution is **1 short sentence** — what it does, not how it works in detail.
- **[Solution 1 name]:** [One sentence.]
- **[Solution 2 name]:** [One sentence.]
- **[Solution 3 name]:** [One sentence.]

**[OUTPUT — FIXED TRANSITION]**
> "To evaluate these, I'll use two criteria: User Impact — how well it solves the problem and how desirable it is — and Effort — the complexity and time to build."

**[OUTPUT]** Evaluate each solution in 2 sentences using bold labels:
- **[Solution 1]:** **[High/Medium/Low] user impact** — [why in a few words]. **[High/Medium/Low] effort** — [why in a few words].
- **[Solution 2]:** same format.
- **[Solution 3]:** same format.

**[OUTPUT] MVP:** Declare the winner. List core features as tight bullets — what it does, not how it's built. Call out 1–2 explicit v1 exclusions.

**[OUTPUT] Risks + Mitigations:** 2 bullets max.
- **Risk:** [Name it]. **Mitigation:** [One specific action.]

**[OUTPUT — FIXED CLOSE]**
> "To summarize: I'd focus on [target segment], specifically around the pain of [top pain point], and build [MVP solution] as our first bet. Happy to go deeper on any section."

---

## Quality Checklist

- [ ] All 6 sections present and labeled with timing
- [ ] Word budgets respected — no section is bloated
- [ ] No internal reasoning in output
- [ ] Fixed scripts appear verbatim
- [ ] All lists are MECE
- [ ] Bullets used for all enumerated sub-content; prose for transitions
- [ ] Bold labels on all prioritization ratings (reach, impact, effort, frequency, severity)
- [ ] No specific market size numbers or percentages
- [ ] If no company specified, startup assumption is stated in Clarify section
- [ ] Product goal is outcome-oriented — no solution or mechanism described in the goal
- [ ] Product goal output is one-line vision + "success looks like" only — no "in practice" unpacking
- [ ] Ecosystem players span supply-side, demand-side, supporting, and enabling roles — not just end-users
- [ ] Ecosystem player scoring (top 2–3 comparison) is INTERNAL only — not in output
- [ ] Ecosystem player summary includes per-criteria ratings (Reach, Impact, Strategic Fit) for the chosen player
- [ ] Ecosystem player prioritization is honest — ratings not inflated to justify the pick
- [ ] Segmentation dimensions change user needs in a real way — distinct behavior, pain intensity, and product solutions across segments
- [ ] Segmentation dimensions do NOT artificially cut off the user journey or solution space
- [ ] Dimensions labeled "Primary" and "Secondary" — not "First" and "Second"
- [ ] Persona is exactly two sentences: who they are + what they care about (no "why")
- [ ] Top pain point explicitly names both **Frequency** and **Severity** (blocking + underserved + emotional toll) as dimensions
- [ ] Pain points are short phrases or 1-sentence bullets — not paragraphs
- [ ] Each solution description is 1 short sentence
- [ ] MVP includes explicit v1 exclusions
- [ ] Persona has no pain points
- [ ] Closing summary names segment, pain point, and solution
