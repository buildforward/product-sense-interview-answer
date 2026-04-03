---
name: strategic-debate
description: "Triggers when a user wants to stress-test, pressure-test, or get diverse perspectives on a product decision, PRD, proposal, strategy, plan, business idea, or any consequential choice. Trigger phrases include: 'debate this', 'what would X think', 'stress test my idea', 'play devil's advocate', 'give me different perspectives on', 'argue for and against', 'put my plan on trial', 'challenge this', 'poke holes in this', 'what am I missing', or any request to evaluate a decision from multiple strategic angles. Also triggers when a user names two thinkers or frameworks and asks them to weigh in on something, e.g. 'what would Bezos vs Jobs say about this'. Use this skill even if the user doesn't say 'debate' — if they want their idea challenged from multiple angles, this skill applies."
---

# Strategic Debate Skill

Stage a sharp, fast debate between two strategic thinkers on any product decision, proposal, or strategy. The user gets entertained by the clash and walks away with a clear decision brief.

## Core Rules

1. **Genuine tension.** Pair thinkers whose frameworks naturally conflict. Agreeable debates are useless.
2. **One point per turn.** Each persona makes ONE argument per turn. No laundry lists.
3. **Talk to each other, not past each other.** This is a conversation, not two presentations. Person B's opening must already be a reaction to Person A — not an independent speech. Every turn after the first must reference something the other person just said. Use phrases like "But that ignores...", "The problem with what you just said is...", "You're right about X, but...".
4. **Take a side.** Each persona commits to a clear, actionable position — not "it depends." They tell the user what to do.
5. **Plain language.** Write like two smart people arguing over coffee, not like consultants presenting to a board. No jargon, no MBA-speak, no framework names dropped without explanation. If your mom wouldn't understand the sentence, rewrite it. "Most coding jobs that are getting cut are the routine ones — gluing APIs together, building standard web pages" — not "standard business logic in the primary AI substitution zone."
6. **No new facts — only framework reasoning.** Personas do NOT introduce outside data, statistics, or market facts. They only work with what's in the user's input — applying their core framework to poke holes in the logic, question assumptions, and expose contradictions. Musk asks "what does this look like from first principles if you strip away the conventions?" Munger asks "what's the most likely way this fails?" Thiel asks "where's the monopoly?" Every critique must flow from the persona's one voice applied to the user's own claims. The power comes from the framework revealing what the user's own logic missed.
7. **No hallucinated quotes.** Channel reasoning style, not fabricated words.
8. **500 words max.** Entire output — conversation + decision brief — under 500 words.
9. **Match the user's language.** Output in the same language as the user's input. If the input is in Chinese, the entire output — debate and decision brief — is in Chinese. If the user explicitly requests a different language, use that instead.

---

## Persona Roster

Each persona has ONE core voice. This voice drives every critique, rebuttal, and suggestion they make — no mixing frameworks.

| Persona | One Voice | How It Sounds in a Debate | Best Foils |
|---|---|---|---|
| **Elon Musk** | First-principles thinking | "Forget what exists. What does physics actually allow here?" | Sun Tzu, Munger |
| **Steve Jobs** | Radical focus | "You're doing too many things. Kill everything but the one that matters." | Andreessen, Bezos |
| **Jeff Bezos** | Long-term patience | "You're optimizing for next quarter. Be willing to be misunderstood for years." | Munger, Jobs |
| **Charlie Munger** | Inversion | "Tell me how this fails. Now avoid that." | Bezos, Musk |
| **Peter Thiel** | Monopoly thinking | "You're competing. Stop. Find the secret that makes competition irrelevant." | Zhang Yiming, Andreessen |
| **Marc Andreessen** | Techno-optimism | "You're thinking too small. The technology wave is bigger than your plan." | Jobs, Sun Tzu |
| **张一鸣 (Zhang Yiming)** | Algorithm-first | "Remove your ego. Let data decide, not your intuition." | Thiel, Jobs |
| **孙子 (Sun Tzu)** | Strategic positioning | "You haven't studied the terrain. Know where the enemy is weak before you move." | Musk, Andreessen |

---

## Pairing Logic

Auto-select based on the input's dominant tension. The "Why They Clash" must reflect each persona's one voice — nothing else.

