+++
date = '2020-09-14T14:41:43+08:00'
draft = false
title = 'Microservice Design Principles Based on Spring Cloud'
tags = ["Java", "Cloud Native"]
+++

In recent years, microservices have become very popular, and everyone is building them. If you don't know something about microservice-related technologies, it's almost embarrassing to greet your peers. I've seen many people around me fall into various pitfalls with microservices. I've been involved with microservices since 2016 and have architectural experience in multiple large-scale enterprise distributed systems. Therefore, I decided to share a session on microservices. However, microservices and the associated distributed computing are extremely complex and cannot be fully explained in a single article. This post aims to introduce you to the basic concepts and usage from a beginner's perspective. If you're interested, you can further your studies by consulting relevant literature and technical books.

This sharing is divided into three parts, with the following outline:

* Microservice Concepts and Principles (Theory)
* How Spring Cloud Implements Microservices at Low Cost (Implementation)
* Architecture Solutions for Large-Scale projects using Spring Cloud (Real Case Study)

### Microservice Concepts and Principles

##### What are Microservices?

A simple example: For those of you who follow military news, you know that while an aircraft carrier is powerful, its weakness is obvious—its defensive capabilities are poor. A single aircraft carrier rarely operates alone; usually, the aircraft carrier strike group is the primary military force. You can think of a single carrier as a monolithic application (poor defense, limited maneuverability) and the strike group (complex coordination, high maintenance cost) as microservices.

A simple summary of characteristics:

