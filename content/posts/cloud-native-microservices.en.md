+++
date = '2021-11-30T14:50:42+08:00'
draft = false
title = 'Microservice Architecture in the Cloud-Native Era'
tags = ["Cloud Native"]
+++

This sharing mainly focuses on the following four topics:

* What is Cloud Native?
* Why use Cloud-Native architecture?
* The concept of Microservices
* Technical selection for Microservices

### What is Cloud Native?

#### Cloud Computing and Cloud Native

Cloud computing is different from traditional self-built computer rooms. Cloud computing abstracts computing into infrastructure and distributes it through the network. Thanks to the infinite scaling capability of cloud computing, "cloud computing" is just like a water plant; we can get water at any time, unlimited, and pay according to our water consumption. Here are the five basic characteristics of cloud computing.

![Basic characteristics](https://s2.loli.net/2025/02/13/J2Npb3rkiwWxGFz.jpg)

Here are some current mainstream public cloud vendors:

![Mainstream public cloud vendors](https://s2.loli.net/2025/02/13/CamYIjr6suzOiwN.png)

Cloud native, as the name suggests, **is an application service designed based on cloud computing characteristics**. Thanks to the rapid development of cloud computing, cloud-native applications designed based on cloud computing characteristics have a huge lead over traditional monolithic applications in security, scalability, rapid iteration, operation and maintenance, and other aspects. Cloud native does not refer to a certain technology; it is an architectural design philosophy. Any application that conforms to this architectural design philosophy can be called a **cloud-native application**. Let's look at the CNCF official definition of cloud native:

![Definition of Cloud Native](https://s2.loli.net/2025/02/13/pdLv87A6aEMYNCl.png)

#### Development of Container Cloud Technology

![Development history of virtualization technology](https://s2.loli.net/2025/02/13/y36cj1OX5uJzheg.png)

Cloud native relies on containers as the technical foundation to be realized, but containers are not a trendy new technology. Here is the development history of container cloud technology, with several key historical milestones:

* As early as 2006, Amazon built the IaaS platform AWS based on container technology, becoming the ancestor of all cloud computing vendors. Due to its technical lead, AWS remains the leader in the cloud computing industry today.
* In 2013, the birth of Docker further lowered the threshold for using container technology. The Docker company, thinking it held the core technology of the cloud era, began to ambitiously challenge traditional cloud computing giants like RedHat and Google. However, it was unexpectedly defeated by Kubernetes, released by RedHat in collaboration with Google. The success of Kubernetes made everyone realize that container technology is not the core technology of the cloud era—**container orchestration** is. (Note: In 2020, K8S officially announced that any container that satisfies the K8S CRI interface can be orchestrated by K8S; Docker was left behind by the era).
* In 2015, following the success of Kubernetes, Google announced the establishment of the CNCF Foundation, a representative organization of the cloud-native era, dedicated to perfecting cloud-era infrastructure and helping developers build better products.

The diagram below is the CNCF landscape:

![CNCF Landscape](https://s2.loli.net/2025/02/13/I2eoGCOsxntKkP3.png)

### Why use Cloud-Native architecture?

Mainly discussed from four aspects:

* Automatic Recovery
* Service Security
* Elastic Scaling
* Rapid Release

#### Automatic Recovery

In my early career, I took over a dilapidated legacy system that had a mysterious bug: it would automatically crash every night for no apparent reason. It could be restored by simple restarting. To ensure the normal use of the business system, I always Got up in the middle of the night to restart the server. At that time, I thought: **If there were a tool that could detect a system crash and automatically restart it, I could sleep soundly**. This is the first problem cloud-native architecture aims to solve: **When an application system goes down, it can automatically recover in the shortest possible time without manual intervention to ensure system robustness**.

Besides unknown bugs, there are also strange exceptions that can cause service crashes, such as:

* Poorly written code leading to OOM.
* Insufficient resources on the server itself.
* Deadlocks, disks, network issues, etc.
* And more...

Three strategies for Kubernetes Pod application automatic recovery:

```yaml
spec: 
  restartPolicy: Always # When a container terminates and exits, always restart it; this is the default strategy.
  containers: 
  - image: nginx
    name: web 
```

* `Always`: When the container terminates and exits, always restart it; default strategy.
* `OnFailure`: Restart the container only when it exits abnormally (exit status code non-zero).
* `Never`: Never restart the container after it terminates and exits.

#### Security

In the large-scale distributed systems of microservice architecture, **safe protection and isolation mechanisms between services are established through circuit breaking**.

Cloud-native architecture guarantees system security mainly in two aspects:

* Service Isolation
* Resource Isolation

**Service Isolation**

Let's look at the secure isolation of service calls, as shown in the figure:

![Security Isolation](https://s2.loli.net/2025/02/13/2NmDYIcbqz5MhSF.png)

Suppose there is a dependency call relationship between Service A and Service B. Its processing logic is as follows:

1. If Service B crashes or goes offline abnormally, the registry will send Service B's status to Service A, which will then trigger the circuit-breaking mechanism.
2. Service A adopts a degradation strategy or stops sending requests to Service B, avoiding call chain cascades and protecting Service A's availability.
3. When Service B is brought back up, Service A receives the health check from the registry for Service B and resumes calls or removes the degradation strategy.

**Resource Isolation**

Cloud-native architecture's protection mechanism for services is also reflected in resource usage. Previously, multiple systems shared a host's resources, making it prone to the "barrel's short board" effect: as long as one system exhausted the host's resources, all other systems would be affected. Now, based on container-deployed microservices, your system in the production environment is deployed as if confined in small rooms. Pre-arranged resource settings determine the size of the room; the service can only operate within that specified size range. Even if an internal exception causes the service to consume all allocated resources, it won't affect the normal activities of the "little friends" in other rooms, thus ensuring the availability of the entire system.

Pod configuration file specifying memory requests and limits via Kubernetes:

```yaml
spec:
  containers:
  - name: memory-demo-ctr
    image: polinux/stress
    resources:
      limits:
        memory: "200Mi"		# Memory will be limited within 200 MiB
      requests:
        memory: "100Mi"		# Container will request 100 MiB of memory
```

Through service isolation and resource isolation, safety and availability are provided for cloud-native systems. This is just an introductory overview.

#### Elastic Scaling

Traditional monolithic applications are often deployed in host servers within computer rooms. Self-purchased servers struggle to cope with rapid business growth, posing several problems:

* Time cost: Purchasing servers requires filling out configuration lists, going through various processes, and waiting for logistics. This can take 1-2 weeks.
* Space cost: Significant space must be cleared for these large units.
* Other costs: 24-hour air conditioning, personnel shifts, machine maintenance, idle machines after service decommissioning, etc.

Cloud-native systems designed based on the basic characteristics of cloud computing do not have these problems. Mainstream public cloud vendors provide ECS hosts that can basically be scaled and configured as needed, and the resource usage also follows a **pay-as-you-go** model, effectively avoiding limits and waste of computing resources.

#### Rapid Release

With the perfection of cloud-native infrastructure like Kubernetes, the deployment methods of modern applications are also very different from the past. Compared to traditional inefficient downtime releases, the Rolling Update provided by cloud-native services helps us achieve the goal of upgrading systems without downtime. For companies that need to respond quickly to market demands, the ability to rapidly iterate business system functions is particularly important for gaining a competitive edge. The Kubernetes RollingUpdate strategy is used to solve the problem of zero-downtime releases:

![Downtime-free release](https://s2.loli.net/2025/02/13/OjlcINCd6TFeXBM.png)

Additionally, we can roll back a deployment to a specific version via `kubectl rollout undo` to solve the problem of rapid microservice rollback. These are the huge advantages of cloud-native architecture over traditional systems.

### The concept of Microservices

#### Theoretical Basis of Microservices

Microservices do not refer to a specific technology; it is an abstract concept. As long as all its specifications are met, it can be understood that your system has implemented microservices.

![Common concerns of microservices](https://s2.loli.net/2025/02/13/BMqtzHchxX2VnuY.png)

#### When to use Microservices?

There have always been two voices in the industry regarding when your project should introduce a microservice architecture:

* Option A: Monolith first, gradually replaced by microservice architecture as the architecture evolves.
* Option B: Microservices first, to avoid large-scale architectural refactoring later.

In fact, as early as 2015, the tech guru [Martin Fowler](https://martinfowler.com/) gave a referenceable answer in his blog post [MicroservicePremium](https://martinfowler.com/bliki/MicroservicePremium.html):

![MicroservicePremuim](https://s2.loli.net/2025/02/13/J1NDigFj7Rs36on.png)

In the early days (around 2015), the cost and threshold for using microservices were high, and production efficiency was not as good as monolithic applications. However, as the system's business complexity gradually increased, the production efficiency of monolithic applications gradually decreased. When the critical point was reached, the advantages of microservices emerged, and their production efficiency began to exceed that of monolithic applications. Therefore, in 2015, weighing costs and benefits, most people chose a **monolith first** architectural approach.

#### The Birth of Netflix OSS

As early as 2015, when the CNCF foundation was just born, the community's microservice infrastructure was very imperfect. Netflix + Pivotal, as explorers of microservice practice, **implemented microservice architecture by providing many microservice infrastructure components at the application level**. The complete solution of microservice components provided by Netflix is called Netflix OSS (Open Source Software Center).

![Netflix OSS Landscape](https://s2.loli.net/2025/02/13/3mbB2uUHp8QxPv6.png)

#### Microservices First

Martin Fowler's viewpoint in 2015 is clearly no longer applicable to the modern system architecture of 2021. In recent years, with the rapid development of CNCF, cloud-native infrastructure has gradually improved and matured, and the cost of using microservices has decreased year by year. The cost of implementing microservices has trended towards monoliths and may even be superior in the future. My personal view is that **if microservices can solve the usage and learning cost issues, they will eventually replace monolithic applications completely.**

### Technical selection for Microservices

#### Selecting a Microservice Framework

There are many microservice frameworks on the market. Most large companies currently have their own. Let's look at a few mainstream and representative ones:

* Dubbo (Alibaba)
* Spring Cloud (Netflix)
* Kubernetes (Google)

We compare the mainstream frameworks across three dimensions: basic concerns of microservices, operational architecture, and product background.

![Comparison of mainstream frameworks](https://s2.loli.net/2025/02/13/28dJ1pTMUZtkn5E.jpg)

Through horizontal comparison, we can see that both Dubbo and Spring Cloud have many disadvantages compared to Kubernetes. Compared to Alibaba's Dubbo and Netflix's Spring Cloud, Google's Kubernetes is the technical solution that provides a complete, one-stop microservice solution.

![Kubernetes Solution](https://s2.loli.net/2025/02/13/CzVH17nKamUloEN.png)

If using a house as a metaphor, the former are like unfurnished houses where you have to do your own decoration; Kubernetes is a fully decorated commodity house that solves all problems for you. Additionally, **building a Kubernetes cluster yourself is expensive, so it is recommended to use Kubernetes services provided by public cloud vendors.**

#### Microservices and Gateways

If you compare a distributed microservice system to a company, then the gateway is the company's reception. When a user wants to visit the company, they must register and verify their identity at the reception. This step is called **Gateway Authentication**. Based on the user's description of the task and the credentials they carry, the gateway leads them to the appropriate office. This step is called **Gateway Routing**. If there are too many users for one reception to handle, more windows will be opened to divert traffic; this step is called **Load Balancing at the Gateway level**. The gateway is the "front door" of microservices and is crucial.

Advanced features of a gateway:

* Gateway throttling (closing the door when there are too many people).
* Canary release (leading a small portion of users to a new office area to experience it).
* Elastic scaling.

#### Microservices and Secure Authentication

**Session Management in Early Distributed Monoliths**

Early monolithic applications used server-side stored sessionid + cookie + filter to maintain user state. **However, such stateful services had many drawbacks**, such as state loss upon service restart and difficulty in horizontal scaling. Later, people began to put the user session state in storage middleware like Redis.

**Auth-based Authentication in Microservices**

In microservice systems, the identity authentication module is extracted and handled by a separate service, usually called Auth Service. Access tokens are issued by Auth and authenticated uniformly by the gateway. This separation allow microservices to focus more on business. However, this may cause unnecessary performance loss as all requests go to Auth for verification. Is there a more light-weight solution? The answer is the very popular JWT (JSON Web Token) authentication. JWT combined with the RBAC (Role-Based Access Control) model is a mainstream lightweight authentication solution today.

JWT is highly regarded and widely used because after the Auth service issues the token, the gateway can verify its validity without needing to request the Auth service again. The token itself can even contain a small amount of user information. You can decode it on sites like [JWT.io](https://jwt.io/).

#### Microservice Operations and Monitoring

**Production Ready**

In software development, "Feature-Complete" is only a small part. What other stages are needed from finished coding to being "Production Ready"?

* Integration Testing: Accuracy, performance, and stress testing.
* Log Management: Logs must be standardized and distinguish between Info, Warn, Error, etc., to facilitate collection and monitoring.
* Monitoring and Alerting: Business indicators, application indicators, CPU, memory, disk, network IO, etc.
* Call Chain Monitoring: Visualize call relationships and performance, find bottlenecks, and quickly locate problems.
* High Availability: Backups, disaster recovery strategies, elastic mechanisms, etc.

**EFK-based Log Collection**

Kubernetes recommends using EFK (Elasticsearch + Fluentd + Kibana) to collect logs. Fluentd sends the collected logs directly to Elasticsearch, which parses them for Kibana to display in a dashboard.

**Distributed System Service Monitoring**

The mainstream microservice monitoring system is built via Kubernetes + Prometheus. Prometheus discovers Kubernetes services, Alert Manager handles monitoring and alerting via Email/SMS, and Grafana displays various metrics.

**Skywalking-based Distributed Link Tracking**

Skywalking is a non-intrusive distributed link tracking framework that can complete tracking without adding a single line of code.

### Summary

This article has covered why programmers should embrace cloud-native, the revolutionary changes it brings to traditional monolithic applications, and the working principles, architectures, and operations of microservices. In real production-grade cloud-native applications, there are even more factors to consider, such as:

* HTTPS
* Coding standards, test coverage, E2E testing
* Monitoring: Log/Trace/Metrics, business metrics
* Continuous Integration: CI/CD pipelines
* Thorough README documentation

I look forward to learning and communicating with all of you. Thank you.
