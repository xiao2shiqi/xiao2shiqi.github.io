+++
date = '2024-04-24T13:40:10+08:00'
draft = true
title = 'Cookie-Session 与 JWT 两种凭证管理方案的对比'
+++

### 概述

在上一篇文章我们聊完了授权的过程，在服务器对客户端完成授权之后，服务器会给客户端颁发对应的凭证，客户端持有该凭证访问服务端，服务器便能知道你是谁，你有什么权限等信息。这一章我们具体聊聊常见的凭证管理技术有哪些。

在软件架构中，关于凭证如何存储和传递，一直有两种不同的解决思路，两种不同的解决方式，实际上反映了两种不同的架构思路：

1. 一种是把所有状态信息都放在服务器端 （Cookie-Session 方案）
2. 一种是把所有状态将信息存储在客户端（JWT 方案）

在互联网早期，这个问题早就有了明确的答案。大多数应用都采用了 “Cookie-Session” 的方法，这种方法通过在服务器上存储用户状态，来实现用户身份的识别和信息的传递。这种方法在很长一段时间里都是主流。

然而，随着微服务和分布式系统的兴起，我们发现由于 CAP 的限制，服务器端存储状态信息的方式开始面临很多问题（微服务要求服务端本身是无状态，才能实现动态扩缩容）。这就迫使我们重新考虑被放弃的客户端状态存储方法。在这个背景下，JWT（JSON Web Token）的令牌的方案开始受到关注。JWT 是一种在客户端存储用户状态信息的方式，它允许用户在不同的服务器之间自由切换，而不需要重新登录。这种特性在分布式系统中非常有用。但是要明白，JWT 和 Cookie-Session 只是对授权信息存储的主体（客户端，服务端）不同，各有优势，合适场景不同，不存在谁比谁要先进的问题。在本节中，我们将探讨 Cookie-Session 和 JWT 两种方案的相同点和不同点，帮你更好地理解这两种方案的优缺点，以及它们在不同场景下的应用。

### cookie-session

总所周知，因为 HTTP 是无状态协议，所以 Cookie-Session 的原理其实很简单，就是解决 HTTP 协议无状态的问题，在 RFC 6265 中定义了 HTTP 的状态管理机制，增加 `Set-Cookie` 指令，服务端向客户端发送一组信息（标识）示例：

```
HTTP/1.1 200 OK
Content-type: text/html
Set-Cookie: session_token=abc123; Expires=Wed, 09 Jun 2021 10:18:14 GMT; Path=/
```

客户端收到指令后在此后一段时间的 HTTP 请求中都发给服务端会话信息（在 Header 中携带 cookie 信息），以便服务器区分不同的客户端：

```
GET /profile HTTP/1.1
Host: www.example.com
Cookie: sessionid=xyzasdzxc123789456
```

客户端的 Cookies 里通常只存储一个无意义，不重复的字符串，通常命名是 `sessionid` 或 `jessionid` ，服务端则根据该字符串作为 Key，和用户信息建立关联后存储在服务端的内存或者缓存中。再辅以一些超时自动清理的措施来管理会话。

它们的交互过程如下：

