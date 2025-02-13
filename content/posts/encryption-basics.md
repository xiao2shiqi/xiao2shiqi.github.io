+++
date = '2024-04-28T13:34:26+08:00'
draft = true
title = '信息加密的基本方法'
tags = ["信息安全"]
+++

### 概述

在我很喜欢的一部（根据真实事件改编）的电影《模仿游戏》里面：著名的科学家图灵带领他的团队，花费两年的时间，费劲九牛二虎之力，在找到德军的话术口令后才得以破解了德军通讯加密装置 “英格玛”，为第二次世界大战取得胜利打下的坚实的基础。那么德军使用的通讯加密究竟是一种怎样的技术，这是我们今天要探讨的数据加密技术。数据的保密是对数据加密、解密的统称，用学院派的说法就是，\*\*使用某种算法改变了信息原本的形态，使攻击者即使窃取了信息也因为没有对应的解密的方法也无法获取当信息的真实内容。\*\*这就是信息保密的目的，对于信息的保密，可以在三个环节进行，分别是：

1.  在客户端进行保密
2.  在传输时进行保密（最复杂，也最有效）
3.  在服务端进行保密



### 加密的强度

在安全领域大家都知道安全是区分等级的，不同应用的敏感信息重要性不同，所以需要的安全等级也不同，这个世界上没有绝对的安全，安全等级不可能无止境的拉满，任何安全手段都可以破解（只要花费足够的成本），想要更高级别的安全等级，就要付出更高的成本（工作量，算力）等。例如常见的加密技术可以说明这一点。加密的强度从低到高，分别有：

一：哈希算法：最常见的加密手段，对明文密码使用 `MD5` 等哈希摘要算法进行不可逆的哈希计算进行加密，示例：

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

输出结果：

```sh
MD5 Digest: 65a8e27d8879283831b664bd8b7f0ad4
```

这种方式，安全等级低，弱密码容易被彩虹表（预先进行摘要好的哈希表，进行反向破译）破击。

二：哈希算法加盐：增强了基础的哈希算法，加上 `salt` 盐值混淆哈希计算，可以有效防御彩虹表的攻击，示例：

```java
private static final String SALT = "YourFixedSalt";  // 固定盐值

private static String getSecurePassword(String passwordToHash) {
    String generatedPassword = null;
    try {
        MessageDigest md = MessageDigest.getInstance("MD5");
        // 添加固定盐值
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

这种方案的缺点是，但如果盐值泄露，那么破译所以密文也是一件很容易得事情，而且弱密码即使加了盐值，在强大算力的彩虹表面前，破译也不是一件难事。

三：动态盐加哈希：动态盐值有一个特点，就是每个盐值只使用一次，这种方式有点像就像我喜欢吃的那家酸菜鱼，他们家宣传的口号就是：油每次只用一次，本质上就是花费更高的成本换来更高的安全。示例：

```java
public static void main(String[] args) {
    // 待加密的密码
    String passwordToHash = "yourPassword";
    // 生成动态盐值
    byte[] salt = getSalt();
    // 获取带盐的安全密码
    String securePassword = getSecurePassword(passwordToHash, salt);
    System.out.println("Secure Password: " + securePassword);
    System.out.println("Salt: " + bytesToHex(salt));
}

// 使用MD5加密密码，并结合盐值
private static String getSecurePassword(String passwordToHash, byte[] salt) {
    try {
        // 创建MD5摘要算法的 MessageDigest 对象
        MessageDigest md = MessageDigest.getInstance("MD5");
        // 将盐值添加到摘要中
        md.update(salt);
        // 完成密码的哈希计算
        byte[] hashedBytes = md.digest(passwordToHash.getBytes());
        // 将哈希值转换为十六进制字符串
        return bytesToHex(hashedBytes);
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();
        return null;
    }
}

// 生成一个随机的盐值
private static byte[] getSalt() {
    SecureRandom sr = new SecureRandom();
    byte[] salt = new byte[16];
    sr.nextBytes(salt);
    return salt;
}

