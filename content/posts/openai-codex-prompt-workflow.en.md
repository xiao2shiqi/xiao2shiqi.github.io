+++
date = '2026-03-01T00:00:00+08:00'
draft = false
title = 'Use Codex Like OpenAI Engineers: A Prompt Workflow You Can Copy Today'
description = 'A practical breakdown of the official PDF: Ask before Code, 7 high-frequency scenarios, plus an AGENTS.md template you can reuse.'
tags = ["AI Coding", "Codex", "Prompt Engineering"]
+++

![How OpenAI engineers use Codex in daily work](/images/posts/openai-codex-prompt-workflow/image-20260301174504763.png)

After using AI coding tools for a while, I noticed something awkward.

Most people are not really using AI for programming. They are using it for typing code. It sounds similar, but it is not the same thing.

Typing code means: you already know what to do, and AI helps you write faster.

Programming means: you make architecture decisions, debug uncertainty, control risks, and turn ambiguity into a deliverable.

It is easy to let AI “type.” But in real engineering tasks, like taking over an unfamiliar system, refactoring across modules, or diagnosing weird production bugs, many people still get stuck. The issue is not that the tool is weak. The issue is that people do not know what to ask, how to ask, and how to move forward after the answer.

Recently, I read OpenAI’s public PDF: [How OpenAI uses Codex](https://cdn.openai.com/pdf/6a2631dc-783e-479b-b1a4-af0cfbd38630/how-openai-uses-codex.pdf).

It explains how their own engineers use Codex in day-to-day work, across 7 high-frequency scenarios, and which best practices they rely on.

My biggest takeaway: they do not treat Codex as smarter autocomplete. They treat it as a standard engineering component inside a real delivery workflow.

In this post, I translated that PDF into a practical playbook: where they use Codex most often, and what practices make it work.

![A complete map of Codex usage scenarios at OpenAI](/images/posts/openai-codex-prompt-workflow/infographic.png)

### 7 High-Frequency Codex Use Cases at OpenAI

#### Code comprehension: turn unknown systems into something queryable

When you inherit an unfamiliar codebase, the hardest part is not file count. It is the “where do I start” paralysis.

You cannot locate core logic, dependency boundaries, or real request flow. In that state, you can barely start, especially under on-call pressure.

OpenAI engineers often start with questions, not code generation: where auth lives, how requests travel, which modules are blast-radius sensitive, and what documentation should exist but does not.

A detail worth copying: after fixing a bug, do not close the thread immediately. Ask: “Where else could the same class of issue exist?” One fix becomes preventive scanning.

#### Refactoring and migration: consistency is the real difficulty

Refactoring is rarely hard because of changing code. It is hard because changes must stay consistent everywhere.

You update one API call here, but eight old patterns remain elsewhere. Production breaks, and only then you find the missing spot.

OpenAI’s approach is to scan first, modify second: map all impacted locations, summarize scope, then execute.

Codex is used to batch consistency work, not to manually patch one file at a time.

#### Performance optimization: find the real bottleneck first

The place that looks slow is often not the place that is actually slow.

You optimize a visible loop, but the real bottleneck may be repeated expensive operations or uncached DB access in a hot path.

The PDF mentions engineers spending 5 minutes on a good prompt to save 30 minutes of manual digging.

Feed Codex the suspected hot code path, ask for bottlenecks and alternatives, then make final decisions yourself.

#### Test coverage: recover the work that “should exist” but does not

In reality, many teams write just enough tests to pass.

Not because they do not care, but because they are short on time and attention. Low-coverage modules stay low-coverage until incidents expose the gap.

OpenAI points Codex directly at weak-coverage modules and lets it generate runnable test PRs, including edge cases and failure paths. Some teams even let this run overnight and review in the morning.

The key change is cost. High-volume test generation used to be expensive. Now it is cheap enough to become routine.

#### Delivery speed: scaffold at start, fill gaps near release

At kickoff, time is usually lost on repetitive scaffolding: folders, module setup, API stubs, validation, logging.

Near release, pain comes from fragmented but critical tail work: bug triage, monitoring hooks, config checks, and turning product feedback into draft code.

OpenAI offloads both ends to Codex: scaffolding early, tail tasks late, while engineers keep attention on high-judgment decisions.

#### Flow protection: let Codex hold task context while you are in meetings

Meeting-heavy days kill engineering flow.

You make progress in the morning, then context-switch across meetings all afternoon. You avoid touching small tasks because the recovery cost is high.

OpenAI engineers delegate queued tasks to Codex immediately: ask it to plan or draft while they are away. When they return, they can review concrete output instead of rebuilding context from scratch.

Another practical pattern: dump Slack threads, traces, and issues into Codex so context is organized before the next work block.

#### Exploration and design thinking: make Codex challenge your own assumptions

Sometimes you are blocked not because you have no idea, but because your idea may be wrong.

You sense flaws in current design but cannot articulate them, or you are stuck between two options with mixed tradeoffs.

Engineers use Codex for open exploration: “What if we switch to event-driven?”, “Which assumptions are weak?”, “What are the tradeoffs?”

A proactive variant: provide known bugs or deprecated methods and ask Codex to find similar patterns repo-wide for preventive cleanup.

### Best Practices

#### Ask first, then Code

OpenAI repeats this as discipline, not a trick.

Many people jump straight to “write the code.” Then they discover missing constraints, wrong direction, and oversized scope.

Their pattern: ask Codex for an implementation plan first, review and adjust, then generate code. They also recommend scoping single tasks to roughly one hour and a few hundred lines, then splitting bigger work.

#### Treat your dev environment as a product

Codex success is highly environment-dependent.

Missing startup scripts, incomplete env vars, and insufficient network permissions often cause repeated failures.

Their advice: each time you fix an environment issue, fold that fix into durable setup. Do not solve it once. Productize it.

#### Write prompts like GitHub issues

“Please refactor this module” is too vague.

Good issues define background, current problem, expected outcome, and boundaries. Prompts should do the same.

Include file paths, component names, relevant diffs, and implementation references such as “follow module X pattern.” More specific context means lower drift.

#### Use your task queue as a lightweight backlog

Not every small issue deserves immediate interruption.

Naming cleanup, simplification opportunities, and technical debt notes can all be queued.

Send these to Codex as backlog items, ask for a plan or draft, and review later during focused work.

#### Maintain an AGENTS.md

This is one of the highest-ROI habits.

Codex has no persistent memory of your conventions unless you restate them. Without project-specific context, it defaults to generic assumptions.

Store naming rules, directory structure, business constraints, known pitfalls, and common commands in `AGENTS.md`. This becomes your persistent project handbook.

#### Improve output quality with Best-of-N

For important tasks, do not request only one answer.

Ask for three alternatives, then compose the final result from the best parts. Usually no single output is perfect, but combinations are stronger.

This separates generation from judgment: Codex generates options, you make decisions.

### Why Prompt Engineering Deserves Serious Attention

Prompt quality directly controls model output quality.

Same model, same task, different prompt quality, very different outcomes. Better context and clear constraints reduce rework.

Good prompts also reduce drift and harmful output patterns. Models complete input patterns. Vague input invites average, generic output.

Structured prompts create predictability. Once a good template exists, you can reuse it across similar tasks with small variable edits.

That is why prompt engineering is not about magic words. It is about precise intent expression.

### Final Thoughts

OpenAI states Codex is still in research preview.

At the same time, they report real internal impact: faster completion of neglected tail work, safer progress on multi-module changes, and earlier detection of issues that would otherwise surface after release.

The larger lesson is not “use a smarter tool.” It is “adopt a better workflow.”

Tool choice may change. But Ask-before-Code, iterative environment hardening, explicit context, and a maintained `AGENTS.md` stay valuable.

If you are also building an AI-assisted engineering workflow, this is a practical baseline worth trying.

![AI coding community QR code](/images/posts/openai-codex-prompt-workflow/community_qr.jpg)
