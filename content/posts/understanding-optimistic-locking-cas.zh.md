+++
date = '2025-12-07T00:00:00+08:00'
draft = false
title = '理解乐观锁 CAS 的非阻塞同步机制'
tags = ["并发编程", "Java"]
description = '如何在不加锁的情况下保证并发安全？'
+++

在并发编程的世界里，“线程安全”通常意味着“加锁”。从 `synchronized` 关键字到 `ReentrantLock`，我们已经习惯了通过排他性地锁定资源来确保数据一致性。然而，锁并非万能良药。在追求极致性能的场景下，锁带来的上下文切换和等待成本可能成为系统瓶颈。那么，有没有一种方法可以在不挂起（阻塞）线程的情况下，安全地在多线程间修改共享变量呢？

答案是肯定的。这就是**原子变量**（atomic variables）和**非阻塞同步算法**（Non-blocking Algorithms），也就是我们俗称的“乐观锁”。

## 第一部分：锁的代价

在传统的并发模型中，我们主要依赖阻塞锁。这种机制也被称为悲观锁：它假设最坏的情况，认为如果不锁定资源，其他线程一定会捣乱。虽然锁能保证安全，但在高并发场景下，它带来了两个主要的性能杀手：

1. **线程挂起与恢复的开销**：当一个线程无法获取锁时，它会被阻塞（挂起）。操作系统在挂起和恢复线程时需要进行上下文切换，这在高位性能场景下是非常昂贵的。
2. **活跃性问题**：阻塞锁可能导致死锁、优先级倒置和线程饥饿。

![锁的开销示意图](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_myqg4emyqg4emyqg.png)


对于简单的计数器自增操作，为此挂起和恢复线程就像为了喝杯水而关掉整个城市的供水系统一样——成本极度不成比例。对于涉及整数和对象引用变更的场景，我们需要一种更轻量、更“乐观”的方法。

## 第二部分：硬件级原子武器：CAS

Java 5.0 引入了 `java.util.concurrent` 包。原子类（如 `AtomicInteger`）和非阻塞数据结构（如 `ConcurrentLinkedQueue`）性能飞跃背后的秘密武器就是 **CAS (Compare-And-Swap)** 指令。

**什么是 CAS？**

CAS 是一种直接由 CPU 指令集支持的硬件原语（如 x86 的 `lock cmpxchg`）。它体现了乐观锁的哲学：我不加锁，直接尝试更新；如果更新失败（说明别人先到一步），我就重试或放弃，但我绝不挂起自己。

CAS 操作由三个核心步骤组成：

1. **读取旧值**：我看一眼内存里当前的值是多少。
2. **比较**：准备写入时，我再看一眼——内存里的值还是我刚才看到的那个吗？
3. **交换**：如果是，我就把它更新为新值（New Value）；如果不是，说明在此期间有其他线程修改了它，我的操作失败。

![CAS 工作原理图](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_d9qq9wd9qq9wd9qq.png)


我们可以用一段 Java 代码来模拟 CAS 逻辑（注意：真实的 CAS 是无锁的 CPU 指令，这里使用 `synchronized` 仅为了模拟其原子语义）：

```java
@ThreadSafe
public class SimulatedCAS {
    @GuardedBy("this") private int value;

    // 仅当内存中的值等于 expectedValue 时，才更新为 newValue
    public synchronized int compareAndSwap(int expectedValue, int newValue) {
        int oldValue = value;
        if (oldValue == expectedValue)
            value = newValue;
        return oldValue;
    }
}
```

**为什么 CAS 比锁快？**

锁的代价是**等待**（线程阻塞），而 CAS 的代价是**重试**（CPU 自旋）。在大多数情况下，对于 CPU 来说，重试几条指令的成本远低于挂起和调度线程的成本。

要使用 CAS，必须满足两个前提：

1. **持有旧值**：你必须知道你是基于哪个版本的数据进行修改的。
2. **能计算出新值**：CAS 是“比较+替换”，你必须在操作前准备好新值。

一旦掌握了 CAS，我们就可以构建**非阻塞算法**。这类算法的特点是：一个线程的失败或挂起，不会妨碍其他线程的继续工作。

以**非阻塞栈（Treiber Stack）**的 push 操作为例，我们可以看到 CAS 是如何工作的：

1. **读取**：获取当前栈顶节点 `oldHead`。
2. **计算**：创建新节点 `newHead`，并让 `newHead.next` 指向 `oldHead`。
3. **CAS**：原子性地尝试将栈顶从 `oldHead` 替换为 `newHead`。
   - **成功**：入栈完成。
   - **失败**：说明在第 1 步到第 3 步之间，有其他线程修改了栈顶。没关系，重新读取新栈顶，重复上述过程。

这种方式完全不需要锁。所有线程都全速运行，没有线程会被操作系统挂起，从而实现了极高的并发性能。

![非阻塞算法示意图](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_hf22vihf22vihf22.png)


## 第三部分：CAS 的陷阱：ABA 问题

虽然 CAS 强大，但它有一个逻辑漏洞：它只比较“值”是否相等，而不比较“值是否被修改过”。这就是 ABA 问题。

**什么是 ABA？**

想象以下场景：

1. 线程 T1 准备执行 CAS，发现变量的值为 **A**。
2. 线程 T2 动作很快，将变量从 **A** 改为 **B**，然后又改回了 **A**。
3. 线程 T1 执行 CAS，发现变量值依然是 **A**，于是认为“数据未变”，操作成功。

在某些场景下（特别是涉及指针复用或链表节点管理时），这可能导致严重的数据结构损坏。虽然值看起来没变，但“此 A 已非彼 A”——中间的状态变更丢失了。

![ABA 问题图解](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_y6hdu9y6hdu9y6hd.png)


**如何解决 ABA 问题？**

解决 ABA 问题的核心思路是增加版本号（Versioning）。如果我们不仅更新引用，还同步更新一个版本号，问题就迎刃而解了：

- 无版本号：`A -> B -> A`，CAS 无法察觉。
- 有版本号：`1A -> 2B -> 3A`。在执行 CAS 检查时，会发现虽然值还是 A，但版本号从 1 变为了 3，因此操作失败。

Java 提供了 `AtomicStampedReference` 类来实现带有版本号的原子引用更新，完美解决了 ABA 问题。

## 第四部分：虚拟线程时代的 CAS

回顾全文，我们可以得出结论：**CAS 是高性能并发的基石**。它避开了重量级的加锁机制，利用 CPU 级指令实现了高效的线程安全。Java 中所有的原子类（AtomicInteger、AtomicReference）以及高性能队列（ConcurrentLinkedQueue）底层都依赖它。在 Java 21+ 虚拟线程的新时代，CAS 的地位依然稳固吗？

答案是：**底层依然是核心，但业务层的统治地位有所下降。**

随着 Project Loom（虚拟线程）的引入，线程阻塞的成本变得极低（仅挂起虚拟线程而非内核线程）。在竞争极度激烈的场景下，简单的锁可能比 CAS 在高频自旋状态下更节省 CPU 资源。但无论如何，理解 CAS 就是理解并发编程的底层法则。
