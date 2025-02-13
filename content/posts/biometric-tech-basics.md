+++
date = '2024-04-07T13:57:47+08:00'
draft = false
title = '生物识别标准技术的基本概述'
tags = ["信息安全"]
+++

### 概述

几乎所有的系统都会面临安全认证相关的问题，但是安全相关的问题是一个很麻烦的事情。因为它不产生直接的业务价值，而且处理起来复杂繁琐，所以很多时都容易被忽视。很多后期造成重大的安全隐患，往往都是前期的不重视造成的。但庆幸的是安全问题是普遍存在的，而且大家面临的问题几乎相同，所以可以制定行业标准来规范处理，甚至是可以抽出专门的基础设施（例如：AD、LDAP 等）来专门解决这类共性的问题。总之，关于安全问题非常复杂而且麻烦，对于大多数 99% 的系统来说，不要想着在安全问题领域上搞发明和创新，容易踩坑。而且行业的标准解决方案已经非常成熟了。经过长时间的检验。所以在安全领域，踏踏实实的遵循规范和标准就是最好的安全设计。

### HTTP 认证

HTTP 认证协议的最初是在 HTTP/1.1标准中定义的，后续由 IETF 在 RFC 7235 中进行完善。HTTP 协议的主要涉及两种的认证机制。

![HTTP 认证的对话框](https://s2.loli.net/2025/02/13/XP3jWseyQLfw7T2.png)

#### 基本认证

常见的叫法是 **HTTP Basic**，是一种对于安全性不高，以演示为目的的简单的认证机制（例如你家路由器的登录界面），客户端用户名和密码进行 Base64 编码（注意是编码，不是加密）后，放入 HTTP 请求的头中。服务器在接收到请求后，解码这个字段来验证用户的身份。示例：

```http
GET /some-protected-resource HTTP/1.1
Host: example.com
Authorization: Basic dXNlcjpwYXNzd29yZA==
```

虽然这种方式简单，但并不安全，因为 `base64` 编码很容易被解码。建议仅在 HTTPS 协议下使用，以确保安全性。

#### 摘要认证

主要是为了解决 HTTP Basic 的安全问题，但是相对也更复杂一些，摘要认证使用 MD5 哈希函数对用户的密码进行加密，并结合一些盐值（可选）生成一个摘要值，然后将这个值放入请求头中。即使在传输过程中被截获，攻击者也无法直接从摘要中还原出用户的密码。示例：

```http
GET /dir/index.html HTTP/1.1
Host: example.com
Authorization: Digest username="user", realm="example.com", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", uri="/dir/index.html", qop=auth, nc=00000001, cnonce="0a4f113b", response="6629fae49393a05397450978507c4ef1", opaque="5ccc069c403ebaf9f0171e9517f40e41"
```

**补充：**另在 RFC 7235 规范中还定义当用户没有认证访问服务资源时应返回 `401 Unauthorized` 状态码，示例：

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Restricted Area"
```

这一规范目前应用在所有的身份认证流程中，并且沿用至今。

### Web 认证

#### 表单认证

虽然 HTTP 有标准的认证协议，但目前实际场景中大多应用都还是基于表单认证实现，具体步骤是：

1.  前端通过表单收集用户的账号和密码
1.  通过协商的方式发送服务端进行验证的方式。

常见的表单认证页面通常如下：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h2>Login Form</h2>
    <form action="/perform_login" method="post">
        <div class="container">
            <label for="username"><b>Username</b></label>
            <input type="text" placeholder="Enter Username" name="username" required>
            
            <label for="password"><b>Password</b></label>
            <input type="password" placeholder="Enter Password" name="password" required>
            
            <button type="submit">Login</button>
        </div>
    </form>
</body>
</html>
```

为什么表单认证会成为主流 ？主要有以下几点原因：

-   界面美化：开发者可以创建定制化的登录界面，可以与应用的整体设计风格保持一致。而 HTTP 认证通常会弹出一个很丑的模态对话框让用户输入凭证。
-   灵活性：可以在表单里面自定义更多的逻辑和流程，比如多因素认证、密码重置、记住我功能等。这些功能对于提高应用的安全性和便利性非常重要。
-   安全性：表单认证可以更容易地结合现代的安全实践，背后也有 OAuth 2 、Spring Security 等框架的主持。

表单认证传输内容和格式基本都是自定义本没啥规范可言。但是在 2019 年之后 web 认证开始发布标准的认证协议。

#### WebAuthn

WebAuthn 是一种彻底抛弃传统密码的认证，完全基于生物识别技术和实体密钥作为身份识别的凭证（有兴趣的小伙伴可以在 github 开启 Webauhtn 的 2FA 认证体验一下）。在 2019 年 3 月，W3C 正式发布了 WebAuthn 的第一版规范。

![webauthn registration](https://s2.loli.net/2025/02/13/EJy13jxtKrkeUMY.png)

相比于传统的密码，WebAuthn 具有以下优势：

1.  减少密码泄露：传统的用户名和密码登录容易受到钓鱼攻击和数据泄露的影响。WebAuthn，不依赖于密码，不存在密码丢失风险。
1.  提高用户体验：用户不需要记住复杂的密码，通过使用生物识别等方式可以更快捷、更方便地登录。
1.  多因素认证：WebAuthn 可以作为多因素认证过程中的一部分，进一步增强安全性。使用生物识别加上硬件密钥的方式进行认证，比短信验证码更安全。

总的来说，WebAuthn 是未来的身份认证方式，通过提供一个更安全、更方便的认证方式，目的是替代传统的基于密码的登录方法，从而解决了网络安全中的一些长期问题。WebAuthn 目前已经得到流程的浏览器厂商（Chrome、Firefox、Edge、Safari）、操作系统（WIndows、macOS、Linux）的广泛支持。

**实现效果**

当你的应用接入 WebAuthn 后，用户便可以通过生物识别设备进行认证，效果如下：

![WebAuthn login](https://s2.loli.net/2025/02/13/xdSlg93QyJF1zYE.png)

**实现原理**

WebAuthn 实现较为复杂，这里不做详细描述，具体可参看权威的官方文档，大概交互过程可以参考以下时序图：

![webauthn 交互时序图](https://s2.loli.net/2025/02/13/jM8ZNHhcuGR3WVA.png)

登录流程大致可以分为以下步骤：

1.  用户访问登录页面，填入用户名后即可点击登录按钮。
1.  服务器返回随机字符串 Challenge、用户 UserID。
1.  浏览器将 Challenge 和 UserID 转发给验证器。
1.  验证器提示用户进行认证操作。
1.  服务端接收到浏览器转发来的被私钥加密的 Challenge，以此前注册时存储的公钥进行解密，如果解密成功则宣告登录成功。

WebAuthn 采用非对称加密的公钥、私钥替代传统的密码，这是非常理想的认证方案，私钥是保密的，只有验证器需要知道它，连用户本人都不需要知道，也就没有人为泄漏的可能；

> 备注：你可以通过访问 webauthn.me 了解到更多消息的信息

文章不适合加入过多的演示代码，想要手上体验的可以参考 okta 官方给出基于 Java 17 和 Maven 构建的 webauthn 示例程序，如下：

-   访问地址：https://github.com/oktadev/webauthn-java-example

