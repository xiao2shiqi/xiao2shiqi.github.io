+++
date = '2020-08-03T15:00:08+08:00'
draft = false
title = 'Practical Lessons from a Technical Leader'
tags = ["Code Quality","Technical Management"]
+++
### Preface

I have personally gone through a lot of mental journeys transitioning from a programmer to a Tech Leader. Currently, I lead a technical team of about a dozen people (controlling the team size mainly follows the [Two Pizza Rule](https://wiki.mbalib.com/wiki/两个披萨原则) proposed by Amazon CEO Jeff Bezos). I remember when I first started leading a team, I was very resistant because I always felt that managing too many "chores" took up a lot of my coding time. Even now, as the leader of a dozen-person team, I still have a preference for technology. In my spare time, I still find time to write code or solve problems on LeetCode. During my time in management, I have read many books, faced many pitfalls, and summarized a lot of experience. Many programmers surely stumble onto the path of a Tech Leader, so I want to write an article to share with you, hoping it helps those in need. The outline is as follows:

* What comprehensive abilities does a technical manager need? How can one possess Leadership in a team?
* What are the transitions from being an engineer to a team Leader?
* How to improve the work efficiency of a technical team?
* How to increase team cohesion?
* Communication skills?
* Self-perception and growth of a manager.

### What comprehensive abilities does a technical manager need? How can one possess Leadership in a team?

When speaking of managing a technical team, the objects of management are naturally programmers. What kind of group are programmers? Most programmers are "smart and proud."

For example, this viral joke about how to correctly report a bug to a programmer:

![image-20250215150209416](https://s2.loli.net/2025/02/15/VOiU8bKTnMNQRYE.png)

A Tech Leader has high requirements for personal comprehensive qualities (managers with good technical skills have a certain advantage in leading a technical team). First, let's talk about the important comprehensive abilities I think a Tech Leader needs:

* Technical ability and basic knowledge (understanding the principles behind technical phenomena).
* Communication and expression skills (logic, empathy, emotional control).
* Business abstraction ability (architecture and evolution).

A Tech Leader must see through the essence of technology because their daily work often includes technical selection, technical solution reviews, code reviews, and creating a technical atmosphere. If the manager is not from a technical background, they may not be able to establish consensus with the technical team, lead to extremely high communication costs, and eventually turn the team into a very inefficient organization where people are just going through the motions. So how can one possess these abilities and have Leadership in a technical team? Personally, I summarize the following points:

* Master basic technology and understand the principles behind it (tall buildings rise from the ground; no matter how popular a framework or technology is, stripping away its fancy exterior leaves principles of operating systems, networking, and data structures).
* Know the details and always be coding (without being familiar with the code, you cannot propose truly practical solutions, cannot perceive where the technical team's pain points are, and thus cannot improve the team's efficiency).
* Continuous learning and bringing new knowledge and understanding to the team (the Tech Leader is the terminator of the team's technical problems; there's no passing them up, so don't become the ceiling of the technical team).
* Have a sincere attitude of helping everyone (helping everyone grow and improve efficiency eventually improves the organization's efficiency, achieving a win-win situation).

After summarizing the above experiences and methodologies, we must think about the form in which a manager's goals or work results are manifested.

![image-20250215150231399](https://s2.loli.net/2025/02/15/MYnKyEeCq8cpQdB.png)

In general, a manager's goals and work results are mainly reflected in two aspects:

* **Doing things**: Cost, efficiency, quality.
* **Leading people**: Talent, echelon, growth.

The above directions are too abstract. In fact, a manager spends much of their time on choices and permissions, mainly in the following areas:

* Selecting the plan that maximizes output under limited resources.
* Making technical decisions that fit the current environment to help the company's products succeed.
* Continuously optimizing and improving production efficiency and quality with methods and tools.

![image-20250215150256073](https://s2.loli.net/2025/02/15/1iZfDGKdbJczNPw.png)

Here is a practical example:

1. For Company A in its startup phase without stable market or customers, technical managers' decisions should lean towards cost + efficiency. For example, the technical team leans towards full-stack types, the workflow is agile, and features are delivered quickly to get user and market feedback for upgrading and iterating products.
2. For Company B in its maturity phase with fixed market and customers and no new growth in the industry, the competition is about efficiency + quality. The technical team leans towards expert types, focusing on product quality and customer experience to form industry reputation and user stickiness.

### What are the transitions from being an engineer to a team Leader?

The changes are quite significant, leading to a lot of discomfort when people first start managing a team. I summarize them as follows:

Let's look at an engineer's work perspective:

* How do I do this function?
* Once I finish writing this requirement, my work for today is done.
* Spare time is only spent on technology-related content.
* What work has the leader assigned to me today?

As a Tech Leader's work perspective:

* What should we do at this stage?
* Where will the team develop in the future? What if team growth is below expectation? How can we meet the company's performance targets this year?
* Besides technology, I need skills in communication, judgment, organization, coordination, and identifying directions.
* Planning work goals for Q1, decomposing them to team members to implement, ensuring the work content matches each team member's ability.

Seeing this, you might realize that unlike the "certainty" of an engineer's work, most of a manager's work is "uncertain," almost endless, and lacks a clear time to mark a "completed" state. This is a huge challenge for engineers used to "certainty" thinking.

Personally, I use a common metaphor: my feeling back when I was coding was that "one person eats and the whole family is full"—relaxed and free. Now, the feeling is like being both a father (doing things) and a mother (leading people), with elders above (superiors) and children below (the team). The pressure is immense!!

### How to improve team work efficiency

Everyone talks about efficiency, but measuring efficiency in the software industry is difficult. Overall, the improvement of work efficiency is actually a combination of "things + people." Let's talk about things first, then people.

From the perspective of "things," let's talk about the conditions for making team development work efficient:

* Provide high-performance computers for employees (to do a good job, one must first sharpen one's tools; talking about efficiency without the right tools is nonsense).
* Is the workflow smooth? (Is the Git server slow? Do you have to write forms and follow a process to apply for code merging? Don't talk about efficiency if there's too much formalism).
* Are automation tools complete? (Can code be merged without automatic scanning or testing? Then there will be an endless cycle of production bugs and fixes).

The above emphasizes tools and processes. Development efficiency and the developer experience are crucial to team efficiency. A smooth workflow allows developers to stay in a "flow state" and produce high-quality functions and code without being frequently interrupted by slow computers or broken processes that kill motivation. Now, let's talk about **improve efficiency from the perspective of people**.

Programmers are essentially knowledge workers. Management guru Peter Drucker said: **"It is impossible to conduct close supervision of knowledge workers."** Therefore, I prefer to provide a proactive, self-driven work atmosphere for the team, letting them naturally form a high-performance team.

Every team has slackers. Managers should not be quick to judge them but instead see if they haven't perceived the employee's psychological needs. Two traits of high-output employees are:

* Ability (professional knowledge, technical ability).
* Willingness (team culture, values, preferred atmosphere).

We often find that the same employee has different outputs in different environments. So when encountering a slacker, don't just look for problems in the employee; think about whether the people, things, environment, work methods, or values around them are the problem. After all, there's a saying: **"Oranges grown south of the Huai River are sweet; those grown north are bitter."**

##### External Incentives

Besides the team and individuals, you can find external reasons to continuously motivate the team. These can be understood as external incentives, mainly including:

* A sense of security and achievement (stable work environment, completing hard challenges, timely BIA feedback).
* Learning and growth environment (working with excellent people, perceiving personal growth).
* Regular communication with managers (making employees feel valued, collecting their suggestions, and making adjustments).

##### Self-drive and Cohesion

Many companies expect employees to have an "Owner" spirit. But if you want the team to maintain enough self-drive, a manager should consider if they have provided:

* Autonomy (freedom in work content, methods, time, and location).
* Growth (clear goals, challenging content, using their strengths).
* Meaning and mission (common goals, vision, values).
* Trust and delegation (facing challenges together, team bonding activities).

### Communication Skills

To explain the importance of communication simply, let's look at the story of the "Tower of Babel" from the Bible:

In Genesis Chapter 11, people built a tower to reach heaven. To stop them, God made them speak different languages so they couldn't communicate. Because they couldn't communicate, they couldn't reach a consensus, became suspicious of each other, fought internally, and couldn't unite. The plan failed, and humans scattered.

In summary, if people are unwilling or unable to communicate, it's easy to have disagreements and misunderstandings, leading to division and failure. Managers need to convey many things through communication to reach a consensus on direction, unite the team, and achieve the company's goals.

So, what can good communication bring?

* The manager's overall perception and judgment of the team improve.
* Trust and rapport are established with team members (trust requires full communication; the higher the trust, the lower the communication cost).
* High-quality communication helps the manager build and accumulate influence in the team.

Since many programmers might not be good at communication, they may need some principles and guidance. Here are 3 tips for communication:

* Recognize individual differences (everyone's living environment is different; use different communication styles for different roles).
* Communicate based on goals (be clear about the intent and purpose of communication to reduce unnecessary misunderstandings and avoid emotional confrontation).
* Use "I" for feedback (instead of "Do you mean...", try "Let me see if I understand correctly...").

The core of communication skills is learning to listen. For those who haven't mastered communication skills, I recommend the 3F Listening tool:

![image-20250215150351947](https://s2.loli.net/2025/02/15/tZz5OlsMoAa7Jwb.png)

##### Emotion Control

Talking about communication, we must talk about emotional control. Why should managers avoid being emotional and learn to control them? Let's look at the principle: emotions often steer communication away from the issue itself into emotional confrontation. Our cerebral cortex prioritizes processing instinctive emotions—such as anger, fear, and hunger—over rational ones. People overwhelmed by instinctive emotions often lose rationality. So during communication, always:

* Control your emotions.
* Stay rational.

Text can be dry, so let's use an iceberg chart to understand the principle:

![image-20250215150418631](https://s2.loli.net/2025/02/15/vQ8TOgGZhrnsHkN.png)

After understanding emotional control, we often encounter cross-departmental or cross-team communication, where "departmental walls" often exist. You often can't appeal to a common superior because there may not be one, and you can't influence each other. In this case, you can reach consensus through:

* **Personality**: A good reputation and integrity make it easier for others to trust and be influenced by you.
* **Past Performance**: Sucessfully completing similar tasks before serves as a success case, making it easier for others to believe you.
* **Influence**: Being a well-known industry figure or a recognized expert in the team brings the power of authority.
* **Logic**: Logical consistency in your content increases persuasiveness.
* **Passion and Vision**: Carrying a grand ideal with a sense of mission and passion makes it easier to gain help and recognition (refer to the success case of Smartisan).
* **Reciprocity**: Understand the other party's needs; the purpose of communication is to satisfy both parties' needs.

After communication skills, let's look at the common pitfalls in daily communication:

* Labeling people, attacking the person rather than the issue (e.g., "Why are you so stupid? You can't even do this small thing").
* Failing to manage emotions, letting negative emotions affect the team.
* No communication loop, assuming a message or email was received once sent.

Those familiar with computer networking know the TCP and UDP protocols. Communication with or without a loop corresponds to TCP (reliable transmission) or UDP (unreliable). I suggest using the "TCP protocol" as much as possible in communication.

### Self-perception and Growth of a Manager

Why do managers need to grow faster than the team? Because **the manager is the team's ceiling; if you don't grow, the team won't grow.** Where should a manager's self-perception be reflected?

* **Perception**: A manager's value is reflected in the team's performance; don't fight the team for credit.
* **Mindset**: Attribute failure to yourself and credit to others. Mistakes are the manager's fault; successes are the team's effort.
* **Responsibility**: Don't evade responsibility. Even for objective reasons, reflect and review to avoid them rather than pushing responsibility outward.

If you can do these three things, I believe you are already an excellent manager. So how do you maintain stable and efficient growth? My personal secret is to manage your **energy**. Everyone has similar amounts of time, especially managers in their thirties with families (like me) who have very little spare time. To win the competition, you need enough time and health. How do you get them? The answer is energy management, which I summarize in several aspects:

* Exercise (regular daily exercise keeps you energized and focused).
* Diet (healthy diet, small but frequent meals).
* Sleep (early to bed, early to rise; no staying up late).
* Health (regular checks, avoid sitting for too long).
* Emotion (relaxing, gratitude, good mood).

After perception and energy management, some may wonder: what is the goal we continuously strive for? With these two, it's like having a high-performance car on a highway, but where are you driving to? This varies for everyone. For me, coming from a tech background, I still love technology. Transitioning to management was more about training my soft skills. I have 2 goals for continuous effort:

* **Soft skill improvement**: Product thinking, project planning, leading teams, leading people, communication, execution.
* **Hard skill improvement**: Architecture, design, algorithms, networking, operating systems, programming languages.

These represent only my personal goals, which might be the goals of many Tech Leaders. There is a misunderstanding that managers don't need to do specific execution work. At least for technical management, this doesn't work. I believe a technical manager **should always write code because they can't make effective decisions without knowing technical details.** It's also dangerous for a manager to lose touch with technology because the market demand for purely managers is not as high as for engineers. A manager's value is often attached to the company, and much of their business knowledge is not transferable. If a manager abandons technology, they are "disabling their own skills" and putting themselves in an awkward spot where they might not even be able to go back to being an engineer if they find they are not suited for management.

### Summary

I've babbled for 5,000 words. The summary will be simpler. I have two suggestions for engineers, managers, or those on the road to management:

- For yourself, whether doing technology or management isn't important; finding your greatest value is.
- Don't be limited by the paths others have walked or by your profession; no one can define your development.

The "officialdom" mindset is still serious in China; many think management means being an official. But this doesn't exist in the software industry. Most internet companies favor flat management. Managers are not fundamentally different in their work; their work is often more about "chores" (from an engineer's perspective). If you do management with that mindset, your starting point is wrong. I'd advise against it because it will likely lead to failure. A manager needs an altruistic, humble, and open mindset, genuinely willing to help the team succeed and eventually realize themselves by achieving others. I've said a lot about technical management; the rules are simple. Whether you can walk the management path well depends on "practicing on things" (事上练). Only the principles you realize yourself can truly be used by you.

References:

1. Peter Drucker - *The Effective Executive* https://book.douban.com/subject/1322025/
2. Jian-guo Liu - *The Path of Technical Management* https://book.douban.com/subject/33463986/
3. Geekbang - *Technical Management in Practice* https://time.geekbang.org/column/intro/113
