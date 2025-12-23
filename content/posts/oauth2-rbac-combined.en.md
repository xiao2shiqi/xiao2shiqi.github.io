+++
date = '2024-04-15T13:49:14+08:00'
draft = false
title = 'Basic Access and Authorization Models: Combining OAuth2 and RBAC'
tags = ["Information Security"]
+++

### Overview

In security systems, **Authorization** is part of the "4A" framework (Account, Authentication, Authorization, and Audit). To build a reliable security module, it is best to follow industry standards. 

Authorization involves:
1. **Control of the Process**: Protocols like **OAuth2**, **SAML2**, or **CAS**.
2. **Control of the Outcome**: Models like **RBAC** or **ABAC**.

The mainstream approach for most applications is a combination of **OAuth2 + RBAC**.

### RBAC (Role-Based Access Control)

RBAC maps permissions to **Roles**, and then assigns roles to **Users**. This decouples users from specific permissions, making management much simpler.

**Variations:**
- **RBAC0**: Basic model (User -> Role -> Permission).
- **RBAC1**: Adds role hierarchies (inheritance).
- **RBAC2**: Adds constraints (e.g., Separation of Duties).

Frameworks like **Spring Security** provide excellent support for RBAC. However, **Data Permission** (restricting which specific data rows a user can see) is much more complex and usually requires custom implementation at the business layer, as it is highly specific to the application's logic.

### OAuth 2

OAuth2 is a delegation protocol that allows third-party apps to access resources without knowing user passwords. It issues **Access Tokens** to clients.

#### 1. Authorization Code Flow
The most secure flow, used for server-side apps.
- **Why use a code?** The code is exchanged for a token on the backend using a `ClientSecret`. This ensures the token and secret are never exposed to the frontend browser, significantly reducing the attack surface. It also allows for the use of short-lived tokens and refresh tokens.

#### 2. Implicit Flow
Used for pure frontend apps (SPAs) where a `ClientSecret` cannot be kept safe.
- **Security tradeoffs**: The token is returned directly in the URL fragment. To mitigate risks, OAuth2 forbids refresh tokens in this mode and strictly enforces callback URI matching.

#### 3. Resource Owner Password Credentials Flow
The user gives their credentials directly to the client. This should only be used for highly trusted "internal" apps where the client and the auth server are part of the same organization.

#### 4. Client Credentials Flow
Used for machine-to-machine communication (e.g., microservices). The client authenticates as itself to access resources. This is a standard pattern in **Spring Cloud** for inter-service security.

### Summary

OAuth2 manages the "how" of obtaining access, while RBAC manages the "what" the user can actually do once they have that access. Together, they form a robust foundation for modern application security.
