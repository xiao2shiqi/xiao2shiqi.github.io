+++
date = '2024-04-24T13:40:10+08:00'
draft = false
title = 'Comparison of Cookie-Session and JWT Credential Management'
tags = ["Information Security"]
+++


### Overview

In the previous article, we finished discussing the authorization process. After the server completes authorization for the client, it issues a corresponding credential. When the client accesses the server with this credential, the server knows who you are and what permissions you have. In this chapter, we will discuss common credential management technologies.

In software architecture, there have always been two different ideas regarding how credentials are stored and transmitted, reflecting two different architectural approaches:

1. Storing all state information on the server-side (**Cookie-Session** approach).
2. Storing all state information on the client-side (**JWT** approach).

In the early days of the Internet, this question had a clear answer. Most applications used the "Cookie-Session" method, which identified users and passed information by storing user state on the server. This method was the mainstream for a long time.

However, with the rise of microservices and distributed systems, we found that due to CAP constraints, storing state information on the server faced many problems (microservices require the server to be stateless for dynamic scaling). This forced us to reconsider client-side state storage. In this context, the JWT (JSON Web Token) scheme began to gain attention. JWT is a way to store user state information on the client, allowing users to switch freely between different servers without re-logging in. This is very useful in distributed systems. However, it's important to understand that JWT and Cookie-Session differ primarily in where the authorization information is stored (client vs. server). Each has its advantages and suitable scenarios; one is not strictly "more advanced" than the other. In this section, we will explore the similarities and differences between these two schemes to help you better understand their pros and cons and their applications in different scenarios.

### Cookie-Session

As is well known, because HTTP is a stateless protocol, the principle of Cookie-Session is actually quite simple—it solves the statelessness of the HTTP protocol. RFC 6265 defines the HTTP state management mechanism, adding the `Set-Cookie` directive. The server sends a set of information (identifier) to the client:

```http
HTTP/1.1 200 OK
Content-type: text/html
Set-Cookie: session_token=abc123; Expires=Wed, 09 Jun 2021 10:18:14 GMT; Path=/
```

After receiving the directive, the client sends this session information (carrying cookie info in the Header) in subsequent HTTP requests, so the server can distinguish different clients:

```http
GET /profile HTTP/1.1
Host: www.example.com
Cookie: sessionid=xyzasdzxc123789456
```

The client's cookies usually store an opaque, unique string named `sessionid` or `jsessionid`. The server then uses this string as a Key to associate it with user information stored in server memory or cache, managed with timeout auto-cleanup measures.

Their interaction process is as follows:

![cookie-session](https://s2.loli.net/2025/02/13/UoBaHJg3G4p2EKb.png)

This server-side state management mechanism is called a Session. Cookie-Session is the traditional but still widely used state management mechanism accomplished via coordination between server and client.

**Summary**

The Cookie-Session approach has several advantages in storing authorization info:

1. **Security**: Since state information is stored on the server, it has a natural advantage in security, completely avoiding the risk of context information being tampered with during transmission.
2. **Flexibility**: Because data is on the server, the server can store various data objects, not just strings.
3. **State Control**: The advantage of the server maintaining state is that it can modify or clear context information at will, making it easy to implement features like forcing a user to log out.

Cookie-Session is the most suitable scheme for monolithic service environments. However, because the server is stateful, horizontal scaling becomes difficult when cluster deployment is required. JWT serves as its alternative in distributed environments, but it cannot be said that JWT is "more advanced" than Cookie-Session, nor can it completely replace it.

### JWT

> When there are multiple servers and state cannot be stored centrally, the client must take responsibility for storing stateful (authorization) information. This is the idea behind the JWT token scheme.

JWT (JSON Web Token) is a token format defined in the [RFC 7519](https://tools.ietf.org/html/rfc7519) standard, primarily used in modern distributed applications and often in conjunction with the OAuth2 protocol. Before diving into the structure of JWT, let's look at its basic form:

![jwt-info](https://s2.loli.net/2025/02/13/HTfC7nkqAcR6JiD.png)

**Note:** JWT tokens are not encrypted; they are only Base64URL encoded. Therefore, do not put sensitive information in them. Tokens solve the problem of tampering, not leakage. You can decode any JWT on the official website (<https://jwt.io>). As shown, a JWT consists of three parts separated by dots (`.`): Header, Payload, and Signature.

**Header**: Usually contains the token type (usually JWT) and the signing algorithm used, e.g., `HS256`:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**: Contains the required claims, which can include user info or other relevant data. For example, user ID and expiration time:

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

For the Payload part, RFC 7519 recommends (non-mandatory) seven claim names. If you use these contents, it's recommended to match the official names:

- **iss (Issuer)**: The entity that issued the token.
- **exp (Expiration Time)**: When the token expires.
- **sub (Subject)**: The subject of the token (e.g., user ID).
- **aud (Audience)**: The intended recipient of the token.
- **nbf (Not Before)**: When the token becomes effective.
- **iat (Issued At)**: When the token was issued.
- **jti (JWT ID)**: A unique identifier for the token.

Furthermore, documents like RFC 8225, RFC 8417, RFC 8485, and protocols like OpenID define other names with standardized meanings, which can be found in the [IANA JSON Web Token Registry](https://www.iana.org/assignments/jwt/jwt.xhtml).

**Signature**: The signature is obtained by signing the encoded Header and Payload using the specified algorithm and a secret key. Encrypting the first two parts involves a formula; for the HMAC SHA256 example:

```
HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload) , secret)
```

The purpose of the signature is to ensure that the info in the payload is trustworthy and hasn't been tampered with or lost. Even a one-byte change in the signed content will result in a significantly different signature. The default HMAC SHA256 algorithm is a secret-key hash algorithm suitable for monolithic apps where both encryption and verification are handled by the same service. In multi-party or distributed apps, asymmetric encryption is typically used. In such cases, the authorization service signs with a private key and [publicizes a public key based on JSON Web Key specs](https://datatracker.ietf.org/doc/html/rfc7517). This public key is used to verify signatures, allowing other services to independently verify the JWT's authenticity without direct communication with the auth service.

The interaction flow for JWT tokens is as follows:

![jwt-process](https://s2.loli.net/2025/02/13/5Nm6pBQeCdFwaWf.png)

**Note:** In a distributed environment, there is typically a separate authentication server responsible for issuing tokens.

**Sending Tokens**

Following HTTP protocol conventions, clients can send JWT tokens to servers in several ways. The most standard method is placing the JWT in the HTTP `Authorization` header, typically using the `Bearer` scheme. This is simple and aligns with RESTful API best practices:

```http
GET /api/resource HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIx......
```

**Summary**

JWT tokens are an excellent solution for credential carriers in distributed systems, offering many advantages:

1. They solve state management in distributed systems, keeping the server stateless for dynamic scaling.
2. They are simple and lightweight; credentials themselves contain important info, so servers don't always need to query the database.
3. Secret-key pairs and signatures prevent tampering, ensuring authenticity.

However, no solution is perfect, and Cookie-Session's strengths are JWT's weaknesses:

1. **Active Revocation is Difficult**: Servers struggle to log out tokens. If required, state must be moved to central storage like Redis.
2. **Limited Payload Info**: While HTTP doesn't strictly limit header size, most servers do (e.g., Tomcat limits to 8kb, Nginx to 4kb).
3. **Client Leakage Risk**: Tokens stored in Cookies, LocalStorage, or IndexedDB are at risk of leakage. Anyone with the token can impersonate the client.
4. **Statelessness hinders common features**: Such as kicking users offline, counting online users, etc.