* **Monolithic Application**: Simple, fragile (if one module fails, the entire system becomes unavailable), low combat power, low maintenance cost.
* **Microservice Architecture**: Complex, robust (if one module fails, it doesn't affect the overall availability of the system), high combat power, high maintenance cost.

Most developers have experienced or developed monolithic applications, whether traditional SSM or modern Spring Boot/Rails; they are all monoliths. What are the downsides of the monolithic applications that have accompanied us for so long? What problems did we face that led us to abandon monoliths in favor of microservice architecture? I summarize the main issues as follows:

- **High Deployment Cost** (Whether you change 1 line or 10 lines of code, you must do a full deployment).
- **High Impact and Risk, High Testing Cost** (The cost remains high regardless of how small the code change is).
- **Low Deployment Frequency** due to high cost and risk (Failure to meet rapid customer delivery needs).

Of course, there are other issues like the inability to support rapid expansion, elastic scaling, and inability to adapt to cloud environment characteristics, but we won't detail them all. These are the problems microservice architecture aims to solve. We'll discuss how they are solved later.

##### What Problems are Solved, and What New Problems are Introduced?

First, let's see what microservices can bring us. Characteristics of microservice architecture:

-   **Specific Service Releases**: Small impact, low risk, low cost.
-   **Frequent Version Releases**: Fast delivery of requirements.
-   **Low-Cost Expansion and Elastic Scaling**: Adapted to cloud environments.

We know a simple philosophy: nothing is perfect; everything has two sides. While microservices solve the problems of rapid response and elastic scaling, what new problems do they introduce? I summarize them as follows:

-   **Complexity of Distributed Systems**.
-   **High Cost of Deployment, Testing, and Monitoring**.
-   **Distributed Transactions and CAP Theorem related issues**.

Applications shift from a single monolith to tens or hundreds of different projects, creating issues like inter-service dependencies, service decomposition, internal interface standards, data transmission, and more. Service decomposition, in particular, requires the team to be familiar with business processes and understand trade-offs. You must ensure that the granularity of decomposition follows the principles of "High Cohesion, Low Coupling" while balancing business growth, corporate vision, and team cooperation.

For distributed systems, deployment, testing, and monitoring require significant middleware support, and the middleware itself needs maintenance. Transaction issues that were simple in a monolith become complex in a distributed environment. Whether to solve distributed transactions with a simple retry + compensation mechanism or a strong consistency method like the Two-Phase Commit (2PC) protocol depends on familiarity with business scenarios and repeated weightings. Similar weightings apply to the CAP model. In short, microservices demand a higher overall technical skill level from the team.

##### What Principles Should Microservices Follow?

As the saying goes: "Before the soldiers move, the fodder must go first." Building microservices requires long-term planning. It's not like writing a CMS where you build database tables and start working; that will likely lead to failure. Before a microservice transformation, an architect must plan. We divide this into three steps: The Preliminary Phase, the Design Phase, and the Technical Phase.

**Preliminary Phase**:
-   Communicate fully with all parties to ensure alignment with customer and organizational needs and gain approval.
-   Communicate with the team (devs/testers/ops) to ensure they understand and are actively involved.
-   Communicate with business departments to specify version plans and launch timelines.

**Design Phase**: Referring to Sam Newman's book [“Building Microservices”](https://book.douban.com/subject/26772677/), a single microservice must meet basic requirements:
-   Standard RESTful interfaces (based on HTTP and JSON).
-   Independent deployment and avoidance of shared databases (prevents database issues from affecting the entire distributed system).
-   High business cohesion and reduced dependencies (avoiding services that are too large or too small).

**Technical Phase**:
A massive distributed system requires strong infrastructure support. What infrastructure does it involve?
-   **CI/CD and Automation** (A distributed system is nearly impossible to deploy manually).
-   **Virtualization Technology** (Ensuring environment isolation; currently, the industry standard is using Docker containers).
-   **Log Aggregation and Full Link Monitoring** (High observability for analyzing and diagnosing issues).

When is your team NOT suitable for microservices?
1. The development team lacks autonomy and is heavily restricted by the organization (Ref: [Conway's Law](https://en.wikipedia.org/wiki/Conway%27s_law)).
2. The team is unfamiliar with the business and cannot identify service boundaries for reasonable decomposition (Ref: [Domain-Driven Design (DDD)](https://en.wikipedia.org/wiki/Domain-driven_design)).

Microservice design is actually an old idea that became popular because virtualization technology allows it to be implemented at a low cost. The essence of microservices—automation, decentralization, independence—is deep. When choosing technologies or solutions, try to understand the technology and its origin in relation to your business characteristics.

### How Microservices are Implemented at Low Cost?

Why is Spring Cloud the most popular microservice framework in China? What out-of-the-box components does it offer? Overview:

* Spring Boot for service applications
* Spring Cloud Config for centralized configuration
* Spring Cloud Eureka for service discovery
* Spring Cloud Hystrix for circuit breaking
* Spring Cloud Zuul for service gateway
* Spring Cloud OAuth 2 for service protection
* Spring Cloud Stream for message-driven integration
* Distributed full-link tracing
* Microservice deployment

Recommended Reference: [Spring Cloud Documentation](https://www.springcloud.cc)

##### Spring Boot: The Foundation of Microservices

Spring Boot is the ideal framework for building microservices, primarily because it can package services into single executable JAR files. Spring Actuator, which exposes service health information, is also a cornerstone. Why?

Let's look at 4 important principles of building microservices:
* Services should be independent and independently deployable.
* Configuration should be read from a central source (Config Center).
* The architecture should be transparent to the client.
* Services must communicate their health status.

Microservices have pros and cons, and not all applications are suitable. An architect must:
* **Decompose Business Problems**: Describe the business problem, note verbs, and look for data cohesion.
* **Establish Service Granularity**: Refactor large services into smaller ones, focusing on interaction and evolving responsibilities.
* **Define Service Interfaces**: Embrace REST concepts, use URIs to convey intent, and use HTTP status codes for results.

Characteristics of **Bad Microservices**:
* **Too Coarse-Grained**: A service takes on too many responsibilities, manages data across too many tables, and has too many test cases.
* **Too Fine-Grained**: Services are heavily dependent on each other, and there is no internal logic.

When NOT to use microservices?
* **Unwillingness to Invest** (Requires high maturity in ops, scale, and handling complexity).
* **High Cost** of managing and monitoring scattered servers.
* **Small Applications** are not suitable; they are too expensive.
* **Data Transactions** (Distributed systems handle transactions with great difficulty).

##### Spring Cloud Config: Configuration Service

Spring Config is a lightweight implementation of a configuration center provided by Spring, based on Git storage. Many users in China recommend Alibaba's open-source [Nacos](https://github.com/alibaba/nacos) (which integrates both configuration and registration centers) as a very good alternative.

![image-20250215144612896](https://s2.loli.net/2025/02/15/dov2lQfjWben8Br.png)

Principles for managing configuration centers in microservices:
* **Separation**: Disconnect application config from actual deployment code.
* **Centralization**: Consolidate configuration into a small number of repositories.
* **Stability**: Ensure high availability of the config center.

Core features of Spring Config:
* Allows use of environment-specific values.
* Uses Spring Profiles to distinguish environment values.
* Supports file-based or Git-based property storage.
* Allows symmetric and asymmetric encryption.

##### Spring Cloud Eureka: Service Discovery

Service discovery is a crucial concept in microservice architecture, also known as a **Registry**. **It plays a role similar to a real estate agent—both buying and selling houses must go through them.** It's the mandatory path for any microservice to go online or offline. The registry controls the fate of microservices, making decisions to remove, offline, or restore services based on CAP strategies and health checks.

![image-20250215144658949](https://s2.loli.net/2025/02/15/u4PvJYFnhRiOrC9.png)

Core functions:
* **Horizontal Scaling**: Quickly scales the number of service instances (though this partially overlaps with K8s features).
* **Abstraction of Physical Location**: Microservices usually run in Docker containers with dynamic IPs; they can only be found via the registry.
* **Enhanced Resilience and Auto-scaling**.
* **Information Sharing and Health Detection**.

Basic requirements for a registry implementation:
* **High Availability**: Shared registration info (cluster deployment); the registry going down must not take down the entire cluster.
* **Load Balancing**: Dynamic load balancing for inter-service requests.
* **Resilience**: Client-side caching of service information.
* **Fault Tolerance and Health Checks**: Automatic removal of failed services without manual intervention.

Features of Spring Eureka:
* Abstracts physical locations of services.
* Seamless addition and removal of services.
* Provides load balancing for inter-service calls.
* Supports 3 call mechanisms: DiscoveryClient, Ribbon-supported RestTemplate, and Netflix FeignClient.

##### Spring Cloud Hystrix: Circuit Breaker

The concept of a circuit breaker is easy to understand. For instance, when the power load in our house is too high and reaches a set threshold, the system triggers a circuit breaker (overload protection) to trip and cut power, protecting the stability of the entire circuit. The concept in microservices is the same; it's the firewall protecting microservice stability, preventing a single service crash or anomaly from causing a cascading "avalanche" effect across the system.

![image-20250215144736122](https://s2.loli.net/2025/02/15/85RyDaYJWUuwQXS.png)

Why use circuit breakers? When a service has an issue:
* It usually starts small and grows until it exhausts threads and crashes completely.
* Inter-service calls become blocked for long periods.
* Unclosed services continue to be called, causing a chain reaction.
* A single poor-performing service can quickly drag down the entire application.

Why is it important?
* Implementing circuit breakers at each node (calls to services or databases) prevents chain reactions.
* Ensures only the problematic service is affected (minimizing impact).
* Provides a flexible foundation for servers.

Key capabilities:
* **Fail Fast**.
* **Fallback** (Alternative solutions).
* **Seamless Recovery** (Periodic checks and automatic recovery).

Hystrix, developed by Netflix and practiced in production for years, is a mature and reliable implementation. It joined the Spring Cloud ecosystem and is simple to use.

Hystrix supports 4 circuit break patterns:
* **Client Load Balancing**: Detects service errors and removes the instance.
* **Circuit Breaker**: Fails fast upon timeout or when failures exceed a threshold.
* **Fallback**: Executes an alternative instead of throwing an exception (e.g., queuing, retrying later).
* **Bulkhead**: Allocates resources for remote calls to independent thread pools; issues only saturate that specific pool.

Three outcomes of "tripping":
1. Service B immediately knows Service C has a problem and fails fast without waiting.
2. Service B executes alternative code (Fallback mode).
3. Service C can check for issues and recover quickly after tripping.

![image-20250215144819633](https://s2.loli.net/2025/02/15/3Cw4PXhH98527Tz.png)

Processing principles:
* Distributed apps must be designed with resilience in mind.
* Complete service failures are easy to detect; circuit breakers provide the time window for detection.
* Poor performance can crash a cluster as inter-service calls block threads and exhaust resources.
* Hystrix supports two isolation models: THREAD and SEMAPHORE.

##### Spring Cloud Zuul: Gateway

The gateway is the entry point for the entire microservice cluster. For users, they don't need to know the address of every service; they only need the gateway address. **Think of it like this: the microservice cluster is a large company with many functional departments (services). To visit a department, you must first register at the front desk, and then the front desk guides you to the specific department (Intelligent Routing).**

Gateway standards:
* An independent service responsible for filtering and routing all service calls.
* A mediator between the service and the client, simplifying client development.

Common tasks for a gateway:
* **Static Routing**: Retrieves specific service locations from the registry.
* **Dynamic Routing**: Routes based on parameters (e.g., for grayscale releases).
* **Authentication and Authorization**: Verifies visitor identity (centralized auth so services can focus on logic).
* **Data Collection and Logging** (Collecting call counts, response times, etc.).

Zuul Gateway runtime diagram:

![image-20250215144845757](./assets/image-20250215144845757.png)

Spring Cloud Zuul features:
* Joins registered addresses from Eureka into Zuul routes.
* Easily adds prefixes like `/api` to all service routes.
* Globally customizes timeouts for Hystrix and Ribbon.
* Implements dynamic routing for A/B testing.
* Checks parameter validity (e.g., JWT, timestamps).

##### Spring Cloud OAuth 2: Service Protection

OAuth 2 ensures requests are legitimate. Like the Config Center, OAuth 2 is often decoupled as a standalone Authentication Center. **Think of OAuth 2 as a police station. When you need to do business with an organization, you need a valid ID card (identity marker). If you don't have one, you go to the police station (OAuth) to apply for one with an expiration date (Token). With this ID, you can buy flight tickets or hotels (Microservices). The service provider then checks your ID (Token) with the police station (OAuth) to verify its validity.**

OAuth 2 supports 4 authorization types: Password, Client Credentials, Authorization Code, and Implicit.

Benefits of Spring Cloud OAuth 2:
* Security framework providing token generation and validation.
* Seamless integration with other services.
* Industry standard for cloud service integration.

Typical Token Response (`/auth/oauth/token`):
* `access_token`: The OAuth2 token presented for each call.
* `token_type`: Usually "bearer token".
* `refresh_token`: For renewing expired tokens.
* `expires_in`: Expiration time (default 12H).
* `scope`: Valid scope for the token.

OAuth 2 supports JWT (JSON Web Token). JWT characteristics:
* Small (Base64 encoded).
* Cryptographically signed (tamper-proof).
* Self-contained (can be verified locally via shared secret without a remote call).
* Extensible (can contain extra metadata).

Summary:
* OAuth 2 is a token validation framework.
* Using it requires an OAuth 2 validation service.
* All protected resource calls must pass OAuth 2 validation.

##### Spring Cloud Stream: Message-Driven

Our interaction with the world is often asynchronous (email, ordering food, booking tickets). To understand Spring Cloud Stream, you must understand event-driven (MQ) programming models. Using messages helps build highly decoupled systems. Spring Cloud Stream doesn't implement the MQ itself; rather, it encapsulates and abstracts major MQ products like RabbitMQ and Kafka. Spring Cloud Stream does for MQs what an ORM does for databases.

Just as an ORM abstracts away the differences between MySQL, Oracle, and SQL Server, allowing you to access databases without deep dependency or learning different dialects, Spring Cloud Stream abstracts message platforms. You can migrate from RabitMQ to Kafka without changing a line of code.

![image-20250215144952833](https://s2.loli.net/2025/02/15/azCGJhIPDgH5WKF.png)

You program against the Spring Cloud Stream model, regardless of whether the underlying MQ is RabbitMQ or Kafka. That is the benefit of standardization.

![image-20250215145026525](https://s2.loli.net/2025/02/15/mJ7ijsq4ZOCw3Ma.png)

Comparing communication methods:
1. **Synchronous (REST)**: Tight coupling (strong dependency), vulnerability (chain reactions), inflexible for adding new consumers.
2. **Asynchronous (MQ)**: Loose coupling, durability (messages can be consumed after service restart), scalability (scale up services for heavy loads), flexibility (easy to add consumers).

Drawbacks of messaging architecture:
1. **Message Semantics**: Order processing and error handling.
2. **Visibility**: Messages aren't processed immediately; need transaction correlation IDs.

Data in messages:
1. Keep the body as small as possible (usually just action type and ID).
2. Use message status: Include version numbers and timestamps.

Spring Cloud Stream Concepts:
* **Source**: Receives and serializes objects, publishes to the channel.
* **Channel**: Abstraction of a queue; configured via files.
* **Binder**: Spring code that interacts with the message platform.
* **Sink**: Receives messages from the queue and deserializes into a POJO.

Summary:
- Asynchronous communication is a key part of microservices.
- It enables scaling and fault tolerance.
- Spring Cloud Stream abstracts underlying complexity via simple annotations.

##### Sleuth and Zipkin: Distributed Tracing

Distributed architecture adds complexity, particularly in troubleshooting and ops. You need to track a transaction across multiple services and machines. Sleuth and Zipkin are used for this. You can see how long a client request takes at each hop and drill down into details.

![image-20250215145051240](https://s2.loli.net/2025/02/15/5bvwNoFu6nLZAfY.png)

Sleuth Workflow:
1. Transparently creates and injects correlation IDs.
2. Manages propagation of IDs across service calls.
3. Adds info to MDC logs.
4. Publishes trace info to the Zipkin platform.

Open Zipkin:
- Visualizes trace chains more clearly than millions of logs.
- Breaks down time spent in each service.
- Supports 4 storage types: In-memory, MySQL, Cassandra, Elasticsearch.

Summary:
- Sleuth adds IDs seamlessly.
- Allows viewing all service behaviors in a transaction.
- Correlation IDs must be used with log aggregation.
- Log platforms are essential, but visual tracing is a valuable tool.

##### Deploying Microservices

The pipeline is the most important part of microservices, which feature fast building, modification, and release.

Deployment Requirements:
1.  **Automated** (Auto-build and deploy).
2.  **Complete** (Images), **Immutable** (No manual intervention during release).
3.  New features/fixes should be deployable in minutes.

### Spring Cloud Architecture for Large Projects

To design a microservice architecture capable of supporting millions of daily orders for a large Chinese enterprise, we can assemble a system like this:

![image-20250215145215882](https://s2.loli.net/2025/02/15/FpUmAnoHR2abOqJ.png)

In this solution, we didn't strictly follow the default Spring Cloud suite but swapped components based on needs:

* **Config Center**: Swapped Spring Cloud Config for **Apollo** for better performance and a streamlined UI with millisecond-level response.
* **Registry**: Eureka is no longer maintained; we use **Alibaba Nacos**. Service registration and heartbeats are now millisecond-level (Eureka's was 90-second polling).
* **Task Scheduling**: Introduced **XXL-JOB**, a mainstream distributed task platform in China.
* **Log Aggregation**: Used the **ELK** stack for collection and retrieval.

### Summary

Note: At the time of writing, Spring Cloud Zuul is no longer the official recommendation; the better-performing [Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway) is its successor. Microservices are the inevitable path for future large enterprises. Although the cost is high, it significantly improves IT robustness and helps developers gain technical depth and breadth.