![cookie-session](https://s2.loli.net/2025/02/13/UoBaHJg3G4p2EKb.png)

这种服务端的状态管理机制就是 Session，Cookie-Session 也是最传统，但今天依然广泛应用于大量系统中的，由服务端与客户端联动来完成的状态管理机制。

**总结**

cookie-session 的方案在存储授权信息具有以下优势：

0.  安全性：由于状态信息都存储在服务端，cookie-session 方案在安全性上有天然的优势，能完全规避上下文信息在传输过程中被篡改的风险
0.  灵活性：由于存储在服务端，服务端可以存储各种数据对象，而不仅仅是字符串
0.  状态控制：服务端维护状态的优势在于可以根据自己的意愿随时修改，清除上下文信息，可以很轻松实现用户强制下线的功能。

Cookie-Session 在单体服务环境中是最合适的方案，但是因为服务端有状态，当需要水平扩展服务能力，要部署集群时就开始面临麻烦了。接下来的 JWT 令牌就是 Cookie-Session 在分布式环境的替代品，但是不能说 JWT 要比 Cookie-Session 更加先进，更不可能全面取代 Cookie-Session 机制。

### JWT

> 当服务端有多台，并且不能存储状态的时候，客户端就要承担存储有状态（授权信息）的职责了。这就是 JWT 令牌的方案思路。

JWT（JSON Web Token）是一种定义在 [RFC 7519](https://tools.ietf.org/html/rfc7519) 标准中的令牌格式，主要应用于现代分布式应用系统中，经常与 OAuth2 协议配合使用。在深入探讨 JWT 的结构之前，我们先来直观地了解一下它的基本形式。示例：

![jwt-info](https://s2.loli.net/2025/02/13/HTfC7nkqAcR6JiD.png)

注意：JWT 令牌不加密，只使用 Base64URL 转码，所以 JWT 令牌里别放敏感信息，令牌只解决防篡改的问题，并不解决防泄漏的问题，JWT 令牌都可以在 JWT 官网（<https://jwt.io>）上进行解码。如图所示，JWT（JSON Web Token）由三部分组成：Header（头部）、Payload（负载）、Signature（签名）。这三部分之间使用点（`.`）分隔。

**Header**：Header 部分通常包含令牌的类型（通常是 JWT）和使用的加密算法，例如 `HS256`：

```
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**：Payload 部分包含所需的声明，这些声明可以包括用户信息或其他相关数据。例如，用户ID和过期时间：

```
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

负载部分，JWT 在 RFC 7519 中推荐（非强制约束）了七项声明名称（Claim Name），如有需要用到这些内容，建议字段名与官方的保持一致：

-   iss（Issuer）：签发人。
-   exp（Expiration Time）：令牌过期时间。
-   sub（Subject）：主题。
-   aud （Audience）：令牌受众。
-   nbf （Not Before）：令牌生效时间。
-   iat （Issued At）：令牌签发时间。
-   jti （JWT ID）：令牌编号。

此外在 RFC 8225、RFC 8417、RFC 8485 等规范文档，以及 OpenID 等协议中，都定义有约定好公有含义的名称，可以参考 [IANA JSON Web Token Registry](https://www.iana.org/assignments/jwt/jwt.xhtml)。

**Signature**：Signature 是使用 Header 中指定的算法和一个密钥对 Header 和 Payload 进行签名得到的。对前面两部分内容进行加密计算，以例子里使用的 JWT 默认的 HMAC SHA256 算法为例，将通过以下公式产生签名值：

```
HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload) , secret)
```

签名的意义在于确保负载中的信息是可信的、没有被篡改的，也没有在传输过程中丢失任何信息。因为被签名的内容哪怕发生了一个字节的变动，也会导致整个签名发生显著变化。JWT 默认使用的 HMAC SHA256 算法是一种密钥哈希算法，适用于单体应用中，因为加密和验证都需要由同一授权服务完成。在多方或分布式应用中，通常使用非对称加密算法进行签名。这种情况下，授权服务使用私钥签名，并通过遵循 [JSON Web Key 规范公开一个公钥](https://datatracker.ietf.org/doc/html/rfc7517)。这个公钥用于验证签名，使其他服务能够独立验证 JWT 的真实性，无需直接与授权服务通信。

JWT 令牌的交互流程如下：

![jwt-process](https://s2.loli.net/2025/02/13/5Nm6pBQeCdFwaWf.png)

说明：如果是在分布式环境下，通常会有单独的认证服务器来负责颁发令牌。

**发送令牌**

按照 HTTP 协议的规范，客户端可以通过多种方式使用 HTTP 协议发送 JWT 令牌给服务端。最标准的方式是将 JWT 放在 HTTP 的 `Authorization` 头部中，通常与 `Bearer` 方案一起使用。这种方法简单且符合 RESTful API 的最佳实践：

```
GET /api/resource HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIx......
```

**总结**

JWT 令牌是分布式系统下凭证载体的优秀解决方案，它优点众多：

0.  解决了分布式系统下的状态信息的管理问题，让服务端无状态，实现动态扩缩容。
0.  结构简单，轻量，凭证本身包含重要信息，服务端无需再查询数据库
0.  通过密钥对和签名的方式，保证凭证信息的无法被篡改，保证了凭证的真实性

但是没有完美的解决方案，cookie-session 的优点也 JWT 也缺点：

0.  会话难以主动失效：服务端难以注销令牌，如果非要实现，就要把状态信息转移存储到 redis 中。
0.  携带的信息有限：虽然 HTTP 没有限制 Header 中可存储的大小限制，但是 HTTP 服务端大多都有存储上限，例如 tomcat 限制 8kb，nginx 限制 4kb
0.  客户端令牌泄露风险：客户端令牌存在哪里 ？ Cookie ? localStrong ? Indexed ? 存在哪里都有泄露风险。只要拿到令牌就能冒认客户端身份
0.  服务端无状态会导致很多常见的功能难以实现，例如：踢人下线，统计在线人数等等。。