+++
date = '2024-05-07T13:20:19+08:00'
draft = false
title = 'The Main Process of HTTPS Transport Encryption'
tags = ["Information Security"]
+++

### Overview

Modern cryptography handles information in three main forms:

1.  **Digest**: Primarily used for data validation (e.g., storing passwords). A digest is a one-way hash. Hash functions are characterized by their sensitivity (even tiny changes produce totally different results) and irreversibility. Common algorithms include `MD5` and `SHA-256`.
2.  **Encryption**: Used to ensure secure transmission so that only authorized parties can access the real message. Unlike digests, encrypted data can be decrypted back to plaintext. Keys are categorized into symmetric and asymmetric (public/private). Common algorithms include `AES` and `RSA`.
3.  **Signature**: Used to ensure the integrity and authenticity of plaintext messages. For example, a JWT contains a signature to guarantee that the payload was not tampered with. Signatures do not guarantee privacy; the message itself is often public.

**In summary:**
- Digests ensure integrity.
- Encryption ensures confidentiality.
- Signatures ensure authenticity.

### Keys

#### Symmetric Keys

![Symmetric Encryption](https://s2.loli.net/2025/02/13/oJPagjRvX3O1uZb.jpg)

Symmetric encryption uses the same key for both encryption and decryption. It is simple, fast, and efficient for large amounts of data. Common algorithms: **AES**, **DES**, **3DES**. The main challenge is key distribution: the key must be shared securely between parties.

#### Asymmetric Keys

![Asymmetric Encryption](https://s2.loli.net/2025/02/13/LSTVGgFCwNEM3dP.png)

Asymmetric encryption uses a pair of keys: a public key for encryption and a private key for decryption. While it solves the key distribution problem, it is computationally expensive and slow. Therefore, it is usually used to securely exchange a symmetric key, which is then used for the actual data transfer. This is called **Hybrid Encryption**.

### Certificates

To establish trust with a party you've never met online, we rely on a **Trusted Third Party**—the CA (Certificate Authority).

#### CA (Certificate Authority)

A CA issues digital certificates to servers. When a client visits a server, it checks the certificate's validity to establish a secure link.

![Secure Link Icon](https://s2.loli.net/2025/02/13/vNJxOcLuSWqi2aH.png)

Server certificates follow the X.509 standard and include:
- **Version**: X.509 version.
- **Serial Number**: Unique ID assigned by CA.
- **Signature Algorithm**: Algorithm used for the certificate's signature.
- **Issuer**: The CA that issued the certificate.
- **Validity**: Start and end dates.
- **Subject**: Usually the domain name.
- **Subject Public Key Info**: The server's public key.

### Secure Transport Protocol

The combination of keys and certificates is applied in the network via SSL/TLS.

**History of SSL/TLS:**
- 1994: SSL (Netscape) introduced.
- 1999: TLS 1.0 (IETF) released as the successor to SSL.
- 2018: TLS 1.3 simplified the handshake for better speed and security.

#### The TLS 4-Way Handshake
1.  **ClientHello**: Client sends supported TLS versions, cipher suites, and a random number.
2.  **ServerHello**: Server responds with the chosen version, cipher suite, its certificate, and another random number.
3.  **Client Finished**: Client verifies the certificate, generates a "Master Secret" (using a public key), and notifies the server.
4.  **Server Finished**: Server confirms and ends the handshake.

Once established, the HTTPS connection ensures:
- **Confidentiality**: No one can eavesdrop.
- **Integrity**: Messages cannot be tampered with.
- **Authenticity**: The server's identity is verified.

This layer above HTTP is what we call HTTPS ("HTTP over SSL/TLS").
