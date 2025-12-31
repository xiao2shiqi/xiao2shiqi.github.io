+++
date = '2020-08-25T14:55:57+08:00'
draft = false
title = 'Several CodeReview Experiences Summarized from Practice'
tags = ["Code Quality","Technical Management"]
+++


Experienced programmers know that Code Review can greatly improve code quality, enforce coding standards, and enhance team capabilities. As the famous technical expert "Haoel" (Left-Eared Mouse) once said:

> I believe there is no need to stay in a company that doesn't do Code Review (because a company that doesn't do Code Review definitely doesn't respect technology)
>
> — From "The Programmer's Level-Up Guide - Cultivation"

Many tech companies abroad, such as Google and Amazon, value Code Review highly and do it exceptionally well. However, many domestic companies struggle with it, often leading to counterproductive results. Here are some common situations I've seen:

* Mutual accusations between team members during Code Review, harming team cohesion.
* Formalized Code Review that doesn't improve quality or reduce bugs but instead lowers development efficiency.
* Code Review is effective, but the process is too heavy, slowing down the team.

We are also practicing Code Review and have encountered obstacles and gathered experiences on the way. If you face similar issues, you might want to spend a little time reading this article; it might be helpful.

I won't re-list all the benefits here as everyone is familiar with them. Instead, this article focuses on several basic consensuses and principles:

1. The principle of efficiency: let machines do most of the work.
2. The timing of Code Review (Right time, right place, right people).
3. Key principles for promoting Code Review.

### The principle of efficiency: let machines do most of the work

Coding formats and styles are relatively fixed. For instance, common standards for Java include:

1. [Oracle Java SE Standard](https://www.oracle.com/technetwork/java/codeconvtoc-136057.html)
2. [Google Java Guide](https://google.github.io/styleguide/javaguide.html)
3. [Alibaba Java Manual](https://github.com/alibaba/p3c) (Commonly used domestically)

For Ruby, which I've used frequently recently, official standards include:

1. [Ruby Style Guide](https://github.com/rubocop-hq/ruby-style-guide)
2. [Airbnb Ruby Style](https://github.com/airbnb/ruby)

Standards are essentially mechanical rules that should be checked by machines (using tools like P3C, Rubocop, SonarQube). Machines are faster, more rigorous, and don't get tired. **It can even be said assertively: the essence of all automation tools is to reduce dependence on humans**, because humans are prone to uncertainty and are not suited for repetitive, deterministic tasks.

### The timing of Code Review (Right time, right place, right people)

In my experience, **the further left a Code Review is shifted, the lower the cost of modifying code and the higher the developer's willingness to change.** What does "shifting left" mean?

Let's look at the software development pipeline and what I consider the most reasonable timing for code review:

![Software Engineering Development Pipeline](https://s2.loli.net/2025/02/15/zMi5jHh12CgldIf.png)

Software Engineering Development Pipeline (Diagram)

In terms of the pipeline, some individuals perform code review only when merging into the master branch close to release (on the right). At this stage, the modification cost is very high because the code has already been tested. If the review reveals issues requiring code changes, the feature must undergo regression testing, wasting double the testing time and human resources. As the deadline approaches, developers will be less willing to refactor. If compliant-violating code is allowed due to release pressure, people lose respect for the process, and code review slowly becomes a mere formality—a deployment checklist that neither improves quality nor elevates developers but instead slows the team down.

Therefore, the best time for Code Review is after the feature branch self-testing is finished but *before* it's merged into the `develop` branch for official testing. The core of efficient code review is pursuing fast feedback: the earlier a problem is found, the lower the cost to fix it. Refer to the diagram below:

![Cost of Fix](https://s2.loli.net/2025/02/15/etc7NQbsZyHV9SX.png)

Note that after machine scanning (a trick is to add automatic style/static checks to GitLab CI—a high-frequency operation that might happen dozens or hundreds of times a day; automating this via GitLab CI avoids local execution and greatly boosts efficiency), team members only need to focus on code logic, maintainability of design, extensibility, and other areas where machines struggle. Since the code hasn't been officially submitted for testing yet, an initial rejection doesn't waste QA resources, and developers are more open to changes. This achieves both efficiency and quality.

##### Code Review must count toward development workload

A common reason teams skip code review is the feeling that it's a "waste of time." Consequently, poor code is merged, leading to frequent production issues. Developers then spend their lives frantically fixing these accidents. While it might look like features are launching faster in the short term, the overall delivery cycle is elongated when factoring in rework. Counting code review as part of the workload is a way to value long-term benefits and is a prerequisite for successful implementation. From a management perspective, things not counted as workload won't be respected, and code review will eventually be abandoned or reduced to a superficial ritual. This is a primary reason many team implementations fail.

### Key principles for promoting Code Review

To avoid endless arguments over minor details, a team must reach a consensus on principles and methods beforehand. I've seen technical staff argue incessantly over a single function implementation, with both believing they are correct. Establish these consensuses early:

##### Mutual Respect

From the author's perspective:
1. The reviewer spends time and energy reading unfamiliar code to help the author improve; the author should cooperate and make it easy.
2. Submitting high-quality code is a basic form of respect for the reviewer (submitting messy, un-tested code is extremely irresponsible).
3. Maintaining a clear commit history allows others to see changes at a glance. If code is overly complex, a face-to-face discussion with the reviewer is most efficient.

From the reviewer's perspective:
1. Practice mutual respect and empathy. Offer suggestions without subjective criticism or emotional tones.
2. Improvements must be based on facts or clear documentation, not personal preference (e.g., using `for` vs `while` to achieve the same result).
3. Focus energy on logic and design—the parts machines cannot scan—rather than nit-picking minor, scan-detectable details.

##### Building Consensus

As a team:
1. The goal is to improve project quality and avoid the cycle of fixing bugs, allowing the team to face more significant challenges.
2. Code review is a growth opportunity for both individuals and the team. Put aside unnecessary ego and accept different opinions with an open and inclusive mind.

### Summary

These are the practices and summaries from my personal and team experience with Code Review. The key is choosing a review method suitable for your team's situation. If pursuing agile development and rapid iterations, centralized reviews might not be for you—perhaps 1-on-1 pair programming would be more efficient. Every team is at a different stage, and different GitFlow processes apply. There is no "best" tool, only the "most suitable" one.
