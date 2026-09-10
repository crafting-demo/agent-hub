---
name: write-spec
description: Write a feature spec or PRD from a problem statement or feature idea. Use when turning a vague idea into a structured document, scoping v1 vs non-goals, or defining success metrics and acceptance criteria.
---

# Write a feature spec

Turn a problem or feature idea into a spec an engineering manager can execute
without re-asking the product questions.

## Workflow

1. Understand the ask (feature name, problem, or user request). If it is
   vague, ask the two or three questions that most change the spec — not a
   questionnaire.
2. Pull context from the configured ticket board and any files the user named.
   If those tools are not bound, proceed with what the user provided.
3. Draft the spec with the sections below. Mark invented assumptions.
4. If a board is bound, list related tickets instead of minting fake ids.

## Spec shape

- **Problem** — who is affected and what happens if we do nothing
- **Audience** — segment for v1
- **Goals** — observable outcomes, not a feature laundry list
- **Non-goals** — deferred on purpose
- **Locked decisions** — `D-01`, `D-02`, … what the user has settled; see the
  `lock-decisions` skill
- **Requirements** — user stories with acceptance criteria; label Must / Should / Could
- **Success metrics** — how we will know it worked
- **Dependencies and risks**
- **Open questions** — only what the user has not answered

Do not write application code. Do not write DESIGN.md or ENGINEERING.md.
