+++
date = '2024-04-28T13:34:26+08:00'
draft = false
title = 'Basic Methods of Information Encryption'
tags = ["Information Security"]
+++

### Overview

In the movie *The Imitation Game* (based on real events), the scientist Alan Turing led his team to crack the German communications encryption device "Enigma" after two years of intense effort. This feat laid a solid foundation for the victory in World War II. Today, we will discuss the data encryption technology behind such communications.

Data confidentiality refers to encryption and decryption. In academic terms: **using an algorithm to change the original form of information so that even if an attacker steals the information, they cannot understand it without the corresponding decryption method.** Confidentiality can be applied in three stages:
1. On the client.
2. During transmission (the most complex and effective).
3. On the server.

### Strength of Encryption

In the field of security, there is no "absolute safety." Security levels are based on the importance of the sensitive information. Higher security levels come with higher costs (workload, computing power).

Encryption strength ranges from low to high:

**1. Hash Algorithm**: The most common method. Using algorithms like MD5 to perform irreversible hash calculations on plaintext passwords.

```java
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] hashBytes = md.digest(text.getBytes());
// ... convert to hex string
```

This method is low-security. Weak passwords can be easily cracked by "rainbow tables" (pre-computed hashes).

**2. Salted Hash**: An enhancement where a "salt" is added to the hash calculation to defend against rainbow table attacks.

```java
// Adding a fixed salt
md.update(SALT.getBytes());
byte[] bytes = md.digest(passwordToHash.getBytes());
```

The downside is that if the salt is leaked, cracking becomes easy again.

**3. Salted Hash with Dynamic Salt**: Each salt is used only once.

```java
byte[] salt = getSalt(); // Generate random salt
String securePassword = getSecurePassword(passwordToHash, salt);
```

Dynamic salt solves the risk of fixed salt leakage. However, it introduces a "chicken and egg" problem: how do you securely transmit the dynamic salt from the client to the server?

**4. Enabling HTTPS**: This is the mainstream solution for secure communication today. However, even with HTTPS, one can face risks like self-signed certificates, expired certificates, or outdated TLS versions.

**5. External MFA**: Institutions like banks use external U-shields, virtual MFA, SMS codes, or face recognition to boost security.

### Client-side Encryption

For most apps, client-side encryption is essential. Sensitive information like passwords should be handled as early as possible on the client for several reasons:

1. Server databases are frequently breached, leading to mass password leaks.
2. Servers might accidentally print passwords to logs.
3. To avoid man-in-the-middle attacks where plaintext passwords could be intercepted.

In short, never transmit plaintext passwords to the server.

### Creating and Verifying Ciphertext

#### BCrypt Algorithm

To solve the vulnerability of simple hashing to rainbow table attacks, **Slow Hash Functions** were introduced. A slow hash function adds a `cost` parameter to the calculation, extending the time and resources required for each hash, making brute-force attacks infeasible. `BCrypt` is a representative slow hash.

```java
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
String encodedPassword = encoder.encode(originalPassword);
boolean isMatch = encoder.matches(originalPassword, encodedPassword);
```

If a slow hash takes 0.1 seconds, brute-forcing a 10-character weak password could take millions of years. However, BCrypt is resource-intensive and is often recommended for use on the client to avoid overloading the server.

#### Creating Ciphertext (Registration)
1. Client receives the plaintext password.
2. Client encrypts it using a fixed salt + BCrypt (Slow Hash).
3. Server receives the ciphertext, generates a random salt, and encrypts it again.
4. Server stores the random salt and final ciphertext in the database.

#### Verifying Ciphertext (Login)
1. Client encrypts the plaintext using fixed salt + BCrypt.
2. Server receives the client's ciphertext and retrieves the random salt from the database.
3. Server encrypts the client's ciphertext using the random salt and compares it with the stored value.
4. If they match, the password is correct.
