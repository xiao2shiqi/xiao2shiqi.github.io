+++
date = '2021-11-30T14:50:42+08:00'
draft = false
title = 'Microservice Architecture in the Cloud Native Era'
tags = ["Cloud Native"]
+++

This post focuses on the following four themes:

* What is Cloud Native?
* Why use a Cloud Native architecture?
* The concepts of Microservices
* Technology selection for Microservices

### What is Cloud Native?

#### Cloud Computing and Cloud Native

Cloud computing differs from traditional self-built data centers. It abstracts computing into infrastructure distributed via the network. Thanks to its infinite scalability, cloud computing is like a water utility—we can access it at any time, in unlimited quantities, and pay only for what we consume. Below are the five basic characteristics of cloud computing:

![Basic Characteristics](https://s2.loli.net/2025/02/13/J2Npb3rkiwWxGFz.jpg)

Here are the currently mainstream public cloud vendors:

![Mainstream Public Cloud Vendors](https://s2.loli.net/2025/02/13/CamYIjr6suzOiwN.png)

Cloud Native, as the name suggests, refers to **application services designed specifically to leverage cloud computing's characteristics**. Benefiting from the rapid development of cloud computing, cloud native applications have a huge lead over traditional monolithic applications in security, scalability, rapid iteration, and operations. Cloud Native is not a specific technology but an architectural design philosophy; any application meeting this philosophy can be called a **Cloud Native application**. Let's look at the official CNCF definition:

![Cloud Native Definition](https://s2.loli.net/2025/02/13/pdLv87A6aEMYNCl.png)

#### Development of Container Cloud Technology

![History of Virtualization Technology](https://s2.loli.net/2025/02/13/y36cj1OX5uJzheg.png)

Cloud Native relies on containers as its technical foundation. However, containerization is not a new technology. Here is a brief history with key milestones:

* As early as 2006, Amazon built the AWS IaaS platform based on container technology, becoming the pioneer of all cloud vendors. Due to its early lead, AWS remains the leader today.
* In 2013, the birth of Docker further lowered the barrier for container usage. Docker, believing it held the core technology of the cloud era, ambitiously challenged traditional giants like RedHat and Google. However, it was eventually overtaken by Kubernetes (released by RedHat and Google). Kubernetes' success proved that **container orchestration**, not just the containers themselves, is the core technology. (Note: In 2020, K8S officially announced that any container meeting its CRI interface can be orchestrated, effectively leaving Docker behind).
* In 2015, following Kubernetes' success, Google announced the formation of the CNCF Foundation—the representative organization of the cloud native era, dedicated to perfecting infrastructure and helping developers build better products.

Below is the CNCF Landscape:

![CNCF Landscape](https://s2.loli.net/2025/02/13/I2eoGCOsxntKkP3.png)

### Why use a Cloud Native Architecture?

Let's discuss this through four aspects:

* Automatic Recovery
* Service Security
* Elastic Expansion
* Fast Release

#### Automatic Recovery

Early in my career, I inherited a poorly maintained legacy system. It had a mysterious bug where it would crash every night for no apparent reason, yet a simple restart would fix it. To ensure business continuity, I often woke up in the middle of the night to restart the server. I thought: **"If only there were a tool that could detect a crash and automatically restart the system, I could get a good night's sleep."** This is the first problem cloud native architecture aims to solve: **robustness through automatic recovery without human intervention**.

Beyond unknown bugs, many anomalies can crash a service:

* Poorly written code leading to OOM (Out of Memory)
* Insufficient server resources
* Deadlocks, disk issues, network failures, etc.

Kubernetes Pod automatic recovery policies:

```yaml
spec: 
  restartPolicy: Always # Always restart the container when it terminates; default policy
  containers: 
  - image: nginx
    name: web 
```

* `Always`: Always restart the container when it terminates (the default).
* `OnFailure`: Restart only if the container exits with a non-zero status code.
* `Never`: Never restart.

#### Security

In massive distributed microservice systems, **security isolation is established between services via circuit breaking**.

Cloud native security manifests in two ways:

* Service Isolation
* Resource Isolation

**Service Isolation**

Look at the isolation in service calls:

![Security Isolation](https://s2.loli.net/2025/02/13/2NmDYIcbqz5MhSF.png)

If Service A depends on Service B, the logic is:

1. If B crashes or goes offline abnormally, the Registry notifies A, which triggers its circuit breaker.
2. A adopts a fallback strategy or stops sending requests to B, preventing a chain-reaction "cascading failure" and protecting A's availability.
3. Once B is brought back up, A receives a health check update from the Registry and resumes normal calls.

**Resource Isolation**

Security also applies to resource consumption. Previously, multiple systems sharing one host's resources often suffered from the "bottleneck" effect: one system consuming all resources would crash everything on the host. Now, microservices deployed in containers are "locked in separate rooms." The pre-configured resource settings define the room's size—the service can only operate within its bounds. Even if a bug causes a resource spike, it won't affect neighbors in other rooms, ensuring overall system availability.

Kubernetes Pod configuration for memory requests and limits:

```yaml
spec:
  containers:
  - name: memory-demo-ctr
    image: polinux/stress
    resources:
      limits:
        memory: "200Mi"		# Memory limited to 200 MiB
      requests:
        memory: "100Mi"		# Container requests 100 MiB
```

Through service and resource isolation, cloud native systems gain security and availability. This is just an introduction; there is much more to explore.

#### Elastic Expansion

Traditional monolithic apps on physical servers struggle with rapid growth:

* **Time Cost**: Purchasing servers requires paperwork, approval, logistics, and setup—easily taking 1-2 weeks.
* **Space Cost**: Massive physical space is required for hardware.
* **Other Costs**: 24/7 air conditioning, staff rotations, machine maintenance, and difficulty reselling idle hardware.

In a cloud native system designed around cloud computing, these issues vanish. Mainstream public clouds offer ECS instances that can expand or shrink on demand, with **pay-as-you-go** pricing to avoid resource waste.

![ECS Elastic Scaling](https://s2.loli.net/2025/02/13/62wTPgYelButsAo.png)

#### Fast Release

With modern cloud native infrastructure like Kubernetes, application deployment is vastly different. Compared to traditional, inefficient downtime releases, "Rolling Updates" allow for zero-downtime upgrades. For companies needing to respond quickly to market demands, rapid iteration is a vital competitive edge.

![Zero-downtime Release](https://s2.loli.net/2025/02/13/OjlcINCd6TFeXBM.png)

Additionally, we can use `kubectl rollout undo` to roll back to a specific version, solving the problem of fast recovery from bad releases. This represents a massive advantage over traditional systems. As programmers, **it is worth investing time to learn the next generation of mainstream architecture**, which will provide significant technical leverage.

### Microservice Concepts

#### Technical Foundation

Microservices is an abstract concept rather than a specific technology. If your system meets all the standards, it can be considered a microservice implementation.

![Microservice Common Concerns](https://s2.loli.net/2025/02/13/BMqtzHchxX2VnuY.png)

#### When to use Microservices?

There are two schools of thought on when to adopt microservices:

* **Option A, Monolith First**: Gradually evolve into microservices as the architecture matures.
* **Option B, Microservice First**: Avoid large-scale refactoring later.

Technically, as early as 2015, [Martin Fowler](https://martinfowler.com/) provided a definitive answer in his blog post [Microservice Premium](https://martinfowler.com/bliki/MicroservicePremium.html):

![Microservice Premium](https://s2.loli.net/2025/02/13/J1NDigFj7Rs36on.png)

In 2015, microservices had high adoption costs and barriers; production efficiency was lower than for monoliths until a system reached a certain level of complexity. Once that "critical point" was hit, microservices became more efficient. Thus, in 2015, most chose **Monolith First**.

#### Birth of Netflix OSS

When the CNCF Foundation was born in 2015, the microservice infrastructure was immature. Netflix and Pivotal, as pioneers, **implemented microservice architecture through application-level basic components**. This suite of solutions is known as Netflix OSS (Open Source Software Center).

![Netflix OSS Landscape](https://s2.loli.net/2025/02/13/3mbB2uUHp8QxPv6.png)

#### Microservice First

Martin Fowler's 2015 view is less applicable to modern 2021 systems. With the rapid growth of CNCF, cloud native infrastructure has matured, lowering the cost of using microservices to the level of monoliths—or even lower. In my view, **if microservices can solve the cost of learning and use, they will eventually replace monolithic apps entirely**. From a long-term perspective, new projects should prioritize microservice architecture to ensure efficiency, scalability, and avoid massive future refactoring.

### Technology Selection for Microservices

#### Frameowork Choices

Many microservice frameworks exist. Most large companies have their own, but let's look at the most representative ones:

* Dubbo (Alibaba)
* Spring Cloud (Netflix)
* Kubernetes (Google)

Let's compare them across three dimensions: basic concerns, O&M (Operation & Maintenance), and product background:

![Framework Comparison](https://s2.loli.net/2025/02/13/28dJ1pTMUZtkn5E.jpg)

Through horizontal comparison, we can see that both Dubbo and Spring Cloud have many disadvantages compared to Kubernetes. Unlike Alibaba's Dubbo or Netflix's Spring Cloud, Google's Kubernetes provides a complete, one-stop microservice solution.

![Kubernetes Solution](https://s2.loli.net/2025/02/13/CzVH17nKamUloEN.png)

If using housing as an analogy: the former are like "shell" apartments you must renovate yourself; Kubernetes is a "fully-furnished" home—every problem solved, just move in. Furthermore, **local Kubernetes setup is costly; it's recommended to use managed K8S services from public cloud providers**.

#### Microservices and Gateways

If a distributed microservice system is a company, the gateway is the front desk. Visitors must register and prove their identity (and maybe take a temperature check these days). This step is **Gateway Authentication**. Based on the visitor's mission, the front desk guides them to the correct office—**Gateway Routing**. If there are too many visitors, more windows are opened—**Gateway-level Load Balancing**. The gateway is the front door of your microservices and is absolutely critical.

Common gateway workflows:

<img src="https://s2.loli.net/2025/02/13/iyBYwzuOnGrQehV.png" alt="Gateway Workflow" style="zoom:67%;" />

Beyond authentication, routing, and load balancing, gateways enable advanced features:

* Rate Limiting (too many people; close the door or make them queue)
* Canary Releases (guides a subset of users to experience new, yet-to-be-fully-released workspaces)
* Elastic Scaling

The gateway is the source of a microservice's elastic scaling capability. Since development costs for gateways aren't prohibitively high, many standalone products exist:

![Mainstream Gateway Comparison](https://s2.loli.net/2025/02/13/Pr74txIjleFc8EB.png)

#### Microservices and Security Authentication

**Session Management in Early Distributed Monoliths**

Early monolithic apps managed session state via server-side Session IDs, Cookies, and filters. **However, stateful services have many drawbacks**, such as losing user state on restart and difficulty scaling horizontally. Later, monoliths began storing session state in middleware like Redis to solve these issues.

![Redis Stored Sessions](https://s2.loli.net/2025/02/13/sG9RT8uq5QBbyOv.png)

**Auth-based Schemes in Microservices**

In microservices, identity authentication is extracted into a standalone "Auth Service." Access tokens are issued by Auth and verified by the gateway. Separation of concerns allows microservices to focus on business logic.

![Gateway Accessing Auth Service](https://s2.loli.net/2025/02/13/VqhDuYxw5C9Bjep.jpg)

However, sending every request to the Auth Service for verification creates pressure and performance loss. Most applications don't need such a heavy security level. Is there a lightweight technology where tokens can be self-validated? Yes: JWT (JSON Web Token). JWT combined with the RBAC role model is a very popular lightweight solution.

![RBAC+JWT](https://s2.loli.net/2025/02/13/2O38UN7gAGZhmQv.jpg)

JWT is highly regarded because once issued, the gateway can verify its legitimacy independently, reducing requests to the Auth Service and improving performance. It can also self-contain a small amount of user info. You can use [JWT.IO](https://jwt.io/) to decode information from a JWT string:

![JWT Info](https://s2.loli.net/2025/02/13/UO8Tj2Gw34ynVqL.jpg)

JWT isn't perfect; here are its pros and cons:

| Pros | Cons |
| :--- | :--- |
| Compact and lightweight | Once issued, cannot be manually revoked—it must expire |
| Relieves Auth Service pressure; simplifies implementation | Larger payload means higher transmission overhead |

**Summary**

The RBAC role model + JWT scheme is the mainstream security architecture for microservices today, meeting most needs and serving as a best practice in enterprise production.

#### Microservice O&M Monitoring

**Production Ready**

Finally, let's talk about operations. We know being "Feature-Complete" is only a small part of development. What else is needed to be **Production Ready**?

![Production Ready](https://s2.loli.net/2025/02/13/SVTov4pYHkL1NKQ.jpg)

* **Integration Testing**: Accuracy, performance, and pressure testing.
* **Log Management**: Standardized logs across levels (Info, Warning, Error) for easy collection, monitoring, and troubleshooting.
* **Monitoring & Alerts**: Business, application, and infra metrics (CPU, Memory, Disk, Network IO).
* **Distributed Tracing**: Visualizes relationships and performance, identifying bottlenecks and locating issues.
* **High Availability**: Dual-machine backup, Master-Slave, multi-active redundancy, disaster recovery, and elastic mechanisms.

Only when we ensure these requirements are met can we go to production and deliver value.

**EFK Log Collection**

Microservice architectures on containers cannot rely on SSH to fetch logs. A unified collection mechanism is required. Kubernetes recommends EFK (Elasticsearch + Fluentd + Kibana):

![EFK in K8S](https://s2.loli.net/2025/02/13/9XwiUAD5zyRCuBQ.jpg)

1. Fluentd sends collected logs to Elasticsearch (with Kafka as an optional buffer).
2. Elasticsearch parses and filters logs.
3. Kibana provides the dashboard for querying.

**Prometheus Monitoring**

The mainstream monitoring ecosystem for microservices uses Kubernetes + Prometheus:

![K8S and Prometheus](https://s2.loli.net/2025/02/13/lyqLi5VjSZCeAa4.jpg)

1. Prometheus discovers K8S services.
2. Alert Manager handles email/SMS alerts.
3. Grafana visualizes the metrics.

**SkyWalking Distributed Tracing**

SkyWalking is a non-intrusive tracing framework that works without code changes. It became an Apache Top-Level Project in 2019. Its author, Wu Sheng, became the first Chinese director of the Apache Software Foundation.

![SkyWalking Principle](https://s2.loli.net/2025/02/13/tcLm45wlEx6HKTV.jpg)

SkyWalking trace visualization:

![SkyWalking Trace Visualization](https://s2.loli.net/2025/02/13/EX36VSi8zRpIF2P.jpg)

### Summary

This post detailed the history of Cloud Native and why programmers should embrace it. We discussed the disruptive benefits cloud-native systems bring over traditional monoliths, as well as principles for microservice layout and O&M. In real production-grade apps, much more must be considered:

* HTTPS
* Coding standards, test coverage, E2E testing
* Monitoring: Log/Trace/Metrics and business metrics
* Continuous Integration: CI/CD pipelines
* Comprehensive README documentation

I look forward to learning and communicating more with all of you. Thank you.

**References:**

* [Production-Ready vs Feature-Complete: What’s the Difference?](https://www.verypossible.com/insights/production-ready-vs-feature-complete-whats-the-difference)
* [ELK, EFK, Prometheus, SkyWalking, K8s Combinations](https://m.tqwba.com/x_d/jishu/427732.html)
* [Spring Boot and Kubernetes Cloud Native Microservice Practices](https://time.geekbang.org/course/intro/100031401?tab=catalog)
