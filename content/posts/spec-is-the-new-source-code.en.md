+++
date = '2026-03-06T00:00:00+08:00'
draft = false
title = 'Code Is a Byproduct: In the AI Coding Era, the Real Source Code Has Changed'
description = 'In the age of AI Coding, code can be generated and discarded at any time. What truly matters — the irreplaceable artifact — is how you describe requirements, define methods, and specify acceptance criteria. That is the new source code.'
tags = ["AI Coding", "Vibe Coding", "Spec", "Prompt Engineering"]
+++

I've been working through Stanford's AI coding course, and one of the reading assignments has stuck with me ever since.

![Code Is a Byproduct: In the AI Coding Era, the Real Source Code Has Changed](/images/posts/spec-is-the-new-source-code/cover.png)

The article is called *Specs Are the New Source Code*, written by Ravi Mehta and Danny Martinez. The argument is simple, but unsettling when you think it through: in the AI Coding era, code is becoming a byproduct. The real source code is the Spec you write.

I want to explain this in my own words, because the implications reach beyond product managers — they affect everyone who writes code.

### What Is Vibe Coding?

Vibe Coding is a new way of programming: you describe what you want to an AI, the AI generates the code, you review the result, adjust direction, and iterate. The act of writing code itself is now largely delegated to AI.

You've probably already done this: describe a feature to Claude Code or Codex, get a working version in five minutes, tweak the prompt and re-run if you're not happy, then keep moving forward. You're barely writing code directly — but you're directing the entire process.

The change this brings is deeper than most people realize.

### Code Got Cheap — But Not Everything Did

When code can be generated in minutes, when you can throw it away and regenerate it freely, the marginal cost of producing code approaches zero.

This doesn't mean code is unimportant. Running code obviously matters. But the cost of producing a line of code is no longer the bottleneck. Features that used to take days now take hours.

So where's the bottleneck?

It's in knowing what you want — and being able to articulate it precisely.

### Why Spec Became the New Source Code

The article introduces a concept called Lossy Projection, which I think is the most valuable insight in the whole piece.

Code is a lossy compression of your intent. It tells you *what was done*, but not *why it was done*, *what the boundary conditions are*, or *what counts as success*. Code contains no context, no reasoning behind decisions, no record of the conversations between you and your users.

Finished code is static. It captures a single historical moment.

A well-written Spec is different. It contains intent, methodology, acceptance criteria, and the context behind every decision. It can generate code, documentation, test cases — and months later, remind you why you designed something the way you did.

In other words, code is generated *from* the Spec, not the other way around. You can throw away code and regenerate it. But if you throw away the Spec, you've genuinely lost the decision itself.

This is why the Spec is the new source code: it's the irreplaceable artifact.

### The Workflow Has Flipped

The article contrasts the old and new development flows:

Old flow: Vague idea → Wireframes → Design → Engineers build MVP → Customer feedback → Painful Spec revision → Refactor → Pray.

New flow: Vague idea → Quick prototype → Customer feedback → Clear Spec → AI-assisted implementation.

Notice the fundamental reversal in order.

Before, you had to write down all your requirements before getting real user feedback. That was hard, because you were building on assumptions — and the Spec was probably wrong in many places.

Now, you can use AI to quickly build something working, take it to real users, and *then* write the Spec based on validated learning. The Spec becomes an output, not just an input. You're writing requirements from verified understanding, not guessing in the dark.

![The new development workflow: from vague idea to clear Spec](/images/posts/spec-is-the-new-source-code/file-20260302163101395.png)

This isn't just faster. It's fundamentally different.

### Who Becomes More Valuable in This Shift

The article makes a direct claim:

> In the near future, the most effective communicators will be the most valuable programmers.

That's worth pausing on. The data is already beginning to validate it: demand for product managers hasn't fallen because of AI — it's grown. Because as engineering delivery speeds up, the bottleneck of "figuring out what to build" becomes sharper.

![PM demand trends in the AI era](/images/posts/spec-is-the-new-source-code/file-20260302163710750.png)

Historically, a programmer's core value was the ability to translate ideas into code. AI is rapidly taking over that translation. But there's one thing AI still can't do: truly understand what a user needs, and clearly express that understanding.

That's exactly what writing a Spec requires. A good Spec starts with genuinely understanding the user's problem — not the surface-level request, but the real underlying motivation.

So something interesting has happened: skills that were once dismissed as "soft" — understanding requirements, defining problems, communicating clearly — have become the hardest hard skills of this era.

This matters more for engineers than it might seem. You used to be able to say "I'm not great at explaining things, but my code is solid." That moat is narrowing — because "solid code" is an execution-layer capability, and execution is increasingly delegated to AI.

### What It Takes to Write a Good Spec

The article shares a case study: non-technical contributors writing Specs that directly drive AI to modify a codebase, open PRs, and wait for senior engineers to review. Three prerequisites make this work:

Being Specific: Vague Specs produce messy codebases. "Make the search better" is useless as AI input. You need to say: how are results ranked, what happens when nothing is found, how are edge-case inputs handled.

Being Selective: This approach works for tasks with clear boundaries. Complex tasks requiring deep architectural understanding still need expert judgment. Knowing what *can* be delegated to AI — and what can't — is itself a skill.

Gatekeeping: AI-generated code must be reviewed by someone qualified. This isn't distrust of AI. It's basic responsible engineering practice.

Writing a good Spec is, in a sense, precisely externalizing your understanding of a task. That ability is not evenly distributed.

### The Value of Understanding Work Is Rising

The article includes a passage worth quoting in full:

> Today, AI gains are extremely uneven. Some domains — generating code, text, images — have experienced quantum leaps and now run at AI speed. Others — engaging with customers, uncovering needs, persuading buyers — still run at human speed. This uneven distribution is reshaping product teams. The focus is shifting from execution work to understanding work.

Understanding work vs. execution work — I think this is the most important distinction in the piece.

Execution work: translating requirements into code, designs into interfaces, drafts into finished documents. AI is rapidly absorbing all of this.

Understanding work: figuring out what the user's real problem is, what's worth building, why a design decision makes sense. This still runs at human speed.

When execution is automated, the scarcity of understanding becomes visible. Someone who can turn a vague idea into a precise Spec is hard to replace — because that precision comes from genuine depth of understanding, not just capability.

### What I Do Now

In practice: before starting any AI coding task, the first thing I do now is write a short document. It typically includes:

- What problem this task is solving
- The expected approach
- What "done" looks like (acceptance criteria)
- What's out of scope and shouldn't be touched

I used to do this occasionally, informally. Now it's a mandatory step every time.

Not because of ritual — because it works. Tasks described clearly get done well. Tasks described vaguely require repeated correction. Over time, this document accumulates into the most precise external record of how I think about a project.

Code can be rewritten. That document, once lost, is gone.

### Closing Thought

Vibe Coding is not science fiction. It's happening now. Tools are changing. Workflows are changing. What it means for something to be valuable is changing.

Code becoming a byproduct doesn't diminish code — it means the cost of producing code has dropped so dramatically that the valuable layer has shifted upward: how you define the problem, how you describe what you need, how you know when something is right.

That is the new source code.
