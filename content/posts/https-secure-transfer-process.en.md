+++
date = '2024-05-07T13:20:19+08:00'
draft = false
title = 'Main Process of HTTPS Transport Encryption'
tags = ["Information Security"]
+++


### Overview

Modern cryptography primarily handles information in the following three forms:

1.  **Digest**: Primarily used for data validation (e.g., storing passwords). A digest is a one-way hash that changes the original form of information. Hash functions are characterized by their sensitivity—even a tiny change produces a completely different hash value—and the fact that they cannot be reversed. Common examples include `MD4/5`, `SHA-1`, `SHA-256/512`, etc.
2.  **Encryption**: Primarily used to ensure secure transmission, making sure the real information is only accessible by authorized parties (who hold the key). Unlike digests, encrypted information can be decrypted back to plaintext using a key. Key types include symmetric and asymmetric (public and private keys). Common algorithms include `DES`, `AES`, `RC4`, `IDEA`, etc.
3.  **Signature**: Primarily used to guarantee the integrity and authenticity of plaintext information and to check if it has been tampered with (using hash functions). For example, a `JWT token` contains a signature to guarantee the authenticity of the payload. A signature does not guarantee the privacy of the information itself.

**Overall, their roles are:**
- **Digest**: Used to ensure data integrity and for quick comparison; cannot be decrypted.
- **Encryption**: Used to protect data confidentiality; unlike a digest, it can be reversed (decrypted).
- **Signature**: Provides a method to verify the source and integrity of a message, though the message itself is public.

These three elements form the foundation of modern cryptography and are widely used in data protection, identity authentication, and network security.

### Keys

#### Symmetric Keys

