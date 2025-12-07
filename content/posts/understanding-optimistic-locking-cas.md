+++
date = '2025-12-07T00:00:00+08:00'
draft = false
title = '理解乐观锁 CAS 的非阻塞同步机制'
tags = ["并发编程", "Java"]
description = '不用锁，如何保证并发安全 ？'
+++

在并发编程的世界里，"线程安全"通常意味着"加锁"。从 `synchronized` 关键字到 `ReentrantLock`，我们习惯了通过独占资源来保证数据的一致性。然而，锁并非银弹。在追求极致性能的场景下，锁带来的上下文切换和等待成本可能成为系统的瓶颈。那么，有没有一种方法，既不需要让线程挂起（阻塞），又能保证多线程安全地修改共享变量？

答案是肯定的。这就是 原子变量 与 非阻塞同步算法（Non-blocking Algorithms）。也就是常说的乐观锁。

## 一、锁的代价

在传统的并发模型中，我们主要依赖阻塞锁（Blocking Locks）。这种机制也被称为悲观锁：它假设最坏的情况，认为如果不锁住资源，别的线程一定会来捣乱。虽然锁能确保安全，但在高并发场景下，它带来了两个显著的性能杀手：

1. **线程挂起与恢复的开销**：当一个线程获取不到锁时，它会被阻塞（挂起）。操作系统在挂起和恢复线程时，需要进行上下文切换，这在高性能场景下是极其昂贵的操作。
2. **活跃性问题**：阻塞锁可能导致死锁（Deadlock）、优先级反转（Priority Inversion）以及线程饥饿。

![Gemini_Generated_Image_myqg4emyqg4emyqg](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_myqg4emyqg4emyqg.png)

如果是简单的计数器累加操作，为了这就把线程挂起再恢复，就像是为了喝一杯水而关停整个城市的供水系统一样，成本极其不匹配。在面对整数和对象引用变更这种场景，我们需要的，是一种更轻量级、更“乐观”的方法。

## 二、 硬件级的原子武器：CAS

Java 5.0 引入了 `java.util.concurrent` 包，其中的原子类（如 `AtomicInteger`）和非阻塞数据结构（如 `ConcurrentLinkedQueue`）带来性能飞跃的秘密武器，就是 **CAS（Compare-And-Swap）** 指令。

**什么是 CAS ？**

CAS 是一种硬件原语，它由 CPU 的指令集直接支持（如 x86 的 `lock cmpxchg`）。它体现了一种乐观锁的哲学：我不加锁，我直接尝试更新；如果更新失败（说明被人抢先了），我再重试或者放弃，但我绝不挂起自己。

CAS 的操作包含三个核心步骤：

1. 读取旧值（Old Value）：我看一眼当前内存里的值是多少。
2. 比较（Compare）：在准备写入时，我再看一眼，现在内存里的值还是我刚才看到的那个吗？
3. 交换（Swap）：如果是，我就把它更新为新值（New Value）；如果不是，说明这期间有别的线程改过它，我这次操作失败。

![Gemini_Generated_Image_d9qq9wd9qq9wd9qq](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_d9qq9wd9qq9wd9qq.png)

我们可以用一段 Java 代码来模拟 CAS 的逻辑（注意：真实 CAS 是无锁的 CPU 指令，这里用 synchronized 只是为了模拟其原子性语义：

```java
@ThreadSafe
public class SimulatedCAS {
    @GuardedBy("this") private int value;

    // 只有当内存中的 value 等于 expectedValue 时，才将其更新为 newValue
    public synchronized int compareAndSwap(int expectedValue, int newValue) {
        int oldValue = value;
        if (oldValue == expectedValue)
            value = newValue;
        return oldValue;
    }
}
```

**为什么 CAS 比锁快？**

锁的成本是**等待**（线程阻塞），而 CAS 的成本是**重试**（CPU 空转）。在大多数情况下，对于 CPU 而言，重试几条指令的成本远比将线程挂起并调度的成本要低得多。

