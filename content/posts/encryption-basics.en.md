+++
date = '2024-04-28T13:34:26+08:00'
draft = false
title = 'Basic Methods of Information Encryption'
tags = ["Information Security"]
+++


### Overview

In the movie *The Imitation Game* (based on real events), the scientist Alan Turing led his team to crack the German communications encryption device "Enigma" after two years of intense effort. Finding a recurring phrase used by the Germans was the breakthrough that eventually led to decoding their messages—a feat that laid a solid foundation for victory in World War II. What was the technology used by the Germans? It's what we'll discuss today: data encryption. Data confidentiality refers to both encryption and decryption. In academic terms: **using an algorithm to change the original form of information so that even if an attacker steals the information, they cannot understand the real content without the corresponding decryption method.** Confidentiality can be applied in three stages:

1. On the client.
2. During transmission (the most complex and effective).
3. On the server.

### Strength of Encryption

In the security field, it's well-known that security has levels. Different applications have different sensitivity levels for Information, so they require different security levels. There is no such thing as "absolute safety"; you cannot maximize security levels infinitely. Any security measure can theoretically be cracked (with enough cost). Higher security comes with higher costs (workload, computing power, etc.). Common encryption techniques illustrate this point. Encryption strength ranges from low to high:

**1. Hash Algorithm**: The most common method. Using an irreversible digest algorithm like `MD5` on a plaintext password:

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MD5Hash {
    public static void main(String[] args) {
        String text = "yourPassword";
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] hashBytes = md.digest(text.getBytes());
            StringBuilder hexString = new StringBuilder();
            for (byte b : hashBytes) {
                hexString.append(String.format("%02x", b));
            }
            System.out.println("MD5 Digest: " + hexString.toString());
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }
}
```

Output:
```sh
MD5 Digest: 65a8e27d8879283831b664bd8b7f0ad4
```

This method has a low security level; weak passwords can be easily cracked by "rainbow tables" (pre-computed hash tables for reverse lookups).

**2. Salted Hash**: An enhancement where a `salt` value is added to confuse the hash calculation, effectively defending against rainbow table attacks:

```java
private static final String SALT = "YourFixedSalt";  // Fixed salt

private static String getSecurePassword(String passwordToHash) {
    String generatedPassword = null;
    try {
        MessageDigest md = MessageDigest.getInstance("MD5");
        // Add fixed salt
        md.update(SALT.getBytes());
        byte[] bytes = md.digest(passwordToHash.getBytes());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < bytes.length; i++) {
            sb.append(Integer.toString((bytes[i] & 0xff) + 0x100, 16).substring(1));
        }
        generatedPassword = sb.toString();
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();
    }
    return generatedPassword;
}
```

The downside is that if the salt is leaked, cracking ciphertext becomes easy again. Furthermore, with enough computing power, even salted weak passwords aren't impossible to crack.

**3. Salted Hash with Dynamic Salt**: Dynamic salt means each salt is used only once. This is like a certain restaurant I like where they promise "the oil is only used once"—essentially spending more for higher safety:

```java
public static void main(String[] args) {
    // Password to hash
    String passwordToHash = "yourPassword";
    // Generate dynamic salt
    byte[] salt = getSalt();
    // Get secure salted password
    String securePassword = getSecurePassword(passwordToHash, salt);
    System.out.println("Secure Password: " + securePassword);
    System.out.println("Salt: " + bytesToHex(salt));
}

// MD5 hash with salt
private static String getSecurePassword(String passwordToHash, byte[] salt) {
    try {
        MessageDigest md = MessageDigest.getInstance("MD5");
        // Add salt to digest
        md.update(salt);
        // Complete hash
        byte[] hashedBytes = md.digest(passwordToHash.getBytes());
        // Hex string conversion
        return bytesToHex(hashedBytes);
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();
        return null;
    }
}

// Generate random salt
private static byte[] getSalt() {
    SecureRandom sr = new SecureRandom();
    byte[] salt = new byte[16];
    sr.nextBytes(salt);
    return salt;
}

