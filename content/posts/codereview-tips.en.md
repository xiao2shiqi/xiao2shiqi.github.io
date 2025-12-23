+++
date = '2020-08-25T14:55:57+08:00'
draft = false
title = 'Several CodeReview Experiences Summarized from Practice'
tags = ["Code Quality","Technical Management"]
+++

Experienced programmers know that Code Review can greatly improve code quality, enforce coding standards, and enhance team capabilities. As the famous technical expert "Haoel" (Left-Eared Mouse) once said:

> I believe there is no need to stay in a company that doesn't do Code Review (because a company that doesn't do Code Review definitely doesn't respect technology).
>
> — From "The Programmer's Level-Up Guide - Cultivation"

Many tech companies abroad, such as Google and Amazon, value Code Review highly and do it exceptionally well. However, many domestic companies struggle with it, often leading to counterproductive results. Here are some common situations I've seen:

* Mutual accusations between team members during Code Review, harming team cohesion.
* Formalized Code Review that doesn't improve quality or reduce bugs but instead lowers development efficiency.
* Code Review is effective, but the process is too heavy, slowing down the team.

We are also practicing Code Review and have encountered obstacles and gathered experiences. If you face similar issues, this article might help.

I won't re-list all the benefits here. Instead, let's focus on several basic consensuses and principles:

1. The principle of efficiency: let machines do most of the work.
2. The timing of Code Review (Right time, right place, right people).
3. Key principles for promoting Code Review.

### The principle of efficiency: let machines do most of the work

Coding styles are usually fixed. For Java, common standards include:
1. [Oracle Java SE Standard](https://www.oracle.com/technetwork/java/codeconvtoc-136057.html)
2. [Google Java Guide](https://google.github.io/styleguide/javaguide.html)
3. [Alibaba Java Manual](https://github.com/alibaba/p3c)

Static standards should be checked by machines (using tools like P3C, Rubocop, SonarQube). Machines are faster, more rigorous, and don't get tired. **The essence of automation is to reduce dependence on humans**, as humans are prone to uncertainty and are not suited for repetitive, deterministic tasks.

### The timing of Code Review

**The further left a Code Review is shifted, the lower the cost of modifying code and the higher the developer's willingness to change.**

Look at the software development pipeline:

![Software Engineering Development Pipeline](https://s2.loli.net/2025/02/15/zMi5jHh12CgldIf.png)

If Code Review happens just before going live (on the right), the modification cost is high because the code has already been tested. Re-modifying means re-testing, which is a waste of resources. Developers will be less willing to refactor. Eventually, Code Review becomes a mere formality.

The best time for Code Review is after the feature branch self-testing is finished but before it's merged into the `develop` branch for official testing. This ensures fast feedback.

##### Code Review must count toward development workload

A common reason for not doing Code Review is the "lack of time." However, merging poor code leads to production bugs, forcing developers to spend even more time fixing them. While skipping Review might seem faster in the short term, the overall delivery cycle is elongated. Counting Code Review toward the workload is a way to value long-term benefits.

### Key principles for promoting Code Review

To avoid endless arguments over minor details, the team must agree on basic principles:

##### Mutual Respect

From the author's perspective:
1. Respect the reviewer's time and effort; they are helping you improve.
2. Submit high-quality, self-tested code.
3. Provide a clear commit history.

From the reviewer's perspective:
1. Be respectful and empathetic; don't use subjective criticism or emotional tones.
2. Suggestions must be based on facts or documentation, not personal preference.
3. Don't nit-pick; focus on logic and design.

##### Building Consensus

As a team:
1. The goal is to improve project quality and avoid the cycle of fixing bugs.
2. Code Review is a growth opportunity; be open-minded and inclusive.

### Conclusion

There is no "best" tool, only the "most suitable" one for your team's current stage. Whether it's centralized reviews or 1-on-1 pair programming, choosing the right way for your environment is key.
