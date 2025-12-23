+++
date = '2024-04-24T13:40:10+08:00'
draft = false
title = 'Comparison of Cookie-Session and JWT Credential Management'
tags = ["Information Security"]
+++

### Overview

In the previous article, we discussed the process of authorization. After the server completes authorization for the client, it issues a corresponding credential. When the client accesses the server with this credential, the server knows who you are and what permissions you have. In this chapter, we will discuss common credential management technologies.

In software architecture, there have been two different ideas regarding how credentials are stored and transmitted, reflecting two different architectural approaches:

1. Storing all state information on the server-side (**Cookie-Session** approach).
2. Storing all state information on the client-side (**JWT** approach).

In the early days of the Internet, this question had a clear answer. Most applications used the "Cookie-Session" method, which identified users and passed information by storing user state on the server. This remained the mainstream for a long time.

However, with the rise of microservices and distributed systems, we found that due to CAP constraints, storing state information on the server faced many problems (microservices require the server to be stateless for dynamic scaling). This forced us to reconsider client-side state storage. In this context, the JWT (JSON Web Token) scheme began to gain attention. JWT allows users to switch between different servers without re-logging in. This is very useful in distributed systems. However, it's important to understand that JWT and Cookie-Session differ mainly in where the authorization information is stored (client vs. server). Each has its advantages and suitable scenarios; one is not strictly "more advanced" than the other. In this section, we will explore the similarities and differences between the two.

### Cookie-Session

Since HTTP is a stateless protocol, the principle of Cookie-Session is to solve this statelessness. RFC 6265 defines the HTTP state management mechanism by adding the `Set-Cookie` directive. The server sends a set of information (identifier) to the client:

```http
HTTP/1.1 200 OK
Content-type: text/html
Set-Cookie: session_token=abc123; Expires=Wed, 09 Jun 2021 10:18:14 GMT; Path=/
```

The client then includes this cookie information in the headers of subsequent HTTP requests to the server, allowing the server to distinguish different clients:

```http
GET /profile HTTP/1.1
Host: www.example.com
Cookie: sessionid=xyzasdzxc123789456
```

The client's cookies usually store an opaque, unique string named `sessionid` or `jsessionid`. The server uses this string as a key to associate it with user information stored in server memory or cache, managed with timeout policies.

![cookie-session](https://s2.loli.net/2025/02/13/UoBaHJg3G4p2EKb.png)

This server-side state management is called a Session. Cookie-Session is the traditional but still widely used mechanism for state management.

**Summary**

Advantages of the Cookie-Session approach:
- **Security**: Since state is on the server, it naturally avoids risks of context information being tampered with during transmission.
- **Flexibility**: The server can store complex data objects, not just strings.
- **State Control**: The server can modify or clear session information at will, making it easy to force a user to log out.

Cookie-Session is the most suitable scheme for monolithic services. However, because the server is stateful, horizontal scaling becomes difficult. JWT serves as its alternative in distributed environments.

### JWT

> When there are multiple servers and state cannot be stored centrally, the client must take responsibility for storing stateful information. This is the idea behind JWT.

JWT (JSON Web Token) is a token format defined in [RFC 7519](https://tools.ietf.org/html/rfc7519), frequently used with OAuth2 in modern distributed systems.

![jwt-info](https://s2.loli.net/2025/02/13/HTfC7nkqAcR6JiD.png)

**Note:** JWT tokens are not encrypted; they are only Base64URL encoded. Therefore, do not put sensitive information in them. Tokens solve the problem of tampering, not leakage. You can decode them on [jwt.io](https://jwt.io). A JWT consists of three parts separated by dots: Header, Payload, and Signature.

**Header**: Usually contains the token type and the signing algorithm used (e.g., `HS256`).
**Payload**: Contains claims (user info or other data). RFC 7519 recommends several claim names like `iss` (issuer), `exp` (expiration), `sub` (subject), etc.
**Signature**: Created by signing the encoded Header and Payload using the specified algorithm and a secret. The signature ensures the information hasn't been tampered with.

In distributed systems, asymmetric encryption is often used for signatures. The authorization service signs with a private key, and other services verify with a public key.

![jwt-process](https://s2.loli.net/2025/02/13/5Nm6pBQeCdFwaWf.png)

**Summary**

JWT is an excellent credential solution for distributed systems:
- It solves state management issues, allowing servers to be stateless and scale dynamically.
- It is lightweight and self-contained; servers don't always need to query a database to know who the user is.
- Signatures ensure authenticity and prevent tampering.

However, it has drawbacks:
- **Revocation is difficult**: The server cannot easily invalidate a token once issued.
- **Limited information**: While HTTP doesn't strictly limit header size, many servers do (e.g., Nginx 4kb).
- **Client leakage risk**: If a token is stolen from client storage (Cookie, LocalStorage), the attacker can impersonate the user.
- **Statelessness makes some features hard**: Such as "kicking" a user offline or counting real-time online users.