// 将字节数组转换为十六进制字符串
private static String bytesToHex(byte[] bytes) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bytes) {
        sb.append(String.format("%02x", b));
    }
    return sb.toString();
}
```

动态盐值可以解决固定盐值带来的风险，如果由客户端动态生成盐值给服务端进行计算，那么 **客户端如果安全的把动态盐值传输给服务端** 就是另外一个问题，既然通信的信道是安全可靠的，那么传输动态盐值就没有意义，既然通信信道是不安全的，那么传输动态盐值也有被窃听的风险，也没有意义。这简直就是一个 “先有鸡，还是先有蛋” 的问题。

四：启动 HTTPS 信道：HTTPS 加密传输是目前的主流方案，但是启动 HTTPS 后安全信道后也并不能高枕无忧，也会带来一系列的问题，例如因为会遇到服务端使用自签名证书导致信息泄露风险，服务端证书更新不及时，证书过期的问题，还有 TLS 版本过低或密码学套件选用不当产生加密强度不足的风险。

五：外置的 MFA：例如银行等机构在涉及金额交易的时候，会要求客户使用外置的 U 盾，虚拟 MFA，手机验证码，人脸识别等外置设备来加强安全等级。一些关键企业或者军事机构甚至会开辟一条与公网隔绝的独立的内部网络进行信息通信来保证信息的安全。

通过以上示例是想要证明，对于安全和保密而言：**这个世界上是没有绝对的安全，想要更高级别的安全等级，就要付出更高的成本** ，当然有人会挑刺的说，那我拔掉网线不联网最安全，虽然有一定的合理性，但这样封闭式的安全没有意义，所以不在我们讨论的范围之内。

### 客户端加密

对于大多数应用而言，要保证信息通信的安全，客户端只有启用 HTTPS 这一个方案可以选择。而且对于密码这样的敏感信息而言，个人认为最好是在客户端就可以尽快处理掉，以绝后患，原因如下：

1.  服务端存储明文密码，数据库被攻破导致用户密码泄露的新闻已经屡见不鲜的，而且被拖库最严重的还是国内某最大的技术社区。。。
2.  服务端把密码输入到日志，日志文件泄露或者被采集，导致用户密码泄露等等
3.  避免中间人攻击，就算网络设备被劫持，信息被窃取，至少明文密码不会泄露

总之，明文密码最好在客户端就被消灭掉，越早处理越好，不要把明文传到服务端，传输的风险大，在防御上客户端除了启用 HTTPS 外，还要对明文密码进行摘要处理，从而保证敏感的安全。至于客户端应该如何进行加密，我们接下来开始讨论。

### 密文的创建和校验

之前说了在信息安全领域没有绝对的安全，需要多高的安全等级就要消耗多大的安全成本。对于大多数普遍的应用而言，启动 HTTPS 加密通信是在安全等级和安全成本之间的一个合适的平衡点。所以结合实际情况选择合适的方案就好。

#### BCrypt 算法

上面介绍无论如何对明文进行哈希计算，就算加盐都有被彩虹表暴力破解的可能。为了解决这个问题，引入慢哈希函数来解决可能是一个更理想的方案。慢哈希，就是在哈希计算和 `salt` 盐值之外增加一个计算时间 `cost` 的参数，慢哈希通过延长哈希计算时间和消耗的资源来有效的避免诸如彩虹表等暴力破解的攻击，提供系统的安全性，`BCrypt` 算法就是一个具有代表性的慢哈希函数。示例：

```java
public class BCryptExample {

    public static void main(String[] args) {
        // 创建 BCryptPasswordEncoder 实例，可以指定工作因子，默认是 10
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

        // 加密密码
        String originalPassword = "yourPassword";
        String encodedPassword = encoder.encode(originalPassword);
        System.out.println("Encoded Password: " + encodedPassword);

        // 校验密码
        boolean isMatch = encoder.matches(originalPassword, encodedPassword);
        System.out.println("Password matched: " + isMatch);
    }
}
```

如果我们把慢哈希计算的 `cost` 设置为 0.1 秒的时间，那么对所有由10位大小写字母和数字组成的弱密码（共62种字符）进行哈希计算一次，大约需要 8.39×10168.39×1016 秒。这等于大约 971.4 亿天，或者大约 2661 百万年的时间。这表明使用 BCrypt 和适当的工作因子可以极大增加破解密码的难度，使得暴力破解方法变得不可行。但是需要注意的是：

> BCrypt 存在对计算资源和时间有很大的消耗，会明显降低服务端性能，只建议在客户端进行慢哈希处理

#### 密文的创建

对于敏感信息加密阶段，可以参考以下方案进行处理：

![密文的创建](https://s2.loli.net/2025/02/13/9HTgMAVjRWQDNPq.png)

1.  用户创建密码，客户端接收用户的明文密码
2.  客户端对密码使用固定盐值 + BCrypt 慢哈希进行加密后发给服务端
3.  服务端接收密文，然后生成随机盐值，对密文进行二次加密
4.  服务端将随机盐和二次密文存储到数据库

#### 密文的校验

在对密文进行校验阶段，可以参考以下方案进行处理：

![密文的校验](https://s2.loli.net/2025/02/13/igYrDznvLbwfHIl.png)

说明：

1.  用户输入密码，客户端收到用户的明文密码
2.  客户端对密码使用固定盐值 + BCrypt 慢哈希进行加密后发给服务端
3.  服务端接收客户端密文，然后从数据库取出随机盐和二次密文
4.  服务端使用随机盐对客户端密文进行加密，然后和自身的二次密文进行对比
5.  密文内容相同，则表示密码校验通过