// Bytes to hex string
private static String bytesToHex(byte[] bytes) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bytes) {
        sb.append(String.format("%02x", b));
    }
    return sb.toString();
}
```

Dynamic salt solves the risks of fixed salt. However, if the client generates the salt for the server, **how to securely transmit the dynamic salt to the server** becomes the next question. If the channel is secure, transmitting the salt is unnecessary; if the channel is insecure, transmitting the salt is also risky. This is a "chicken and egg" problem.

**4. Enabling HTTPS**: This is the current mainstream solution. However, even with an HTTPS secure channel, risks remain—such as self-signed certificates causing leakage, delayed certificate updates, expiration issues, or weak encryption due to low TLS versions or poorly chosen cipher suites.

**5. External MFA**: Institutions like banks require external U-shields, virtual MFA, SMS verification, or face recognition for transactions. Critical enterprises or military agencies might even use an isolated internal network ("air-gap") to guarantee security.

The above examples illustrate that for security and confidentiality: **there is no absolute safety; higher security levels require higher costs.** One might joke that unplugging the network cable is safest, which has some logic, but such closed security is meaningless and outside our discussion.

### Client-side Encryption

For most apps, the only way to ensure secure communication is for the client to enable HTTPS. Furthermore, sensitive info like passwords should ideally be "destroyed" as early as possible on the client:

1. Server databases are frequently breached—leaks of millions of passwords are no longer news, and one of the largest domestic tech communities was famously hit.
2. Servers might log passwords; if log files leak or are collected, the passwords leak too.
3. Avoiding man-in-the-middle attacks; even if the network is hijacked, plaintext passwords aren't exposed.

In summary, plaintext passwords should be eliminated on the client. Don't send plaintext to the server where transmission risks are high. Besides HTTPS, the client should use hashing/summarizing for sensitive data. We'll discuss how to do this next.

### Creating and Verifying Ciphertext

As mentioned, there is no absolute safety. For most general applications, HTTPS is a suitable balance between security level and cost. Just choose a scheme that fits your situation.

#### BCrypt Algorithm

Regardless of how you hash plaintext, even with salt, there's always the possibility of brute-force cracking via rainbow tables. To solve this, **Slow Hash Functions** are an ideal solution. A slow hash function adds a `cost` parameter to the process. By extending the time and resources needed for each hash calculation, it effectively thwarts brute-force attacks. `BCrypt` is a representative slow hash:

```java
public class BCryptExample {

    public static void main(String[] args) {
        // Create instance, default work factor is 10
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

        // Encrypt password
        String originalPassword = "yourPassword";
        String encodedPassword = encoder.encode(originalPassword);
        System.out.println("Encoded Password: " + encodedPassword);

        // Verify password
        boolean isMatch = encoder.matches(originalPassword, encodedPassword);
        System.out.println("Password matched: " + isMatch);
    }
}
```

If we set the `cost` of a slow hash to 0.1 seconds, brute-forcing a 10-character weak password (consisting of 62 possible alphanumeric characters) would take approximately 26.61 million years. This shows that using BCrypt with an appropriate work factor significantly increases the difficulty of cracking passwords, making brute-force methods infeasible. However:

> BCrypt consumes considerable time and computing resources, which can significantly lower server performance. It is recommended to perform the slow hash on the client.

#### Creating Ciphertext (Registration)

For the encryption stage, refer to this process:

![Creating Ciphertext](https://s2.loli.net/2025/02/13/9HTgMAVjRWQDNPq.png)

1. User creates a password; client receives the plaintext.
2. Client encrypts the password using a fixed salt + BCrypt (Slow Hash) and sends it to the server.
3. Server receives the ciphertext, generates a random salt, and encrypts it again.
4. Server stores the random salt and double-encrypted ciphertext in the database.

#### Verifying Ciphertext (Login)

For the verification stage, refer to this process:

![Verifying Ciphertext](https://s2.loli.net/2025/02/13/igYrDznvLbwfHIl.png)

1. User enters a password; client receives the plaintext.
2. Client encrypts it using a fixed salt + BCrypt (Slow Hash) and sends it to the server.
3. Server receives the client's ciphertext and retrieves the random salt and double-encrypted ciphertext from the database.
4. Server encrypts the client's ciphertext with the random salt and compares it with the double-encrypted ciphertext from the DB.
5. If they match, the password is correct.
