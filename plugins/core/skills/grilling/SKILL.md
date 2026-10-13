---
name: grilling
description: "Stress-test a plan, design, decision or idea through rounds of numbered questions, each with a recommended answer, until no branch is left assumed. Use only when the user asks to be challenged or questioned on a plan (grill me, stress-test this, poke holes). FR : « grille-moi », « challenge mon plan », « questionne-moi », « mets mon idée à l'épreuve », « trouve les failles »."
---

<!-- Adapted from mattpocock/skills (MIT) — https://github.com/mattpocock/skills — modified for jt33120/claude-toolkit -->

# Grilling

Interview the user until you reach a shared understanding. Map it as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled. Ask the whole frontier in one round, number each question, give your recommended answer, then wait.

```
❓ **Q1** - **<title>** : <question, options if any>

➡️ <recommended answer>
```

- Word each question so "oui" accepts the recommendation.
- A question that depends on another open question of the same round belongs to a later round.
- After each round, recompute the frontier from the answers.
- Facts are your job: look them up (files, tools, a sub-agent) instead of asking. Decisions are the user's.
- Ask in the user's language.

Done when the frontier is empty: every branch visited, nothing silently assumed. Then summarise the decisions in a short list and act on them only after the user confirms.