要使用 CAS，你必须满足两个前提条件：

1. **持有旧值（Old Value）**：你必须知道你基于哪个版本的数据在做修改。
2. **能计算出新值（New Value）**：CAS 是“比较+替换”，你必须在操作前就把新值准备好。

在掌握了 CAS，我们就可以构建**非阻塞算法（Non-blocking Algorithm）**。这种算法的特点是：某个线程的失败或挂起，不会导致其他线程也无法工作。

以一个 **非阻塞栈（Treiber Stack）** 的入栈（push）操作为例，我们可以看到 CAS 是如何工作的：

1. **读取**：获取当前栈顶节点 `oldHead`。
2. **计算**：创建一个新节点 `newHead`，并让 `newHead.next` 指向 `oldHead`。
3. **CAS**：原子地尝试将栈顶从 `oldHead` 替换为 `newHead`。
   - **成功**：入栈完成。
   - **失败**：说明在第1步和第3步之间，有别的线程修改了栈顶。没关系，重新读取新的栈顶，重复上述过程。

![Gemini_Generated_Image_hf22vihf22vihf22](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_hf22vihf22vihf22.png)

这种方式不需要任何锁，所有线程都在全速奔跑，没有任何线程会被操作系统挂起，从而实现了极高的并发性能。



## 三、CAS 隐患：ABA 问题

CAS 虽然强大，但它有一个逻辑漏洞：它只比较“值”是否相等，而不比较“值是否被修改过”。那就是 ABA 问题。

1. 什么是 ABA？

想象以下场景：

1. 线程 T1 准备执行 CAS，它看到变量的值是 **A**。
2. 线程 T2 动作很快，把变量从 **A** 改成了 **B**，然后又改回了 **A**。
3. 线程 T1 执行 CAS，它发现变量的值还是 **A**，于是判定“数据未变”，CAS 操作成功。

在某些场景下（尤其是涉及指针重用或链表节点管理时），这会导致严重的数据结构损坏。虽然看起来值没变，但“此 A 非彼 A”，中间经历的状态变化丢失了。

![Gemini_Generated_Image_y6hdu9y6hdu9y6hd](/images/posts/understanding-optimistic-locking-cas/Gemini_Generated_Image_y6hdu9y6hdu9y6hd.png)

那么如何解决 ABA 问题 ？

解决 ABA 问题的核心思路是加版本号（Versioning） 。如果我们不仅更新引用，还同时更新一个版本号，问题就迎刃而解：

- 不加版本：`A -> B -> A`，CAS 无法识别。
- 加版本：`1A -> 2B -> 3A`。CAS 检查时会发现，虽然值还是 A，但版本号从 1 变成了 3，因此操作失败。

Java 提供了 `AtomicStampedReference` 类来实现带有版本号的原子引用更新，从而彻底解决 ABA 问题。

## 四、虚拟线程时代的 CAS

回顾全文，我们可以得出结论：**CAS 是实现高性能并发的基石**。它避开了重量级的锁机制，利用 CPU 底层指令实现了高效的线程安全。Java 中所有的原子类（AtomicInteger, AtomicReference）以及高性能队列（ConcurrentLinkedQueue）底层都依赖于它。在未来 Java 25 + 虚拟线程（Virtual Threads） 的新时代，CAS 的地位依然稳固吗？

答案是：**CAS 依然是底层核心，但在业务层的统治力有所下降。**

随着 Project Loom（虚拟线程）的引入，线程阻塞的成本变得极其低廉（只挂起虚拟线程，不挂起内核线程）。在超高竞争的场景下，简单的锁可能比处于激烈自旋状态的 CAS 更节省 CPU 资源。但无论如何，CAS 依然是 JVM 内部实现、高层并发抽象（如 Virtual Threads 调度本身）的最底层原语。理解 CAS，就是理解并发编程的物理定律。