![Symmetric Encryption](https://s2.loli.net/2025/02/13/oJPagjRvX3O1uZb.jpg)

The basic principle of symmetric encryption is to convert plaintext into ciphertext using an encryption algorithm and a key; the receiver then uses the same key and decryption algorithm to restore the original plaintext. Because the same key is used for both, it is called symmetric encryption. These algorithms are simple and fast, making them suitable for large amounts of data. Common examples: **AES (Advanced Encryption Standard)**, **DES (Data Encryption Standard)**, **3DES (Triple DES)**.

Symmetric keys face difficulties in storage and distribution because the key must be shared securely with all parties, and a new key might be needed for every communication, which becomes complex at scale.
*   **Pros**: Fast encryption/decryption, suitable for large data, simple algorithm, low resource consumption.
*   **Cons**: Key storage and distribution are difficult; they cannot be distributed over an untrusted network, creating a "chicken and egg" problem.

#### Asymmetric Keys

![Asymmetric Encryption](https://s2.loli.net/2025/02/13/LSTVGgFCwNEM3dP.png)

Asymmetric encryption, also known as public-key encryption, uses two different keys: one for encryption (the public key) and one for decryption (the private key). The public key can be shared openly, while the private key must remain secret.

The basic principles are:
1.  **Key Generation**: A pair of keys—one public, one private—is generated. They are mathematically related, but the private key cannot be easily derived from the public key.
2.  **Encryption**: When Party A wants to send information to Party B, A uses B's public key to encrypt it. Thus, only B, who holds the corresponding private key, can decrypt it.
3.  **Decryption**: After receiving the ciphertext, B uses their private key to restore the original message.

The key feature is that the public key is open while the private remains secret. While useful, the main downside is computational complexity and high resource consumption. Therefore, it's often combined with symmetric encryption: asymmetric encryption is used to safely exchange a symmetric key, which then handles the actual data transfer. This solves the problem of two untrusted parties communicating in an insecure environment.
*   **Pros**: Solves key distribution issues; allows secure information transfer over public networks.
*   **Cons**: Slow, unsuitable for large data, high resource consumption, and has length limits (a key of a certain length can only encrypt plaintext of a matched length).

Thus, the distinction between symmetric and asymmetric keys exists to meet different security needs, improve efficiency, and simplify key management. Neither alone manages all aspects of encryption and signatures. **In practice, symmetric and asymmetric encryption are combined—using hybrid encryption to protect channel security.**

**Specific Approach:**
1.  Use asymmetric encryption to negotiate a common key (small amount of info).
2.  Both parties use that shared key for symmetric encryption to transmit large amounts of data.

This hybrid approach, utilizing the strengths of both, is known as a modern cryptographic suite. HTTPS, the ultimate solution for information transfer, is based on this method.

### Certificates

In real life, establishing trust with a stranger usually happens in two ways:
1.  **Based on shared private information**: Someone calls claiming to be a school friend and mentions a specific classmate's name or an embarrassing story only we know; then I trust them.
2.  **Based on an authorized notary**: Someone claims to be a police officer and provides a badge and ID number; we trust and cooperate with them based on that authority.

In the network world, we cannot assume two computers recognize each other or share secret info. Thus, trust is solved via the second way: **the authorized notary.**

#### CA (Certificate Authority)

A CA is an organization responsible for issuing digital certificates to server side—similar to the authority that issues IDs to police. When a client visits a server, it checks if the certificate is valid, and only then is a secure link established.

![Secure Link Icon](https://s2.loli.net/2025/02/13/vNJxOcLuSWqi2aH.png)

Server PKI certificates follow the X.509 standard. They contain the following information for SSL/TLS communication:

![Digital Certificate](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/915e86f9832944e8adae8f43cdd56cf3~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1180&h=1412&s=208395&e=png&a=1&b=fbfbfb)

1.  **Version**: The X.509 version used (1, 2, or 3).
2.  **Serial Number**: A unique identifier assigned by the CA.
3.  **Signature Algorithm**: The algorithm used for the certificate's digital signature.
4.  **Issuer**: The name of the CA that issued the certificate.
5.  **Validity**: The period (start and end dates) the certificate is valid.
6.  **Subject**: The name of the certificate holder—usually the domain name, unique across the network.
7.  **Subject Public Key Info**: The public key and associated algorithm provided by the CA to the holder.
8.  **Extensions**: Additional attributes for later scalability.

### Secure Transport Protocol

The keys and certificates discussed above are ultimately meant for secure transmission. Engineers face the challenge of applying these complex technologies invisibly to all web users. SSL/TLS has evolved over years of exploration since 1994:
1.  **1994: Introduction of SSL** – Developed by Netscape to provide a secure transport mechanism for web transactions.
2.  **1999: Birth of TLS** – TLS 1.0 was released as the successor to SSL, standardized by the IETF. It was similar to SSL 3.0 but fixed several flaws.
3.  **2006: TLS 1.1** – Further enhanced security, such as introducing explicit IVs to prevent cipher-block chaining attacks.
4.  **2008: TLS 1.2** – Added more encryption algorithms and security features, like support for SHA-256.
5.  **2018: TLS 1.3** – Simplified the handshake process, improving speed and security by removing outdated algorithms.

The TLS handshake involves two rounds and four communications, as shown below:

![TLS 4-Way Handshake](https://s2.loli.net/2025/02/13/8xXKaDHfkt15Ndm.png)

1.  **ClientHello**: The client sends a message in plaintext including supported TLS versions, cipher suites, a session ID, and a random number generated by the client.
2.  **ServerHello**: The server chooses a common TLS version and cipher suite and responds with its own random number and session ID.
3.  **Client Finished**: The client verifies the certificate. If valid, it calculates a `MasterSecret` (using a specific algorithm) to be the symmetric key, sends a 32-bit random number, a cipher change notification, and a verification of the handshake integrity.
4.  **Server Finished**: The server responds with final confirmations, including a cipher change notification and a "handshake finished" notice.

Through this four-way handshake, a TLS secure connection is established. The parties negotiate information such as a random key known only to them, the symmetric encryption algorithm (e.g., AES 128), and compression algorithms. The result:
- All information is protected from eavesdropping (encryption).
- Information cannot be tampered with (integrity checks).
- Information cannot be spoofed (certificate authentication).

For users, functionality remains identical despite a slight performance drop. The HTTP protocol built on top of this safety layer is known as "HTTP over SSL/TLS"—more commonly known as HTTPS.
