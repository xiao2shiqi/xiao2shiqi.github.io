+++
date = '2024-04-15T13:49:14+08:00'
draft = false
title = 'Basic Access and Authorization Models: Combined Application of OAuth2 and RBAC'
tags = ["Information Security"]
+++

### Overview

In security management systems, the concept of Authorization often appears alongside Authentication, Account, and Audit—collectively known as the 4A framework. As mentioned in the previous article, implementing security modules is best done by following industry standards and best practices, and authorization is no exception.

As part of a security system, the responsibilities of authorization are as follows:

* Ensure the authorization process is controllable: Common standards include OAuth2, SAML2, CAS protocols, etc.
* Ensure authorization results are controllable: Common standards include RBAC, ABAC authorization models, etc.

For most applications, the mainstream approach is implementing authorization through a combination of OAuth2 + RBAC. Let's expand on these two directions.

### RBAC

RBAC (Role-Based Access Control) is a common way to manage permissions. In this model, the system assigns permissions based on a user's role rather than directly to individual users. This simplifies permission management and configuration, avoiding the need for frequent permission operations on users. It is illustrated as follows:

![RBAC Model](https://s2.loli.net/2025/02/13/D5Prx9flHERhJbz.png)

If there are more complex access control needs, you can extend RBAC0 with RBAC1 (Hierarchical RBAC, where roles have inheritance relationships) and RBAC2 (Constrained RBAC, where roles have mutual exclusion relationships) to improve system security and management convenience. There is also RBAC 3, and so on.

For most applications, there is usually no need to implement these theoretical models yourself. The security issues encountered by most apps are common and universal, allowing them to be abstracted and solved at the framework level. For example, the famous Spring Security framework provides an RBAC-based authorization implementation.

However, it is important to note that while universal access control is relatively straightforward, controlling data permissions is much more difficult. Data access permissions are often highly correlated with business logic, varying by department, role, or even specific individuals. This lacks universality and cannot be solved purely at the framework level—even Spring Security does not provide specific controls for data-level permissions. These must be implemented by business systems in the business layer based on actual circumstances, which remains a prevalent challenge.

### OAuth 2

OAuth2 is an industry-standard authorization protocol that allows users to authorize third-party applications to access their resources on other service providers without sharing their usernames and passwords. It defines four authorization interaction modes suitable for various scenarios:

* Authorization Code Mode
* Implicit Grant
* Password Mode
* Client Mode

OAuth2 implements access control for protected resources through Access Tokens and Refresh Tokens. By innovatively using Tokens instead of user passwords, it prevents the leakage of user credentials.

#### Authorization Code

The Authorization Code mode is arguably the most secure authorization mode, comprehensively considering various risks and preventive measures. However, it is also the most complex protocol, suitable for scenarios where a server can store a ClientSecret. The flow is as follows:

![Authorization Code Flow](https://s2.loli.net/2025/02/13/yTxcfGC2bIrQ6Ds.png)

After seeing the process, you might be curious: **Why does the authorization server return an authorization code instead of returning the token directly?**

The design to return a code first is primarily to improve security for the following reasons:

1. Even if the authorization code is intercepted, the attacker cannot obtain the Access Token without the Client Secret. The secret is only stored on the server side and never exposed through the frontend.
2. During the redirect back to the client app, the authorization code is transmitted via the browser. If the Access Token were transmitted directly, its leakage would pose a much higher risk. The code can be strictly limited (e.g., one-time use, very short validity), making it difficult to exploit even if leaked.
3. When the client uses the code to request a token, the authorization server can verify the Client Secret and Redirect URI contained in the request, ensuring the token request is legitimate.

Additionally, in terms of token issuance strategies, the Authorization Code mode employs a dual-token strategy (long-lived Refresh Token + short-lived Access Token) to minimize the issues associated with the difficulty of revoking stateless JWT tokens. Therefore, given a server can store tokens, the Authorization Code mode is the preferred choice for most scenarios.

#### Implicit Grant

The Implicit Grant mode supports pure frontend applications (SPAs) that lack a server-side storage for a ClientSecret. The integration process is relatively simple:

![Implicit Grant Flow](https://s2.loli.net/2025/02/13/GIdCurElvxVnMPS.png)

In this mode, once user authentication passes, the authorization server returns the token directly to the client, bypassing the ClientSecret and code exchange steps. The cost, however, is reduced security, as the token might be exposed to attackers during redirection.

To address security concerns, OAuth 2 makes its best effort:

1. Limiting the callback URI of the third-party app to match the domain provided during registration.
2. Explicitly forbidding the issuance of Refresh Tokens in Implicit mode.
3. Tokens must be returned "via Fragment" (meaning they can only be read via scripts, as per RFC 3986).

Implicit Grant does its best to prevent token leakage. However, it is not the mainstream way to integrate with OAuth 2 and is generally not recommended unless absolutely necessary.

#### Password Mode

This is mainly used in non-browser access scenarios. If Password mode is adopted, the "third-party" attribute must be weakened—the "third-party" is treated as an internal sub-module of the system, physically independent but logically within the same system. This makes finishing authentication and authorization together in Password mode a reasonable scenario:

![Password Mode Flow](https://s2.loli.net/2025/02/13/RTW1sdLK387SlIO.png)

Password mode is very simple: exchanging a username and password for a token from the auth server. In this mode, OAuth2 does not guarantee security; security must be provided by the user and the third-party app themselves.

#### Client Mode

An application-centric authorization mode that does not involve user login. Client mode refers to a third-party application applying for credentials in its own name to access protected resources:

![Client Mode Flow](https://s2.loli.net/2025/02/13/etPQIj3qy8gF7uW.png)

Client mode is typically used for inter-service communication in microservices, such as scheduled tasks or application-to-application authorization. Microservice architectures do not advocate for default trust between services; therefore, service calls must be authenticated and authorized before communication. For example, the common `Spring Cloud` framework uses this scheme to ensure legitimate calls between services.