| Input Type | Recommended Pairing | Why They Clash |
|---|---|---|
| Product PRD / feature spec | Jobs vs. Andreessen | "Kill features" vs. "Think bigger" |
| Market entry / competitive strategy | Sun Tzu vs. Musk | "Study the enemy first" vs. "Ignore the enemy, what's physically possible?" |
| Business model / monetization | Thiel vs. Bezos | "Lock in monopoly now" vs. "Accept losses for years until you win" |
| Risky bet / uncertain payoff | Bezos vs. Munger | "Be patient, the payoff compounds" vs. "Here's how the patience kills you" |
| Growth / scaling decision | Zhang Yiming vs. Jobs | "Algorithm scales, remove your ego" vs. "Taste doesn't scale — and shouldn't" |
| Platform / infrastructure | Andreessen vs. Sun Tzu | "Bet big on the tech wave" vs. "Map the terrain before you charge" |
| Startup positioning / differentiation | Thiel vs. Zhang Yiming | "Founder conviction finds secrets" vs. "Data finds secrets, founders hallucinate" |

Default if unclear: **Musk vs. Munger** — first-principles ambition vs. how-you-die inversion.

---

## Output Structure

The entire output must be under **500 words**. The debate should read like a real conversation — not three separate "rounds."

### Setup (~40 words)

Name the two debaters. For each, one plain-language sentence explaining how they think so users unfamiliar with them know what to expect. Then state what they'll disagree on.

> **[Persona A]** — [one sentence: how they think, in plain language]. **[Persona B]** — [same]. The question: [what they'll argue about].

---

### The Conversation (~300 words total, 6 turns)

Write as a flowing back-and-forth — six turns alternating between the two personas. Each turn is ~50 words. The conversation must build: each turn responds to what the other person just said, not to the original input.

**Turn 1 — A opens.** States their position on the input. One clear argument.

**Turn 2 — B pushes back.** Doesn't give their own separate opening — directly responds to what A just said, then states their counter-position.

**Turn 3 — A fires back.** Engages B's specific counter-argument. Points out what B is getting wrong or ignoring.

**Turn 4 — B responds.** Addresses A's rebuttal. Can expose a deeper assumption or contradiction in A's logic.

**Turn 5 — A sharpens.** Doesn't concede — but the best counterargument forces them to be more precise. They tighten or adjust their recommendation in a way that accounts for B's strongest point, while still holding their core position.

**Turn 6 — B sharpens.** Same — A's strongest challenge makes B refine their advice. They stay on their side but get more specific about how to actually do it.

The key: these are not concessions. These are two people who've been pushed to give sharper, more honest advice because someone challenged them. The conversation should feel like it arrives somewhere neither person would have reached alone.

Formatting:
> **[Name]:** [Their turn. Conversational, direct, plain language. References what the other person just said.]

The conversation should feel like you're overhearing two people who disagree but respect each other — not like reading two position papers stapled together.

---

### Decision Brief (~150 words)

Drop persona voices. Write as a neutral advisor in plain language.

**Where they agreed** — 1-2 bullets. The things both sides think you should do regardless.

**The core trade-off** — One sentence framing the real either/or with stakes. This naturally leads into the next question:

**What this comes down to** — A single specific question that captures the unresolved tension. Not generic ("what's your priority?") but specific to this input. Frame it as a direct question to the user that, once they answer honestly, points them in a clear direction.

**Your first move** — One concrete discovery step the user can take today to get closer to answering that question. Not a conclusion or a final recommendation — a next action that generates information. "Talk to X", "test Y", "look up Z and see how you feel about the answer."

---

## Word Budgets

| Section | Budget |
|---|---|
| Setup | ~40 |
| Conversation (6 turns) | ~300 |
| Decision Brief | ~150 |
| **Total** | **~400-500** |

Hard ceiling: 500 words. Each turn in the conversation should be roughly equal length (~50 words). No turn should dominate.

---

## Handling User Choices

- **User specifies two personas:** Use them, even if not the "optimal" pairing.
- **User specifies one:** Auto-select from Best Foils column.
- **User specifies none:** Use Pairing Logic table.
- **User names someone off-roster:** Use them if their framework is well-known and distinct. Otherwise suggest the closest roster match.
- **User wants 3+ debaters:** Decline. Two-way debates produce tension; three-way produces mush. Suggest a second debate with a different pair.

---

## Quality Checklist

- [ ] Genuine framework tension between the two personas
- [ ] Setup introduces each persona in plain language a non-expert would understand
- [ ] Each turn: ONE point, not a list
- [ ] Every turn after Turn 1 directly references what the other person just said
- [ ] No outside facts or data introduced — all arguments come from reasoning about the user's input
- [ ] Reads like two people talking, not two essays placed side by side
- [ ] No jargon — a smart non-expert could follow the entire debate
- [ ] Turns 5-6 sharpen positions (not forced concessions) — tighter advice, not surrender
- [ ] Decision Brief flows naturally: agreements → trade-off → the question it raises → a discovery step
- [ ] "Your first move" is a discovery action, not a conclusion or recommendation
- [ ] No fabricated quotes attributed to real people
- [ ] Output language matches user input language
- [ ] Total output ≤ 500 words
