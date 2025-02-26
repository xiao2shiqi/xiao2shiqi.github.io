+++
date = '2023-04-17T14:24:51+08:00'
draft = false
title = 'Redis Stream：更完善的消息队列'
tags = ["Redis", "数据库"]
+++



> 该数据结构需要 Redis 5.0.0 + 版本才可用使用

### 概述

Redis stream 是 Redis 5 引入的一种新的数据结构，它是一个高性能、高可靠性的消息队列，主要用于异步消息处理和流式数据处理。在此之前，想要使用 Redis 实现消息队列，通常可以使用例如：列表，有序集合、发布与订阅 3 种数据结构。但是 stream 相比它们具有以下的优势：

* 支持范围查找：内置的索引功能，可以通过索引来对消息进行范围查找
* 支持阻塞操作：避免低效的反复轮询查找消息
* 支持 ACK：可以通过确认机制来告知已经成功处理了消息，保证可靠性
* 支持多个消费者：多个消费者可以同时消费同一个流，Redis 会确保每个消费者都可以独立地消费流中的消息

话不多说，接下来具体看看如何使用它。（PS：万字长文，行驶途中请系好安全带）



### XADD 添加元素

XADD 命令的语法格式如下：

```perl
XADD stream-name id field value [field value]
```

* stream-name: 指定 redis stream 的名字
* id: 是指 stream 中的消息 ID，通常使用 `*` 号表示自动生成
* field value: 就是消息的内容，是 K-V 格式的键值对

关于使用 XADD 添加元素，还有以下特点：

* 自动创建流：当 `my-stream` 流不存在时，redis 会自动创建，然后将元素追加在流的末尾处
* 任意键值对：流中的每个元素可以包含一个或任意多个键值对



下面是一个使用 XADD 命令添加新消息的示例：

```perl
XADD my-stream * name John age 30 email john@example.com
```

上述命令的说明：

1. 向名为 `my-stream` 的 Redis stream 中添加了一条新消息。
2. `*` 表示使用自动生成的消息 ID，
3. `name`、`age` 和 `email` 是消息的字段名
4. `John`、`30` 和 `john@example.com` 是消息的字段值。



#### 流元素 ID

XADD 命令在成功执行后会返回元素 ID 作为结果：

```perl
"1681138020163-0"
```

每个元素的 ID 是一个递增的唯一标识符，由两部分组成：一个时间戳和一个序列号。

* 时间戳部分是一个 64 位的有符号整数，以毫秒为单位表示自 Unix 时间起经过的毫秒数。
* 序列号部分是一个递增的整数，从 0 开始逐步增加。



为了证明，我们可以指定消息 ID 向指定流中发送一条消息：

```sh
XADD my-stream 1681138020163-1 name Mary age 25 email mary@example.com
```

返回结果：

```sh
"1681138020163-1"
```

最后，可以提前使用 `XRANGE` 指令查看推入流中的数据

```sh
XRANGE my-stream - +
```

返回结果：

```sh
1) 1) "1681138020163-0"
   2) 1) "name"
      2) "John"
      3) "age"
      4) "30"
      5) "email"
      6) "john@example.com"
2) 1) "1681138020163-1"
   2) 1) "name"
      2) "Mary"
      3) "age"
      4) "25"
      5) "email"
      6) "mary@example.com"
```



#### 流元素 ID 的限制

元素 ID 在 Redis stream 中扮演着非常重要的角色，它不仅保证了元素的唯一性和顺序性，还提供了高效的范围查询和分析功能。在使用 Redis stream 时，需要特别注意元素 ID 的限制，并保证 ID 的唯一性和递增性。

限制如下：：

* ID 必须是唯一的
* 新元素的 ID 必须比流中所有已有元素的 ID 都要大

还有一些长度和特殊字符的限制等等，不符合上述限制的添加元素操作，会被 redis 拒绝，并且返回一个错误等。



**最大元素 ID 是如何更新的 ?**

在成功执行XADD命令之后，流的最大元素ID也会随之更新。



**为什么要限制 新元素的 ID 必须比流中所有已有元素的 ID 都要大 ？**

限制新元素的 ID 必须比流中所有已有元素的 ID 都要大，是为了保证 stream 中每个元素的唯一性和顺序性。这种特性对于使用流实现消息队列和事件系统的用户来说是非常重要的：用户可以确信，新的消息和事件只会出现在已有消息和事件之后，就像现实世界里新事件总是发生在已有事件之后一样，一切都是有序进行的。



#### 自动生成 ID 的规则

示例开始就演示自动生成消息向流中推送数据，在日常使用非常方便，这里说一下它的生成规则：

1. 时间戳部分是当前时间的毫秒数。表示自 Unix 时间起经过的毫秒数
2. 序列号从 0 开始递增。序列号是一个 64 位的整数，从 0 开始递增



#### 限制流长度

流的数据大多只是临时保存的，如果不对流的长度进行限制，会出现以下情况：

1. 存储耗尽：随着流中消息的增加，占用的内存也会相应增加。长时间运行的应用程序可能会面临内存耗尽的风险
2. 影响性能：随着数据越多，查询和操作流的速度会更慢，维护也更困难

为了避免该问题，在使用 Redis stream 时，可以使用 MAXLEN 选项指定 stream 的最大长度，命令格式如下：

```sh
XADD stream [MAXLEN len] id field value [field value ...]
```

示例：

```sh
XADD mini-stream MAXLEN 3 * k1 v1
XADD mini-stream MAXLEN 3 * k2 v2
XADD mini-stream MAXLEN 3 * k3 v3
XADD mini-stream MAXLEN 3 * k4 v4

# 我们向一个限制长度为 3 的 `mini-stream` 流中添加 4 条数据，然后查看流内的消息：
XRANGE mini-stream - +
1) 1) "1681140898447-0"
   2) 1) "k2"
      2) "v2"
2) 1) "1681140901790-0"
   2) 1) "k3"
      2) "v3"
3) 1) "1681140906703-0"
   2) 1) "k4"
      2) "v4"
```

最后会看到最早创建的 `k1` 消息已经被移除，redis 删除在流中存在时间最长的元素，从而来保证流的整体长度。



### XTRIM 限制流

除了在 XADD 命令时限制流，Redis 还提供单独限制流长度的 MAXLEN 命令，基础语法如下：

```sh
XTRIM stream MAXLEN len
```

示例：

```sh
XTRIM my-stream MAXLEN 2
(integer) 1
```

这条命令 `XTRIM my-stream MAXLEN 2` 的作用是将名为 `my-stream` 的流修剪为最多包含 2 条消息。换句话说，流中超出这个长度的较旧消息将被移除。



### XDEL 移除元素

XDEL 用于从流中删除特定的消息。这个命令需要提供流的键（key）和一个或多个消息 ID 作为参数。当消息被成功删除时，`XDEL` 命令会返回被删除消息的数量。

`XDEL` 的基本语法如下：

```sh
XDEL key ID [ID ...]
```

示例：

```sh
# 这个命令将从名为 `mystream` 的流中删除消息 ID 为 `1681480521617-0` 的消息。
XDEL my-stream 1681480521617-0
(integer) 1

# 你也可以传入多个 `id` 参数进行批量删除
XDEL my-stream 1681480524451-0 1681480526810-0 1681480965273-0
(integer) 3
```

注意：，`XDEL` 不会修改流的长度计数，这意味着删除消息后，流的长度保持不变。



### XLEN 获取流长度

XLEN 用于获取流中消息的数量。这个命令非常简单且高效，因为它只要一个参数。

`XLEN` 的基本语法如下：

```sh
XLEN key
```

示例：

```sh
XLEN my-stream
(integer) 4
```

注意：`XLEN` 命令仅返回流中消息的数量，并不提供消息的具体内容。获取消息内容的命令，看下面的 XRANGE



### XRANGE 查询消息

`XRANG`  主要用于获取流中的一段连续消息，它还有一个非常相似的 `XREVRANGE` 命令，区别：

* `XRANGE` 按照消息 ID 顺序返回结果
* `XREVRANGE` 按照消息 ID 逆序返回结果（用来查询流中最新的消息，非常有用！）

`XRANG` 的的基本语法如下：

```sh
XRANGE key start end [COUNT count]
```

#### 获取指定消息

获取指定消息，我们可以把 `start` 和 `end` 设置同一条消息 ID，可以用来达到查询指定消息 ID 的效果。使用示例：

```sh
# 获取指定消息 ID
XRANGE my-stream 1681480968241-0 1681480968241-0
```



#### 获取多条消息

获取多条消息，可以利用 COUNT 选项参数，使用示例：

```sh
# 获取流中最早的 5 条消息
XRANGE my-stream - + COUNT 5
```

这条命令获取流中最早的 5 条消息（按消息 ID 顺序排序）。`-` 和 `+` 分别表示最小和最大的消息 ID，用于获取流中的所有消息。



#### 获取全部消息

想要读取流中全部消息内容，移除 COUNT 即可：

```sh
# 获取全部消息
XRANGE my-stream - +
```



#### 逆序获取流

`XREVRANGE` 按照消息 ID 逆序返回结果，基本语法如下：

```sh
XREVRANGE key end start [COUNT count]
```

用法完全和 XRANGE 一样，这里就不过多介绍了，使用示例：

```sh
XREVRANGE my-stream + - COUNT 5
```

这个命令将返回名为 `mystream` 的流中的最新的 3 条消息（按消息 ID 逆序排序）。



#### XRANGE 的使用场景

在实际业务场景中，可以利用 `XRANGE` 和 `XREVRANGE` 命令可以用于实现以下功能：

* 分页查询：通过指定 `start`、`end` 和 `COUNT` 参数，可以实现对流中消息的分页查询
* 实时监控：可以使用这些命令来获取流中的最新消息，以便在实时监控或分析系统中展示
* 数据导出：如果需要将流中的数据导出到其他系统或文件中，可以使用这些命令来获取指定范围内的消息



### XREAD 阻塞读取流

相比 XRANGE，XREVRANGE 类似，XREAD 也是用于从流中读取消息的命令，但它们之间有一些关键区别：

* XREAD 支持同时读取多个流的消息
* XREAD 支持阻塞模式，可以在新消息到达时候，立即粗处理
* XREAD 支持 `BLOCK` 阻塞等待时间参数，控制阻塞时间

XREAD 的阻塞模式，可以更好的构建实时数据处理应用程序，如事件驱动系统、实时分析系统等。

`XREAD` 命令的基本语法如下：

```
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
```

#### 查询模式

查询的话，除了同时读取多个流的特点外，其他和 XRANGE，XREVRANGE 类似。

使用示例：

1. 读取单个流的消息：

```sh
XREAD STREAMS my-stream 0
```

这个命令将从名为 `my-stream` 的流中读取消息，0 代表读取所有消息，如果指定的消息 ID，表示从该消息 ID 之后开始读取

2. 读取多个流的消息：

```sh
XREAD STREAMS my-stream mini-stream 0 0
```

这个命令将从名为 `my-stream` 和 `mini-stream` 的流中分别读取所有消息，后面的 2 个参数 0 分别对应 2 个消息 ID `0` 开始的位置



####  阻塞模式

当使用阻塞模式时，`XREAD` 命令会在以下几种情况下表现出不同的行为：

1. 不会阻塞的情况：找到符合条件的元素会立即返回
2. 会解除阻塞的情况：超时，或者新消息到达
3. 一直阻塞的情况：一直阻塞，等待新消息的到达



使用示例：

1. 不会阻塞的情况

如果流中有满足条件的消息（即从指定的消息 ID 之后的新消息），那么 `XREAD` 命令会立即返回这些消息，不会发生阻塞。

```sh
XREAD BLOCK 1000000 COUNT 1 STREAMS my-stream 0
1) 1) "my-stream"
   2) 1) 1) "1681480968241-0"
         2) 1) "k5"
            2) "v5"
```

2. 会解除阻塞的情况

`XREAD` 命令解除阻塞也分 2 情况：超时，新消息到达

示例代码：

```sh
# 超时: 阻塞超时，没有新消息到达，解除阻塞
XREAD BLOCK 5000 STREAMS my-stream 1681482023346-0
(nil)
(5.09s)

# 新消息到达: 新消息到达，且满足读取条件 (新消息的 ID 大于指定的消息 ID) 解除阻塞
XREAD BLOCK 50000 STREAMS my-stream 1681482023346-0
1) 1) "my-stream"
   2) 1) 1) "1681485525804-0"
         2) 1) "newMessage"
            2) "v1"
(18.46s)
```



3. 一直阻塞的情况：

如果设置的阻塞等待时间为 0，那么 `XREAD` 命令会一直阻塞：

示例代码：

```sh
XREAD BLOCK 0 STREAMS my-stream $
```

这个命令将一直阻塞等待，直到新消息到达。`$` 符号表示只读取新消息。

当然如果客户端主动断开连接，阻塞的 `XREAD` 命令也会被取消



在实际应用中，`XREAD` 使用阻塞模式，可以在新消息到达时立即处理，实现实时消息处理。



### 消费组

在 Redis 流的消息模型中，是通过消费者组（Consumer Group）来组织和管理多个消费者以协同处理来自同一个流的消息的机制。消费者组的主要目的是在多个消费者之间分发消息，实现负载均衡、高可用性和容错能力。

工作原理：

1. Stream 将消息分发，所有订阅的消费者组 Consumer Group 都会收到消息（消费组组共享 stream 的消息）
2. 消费者组本身不处理消息，而是再将消息分发给消费者，由消费者进行真正的消费（消费者独占组内的消息）

如图所示：

```mermaid
graph LR
    Stream((Stream)) -- messages --> ConsumerGroup1(Consumer Group 1)
    Stream((Stream)) -- messages --> ConsumerGroup2(Consumer Group 2)
    ConsumerGroup1(Consumer Group 1) -- messages --> Consumer1A(Consumer 1A)
    ConsumerGroup1(Consumer Group 1) -- messages --> Consumer1B(Consumer 1B)
    ConsumerGroup2(Consumer Group 2) -- messages --> Consumer2A(Consumer 2A)
    ConsumerGroup2(Consumer Group 2) -- messages --> Consumer2B(Consumer 2B)

```

使用消费者组这种模型的设计，以为在 Redis Stream 中实现以下功能：

* **负载均衡**：消费者组可以将消息分发给多个消费者，实现负载均衡
* **高可用性**：在某个消费者发生故障的情况下，仍然可以确保消息被处理
* **容错能力**：消费者组支持重新处理失败的消息，这有助于确保消息被可靠地处理



接下来我们再详细说明消费组相关的命令使用



### XGOUP 管理消费组

#### CREATE 创建消费组

通过 `XGROUP` 命令可以为你的 Redis Stream 创建和管理消费组。

命令格式如下：

```sh
XGROUP CREATE stream group id
```

参数说明：

- `<stream>`：要关联的流的键。
- `<group>`：消费组的名称。
- `<id>`：开始读取消息的起始 ID。通常使用 `$` 表示仅消费新消息，或者使用 `0` 表示消费流中的所有消息。
- `[MKSTREAM]`（可选）：如果流不存在，自动创建一个新的流。

使用示例：

```sh
# 创建消费组，如果流不存在则自动创建
XGROUP CREATE mystream mygroup $ MKSTREAM
OK

# 查看流中的消费组
XINFO GROUPS mystream
1)  1) "name"
    2) "mygroup"
    3) "consumers"
    4) (integer) 0
    5) "pending"
    6) (integer) 0
    7) "last-delivered-id"
    8) "0-0"
    9) "entries-read"
   10) (nil)
   11) "lag"
   12) (integer) 0
```

以上命令是使用 `XGROUP CREATE` 命令创建一个名为 `mygroup` 的消费组，从最新的消息开始消费，使用 `MKSTREAM` 选项，如果流不存在则会自动创建流，返回 OK 既代表创建成功。最后使用 XINFO 查看结果。



#### SETID 修改组的最后消息 ID

在某些情况下，你可能想要消费组忽略某些消息，或者重新处理某些消息来重现 bug，那么可以使用  `XGROUP SETID` 命令设置消费组的起始消息 ID。

命令格式非常简单：

```sh
XGROUP SETID stream group id
```

使用示例：

```sh
# 设置 mygroup 组的最新消息为指定 ID
XGROUP SETID mystream mygroup 1681655893911-0
OK

# 查看消费组
XINFO GROUPS mystream
1)  1) "name"
    2) "mygroup"
    3) "consumers"
    4) (integer) 0
    5) "pending"
    6) (integer) 0
    7) "last-delivered-id"
    8) "1681655893911-0"		# 已被改变
    9) "entries-read"
   10) (nil)
   11) "lag"
   12) (integer) 4
   
# 设置 mygroup 组的最新消息为流的最新消息 ID
XGROUP SETID mystream mygroup $

# 查看消费组
127.0.0.1:6379> XINFO GROUPS mystream
1)  1) "name"
    2) "mygroup"
    3) "consumers"
    4) (integer) 0
    5) "pending"
    6) (integer) 0
    7) "last-delivered-id"
    8) "1681655916001-0"		# 已更新
    9) "entries-read"
   10) (nil)
   11) "lag"
   12) (integer) 0
```

以上命令将 `mygroup` 组的最新消息 ID 更新为指定 ID 和流的最新 ID 的使用示例。



#### XREADGROUP 读取消息

使用 `XREADGROUP ` 命令读取消费组里面的消息，基本语法：

```sh
XREADGROUP GROUP <group> <consumer> [COUNT <n>] [BLOCK <ms>] STREAMS <stream_key_1> <stream_key_2> ... <id_1> <id_2> ...
```

**参数说明**：

- `<group>`：消费组的名称。
- `<consumer>`：消费者的名称。
- `<n>`（可选）：要读取的最大消息数。
- `<ms>`（可选）：阻塞等待新消息的时间（以毫秒为单位）。
- `<stream_key_1>`, `<stream_key_2>`：要从中读取消息的流的键。
- `<id_1>`, `<id_2>`：从每个流中开始读取的消息 ID，通常使用特殊字符 `>` 表示从上次读取的位置开始读取新的消息。



使用示例：

我们创建一个 `myconsumer` 的消费组读取上面创建 `mygroup` 消费组的信息，以下是多种用法示例：

```sh
# 以 myconsumer 消费者身份从 mystream 中读取分配给 mygroup 的消息
# 读取所有最新的消息（常用）
XREADGROUP GROUP mygroup myconsumer STREAMS mystream >
(nil)

# 其他用法:
# 读取最多 10 条消息
XREADGROUP GROUP mygroup myconsumer COUNT 10 STREAMS mystream >

# 进行阻塞读取最新消息
XREADGROUP GROUP mygroup myconsumer BLOCK 5000 STREAMS mystream >
```

这里拿不到数据是因为我们上面把消费组 mygroup 的消息 ID 设置为最新，我们尝试修改消息 ID 重新消费试试

```sh
# 设置消费组的消息 ID，进行重新消费
XGROUP SETID mystream mygroup 1681655893911-0

# 消费组 myconsumer 读取消费组的消息
XREADGROUP GROUP mygroup myconsumer STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1681655897993-0"
         2) 1) "k1"
            2) "v1"
      2) 1) "1681655899297-0"
         2) 1) "k1"
            2) "v1"
      3) 1) "1681655915496-0"
         2) 1) "k1"
            2) "v1"
      4) 1) "1681655916001-0"
         2) 1) "k1"
            2) "v1"
            
# 查看消费组的信息
XINFO GROUPS mystream
1)  1) "name"
    2) "mygroup"
    3) "consumers"
    4) (integer) 1		# 消费组有一个消费者
    5) "pending"
    6) (integer) 4		# 有 4 条正在处理的消息
    7) "last-delivered-id"
    8) "1681655916001-0"
    9) "entries-read"
   10) (nil)
   11) "lag"
   12) (integer) 0
```

通过以上命令可以确认，`myconsumer`  消费者拿到 `mygroup` 消费组的消息未确认处理，所以看到有 4 条消息正在等待处理中。



#### XPENDING  查看消息

通过 XPENDING 命令，可以获取指定流的指定消费者组目前的待处理消息的相关信息。在很多场景下，你需要通过它来观察和了解消费者的处理情况，从而做出处理，例如以下场景：

* 您可以获取消费组中挂起（未确认）的消息信息，从而了解消费者处理消息的速度和效率
* 如果某个消费者的挂起消息数量不断增加，或者某些消息长时间未被处理，可能表明该消费者存在问题
* 在高并发或高负载的情况下，消费者可能无法及时处理所有消息。通过 `XPENDING` 命令检测到积压消息
* 通过定期运行 `XPENDING` 命令，您可以在发现挂起消息数量超过预设阈值时触发报警

基本语法：

```sh
XPENDING stream group [start stop count] [consumer]
```

**参数说明**：

- `<stream>`：流的键。
- `<group>`：消费组的名称。
- `<start>`（可选）：挂起消息范围的起始 ID。
- `<stop>`（可选）：挂起消息范围的结束 ID。
- `<count>`（可选）：返回的最大挂起消息数。
- `<consumer>`（可选）：筛选特定消费者的挂起消息。



使用示例：

使用 `XPENDING` 命令查看上面的 `mygroup` 组的消息去哪儿了：

```sh
XPENDING mystream mygroup
1) (integer) 4			# 待处理消息数量
2) "1681655897993-0"	# 首条消息 ID
3) "1681655916001-0"	# 最后一条消息的 ID
4) 1) 1) "myconsumer"	# 各消费者正在处理的消息数量
      2) "4"
```

以上展示的汇总信息，你还可以通过以下命令，查看待处理消息更详细的信息：

```sh
# 查看指定待处理消息
XPENDING mystream mygroup 1681655897993-0 1681655897993-0 1
1) 1) "1681655897993-0"		# 消息 ID
   2) "myconsumer"			# 所属消费者
   3) (integer) 2397387		# 最后一次投递时间
   4) (integer) 1			# 投递次数
```

从以上信息你可以看到消息正在被谁处理和处理的时间，你也可以指定消费者查看信息：

```sh
XPENDING mystream mygroup - + 10 myconsumer
1) 1) "1681655897993-0"
   2) "myconsumer"
   3) (integer) 2591145
   4) (integer) 1
2) 1) "1681655899297-0"
   2) "myconsumer"
   3) (integer) 2591145
   4) (integer) 1
3) 1) "1681655915496-0"
   2) "myconsumer"
   3) (integer) 2591145
   4) (integer) 1
4) 1) "1681655916001-0"
   2) "myconsumer"
   3) (integer) 2591145
   4) (integer) 1
```

以上命令列出 myconsumer 消费者所有待处理的消息的详细信息



#### XACK 处理消息

XACK 用于确认消费组中的特定消息已被处理。在消费者成功处理消息后，应使用 `XACK` 命令通知 Redis，以便从消费组的挂起消息列表中移除该消息。

命令格式：

```sh
XACK stream group id [id id ...]
```

使用示例：

通过 XACK 命令，我们将上面 myconsumer 消费者的消息进行确认处理：

```sh
# 确认消息
XACK mystream mygroup 1681655897993-0
(integer) 1
# .....
```

当消费者对所有消息进行处理后，再查看消费组内容进行验证：

```sh
XPENDING mystream mygroup - + 10 myconsumer
(empty array)

XPENDING mystream mygroup
1) (integer) 0
2) (nil)
3) (nil)
4) (nil)
```

使用 `XACK` 可以确保消息不会重复处理防止其他消费者或相同消费者在故障恢复后重复处理该消息等等好处。



#### XCLAIM 消息转移

`XCLAIM` 消息转移类似我们生活中的呼叫转移，当一个消费者无法处理某个消息或出现故障时，`XCLAIM` 可以确保其他消费者接管并处理这些消息。命令格式非常简单：

```sh
XCLAIM stream group new_consumer max_pending_time id [id id id]
```

使用示例：

```sh
# 使用 XPENDING 命令查询消费组中挂起的消息
XPENDING mystream mygroup
1) (integer) 2
2) "1681660259887-0"
3) "1681660263096-0"
4) 1) 1) "myconsumer"
      2) "2"
      
# 使用 XCLAIM 命令将消息转移
XCLAIM mystream mygroup myconsumer2 10000 1681660259887-0
1) 1) "1681660259887-0"			# 被转移的消息 ID
   2) 1) "k1"					# 消息内容
      2) "v1"
```

上面的命令意思是：如果消息 ID 1681660259887-0 处理时间超过 10000ms，那么消息转移给 myconsumer2，我们使用 XPENDING 命令来验证：

```sh
XPENDING mystream mygroup
1) (integer) 2
2) "1681660259887-0"
3) "1681660263096-0"
4) 1) 1) "myconsumer"
      2) "1"
   2) 1) "myconsumer2"
      2) "1"
```



#### XINFO 查看流和组信息

XINFO 用于获取流或消费组的详细信息。`XINFO` 命令有多个子命令，可以提供不同类型的信息。

以下是一些常用的 `XINFO` 子命令及其介绍：

**XINFO STREAM**：此子命令用于获取流的详细信息，包括长度、消费组数量、第一个和最后一个条目等。例如：

```sh
XINFO STREAM mystream
```

**XINFO GROUPS**：此子命令用于获取流中消费组的列表及其相关信息。例如：

```sh
XINFO GROUPS mystream
```

**XINFO CONSUMERS**：此子命令用于获取消费组中消费者的列表及其相关信息。例如：

```sh
XINFO CONSUMERS mystream mygroup
```

通过使用这些子命令，您可以了解流、消费组和消费者的状态，从而监控和优化 Redis Stream 应用程序的性能。在处理问题或分析系统性能时，这些信息可能特别有用。



#### 删除操作

##### 删除消费者

当用户不再需要某个消费者的时候，可以通过执行以下命令将其删除，命令格式：

```sh
XGROUP DELCONSUMER stream group consumer
```

使用示例：

```sh
# 删除 myconsumer 消费者
XGROUP DELCONSUMER mystream mygroup myconsumer
(integer) 1
```



##### 删除消费组

当你不需要消费组时，可以通过以下命令删除它，命令格式：

```sh
XGROUP DESTROY stream group
```

使用示例：

```sh
# 删除 mygroup 消费组
XGROUP DESTROY mystream mygroup
(integer) 1
```



### 总结

以下是本篇文章涉及的 Redis Stream 命令命令和简要总结：

1. **XADD**：向流中添加新的消息。
2. **XREAD**：从流中读取消息。
3. **XREADGROUP**：从消费组中读取消息。
4. **XRANGE**：根据消息 ID 范围读取流中的消息。
5. **XREVRANGE**：与 XRANGE 类似，但以相反顺序返回结果。
6. **XDEL**：从流中删除消息。
7. **XTRIM**：根据 MAXLEN 参数修剪流的长度。
8. **XLEN**：获取流的长度。
9. **XGROUP**：管理消费组，包括创建、删除和修改。
10. **XACK**：确认消费组中的消息已被处理。
11. **XPENDING**：查询消费组中挂起（未确认）的消息。
12. **XCLAIM**：将挂起的消息从一个消费者转移到另一个消费者。
13. **XINFO**：获取流、消费组或消费者的详细信息。

这些命令提供了对 Redis Stream 的全面操作支持，包括添加、删除、读取、修剪消息以及管理消费组和消费者。通过熟练使用这些命令，您可以实现高效且可扩展的消息传递和日志处理系统。edis Stream 是 Redis 提供的一种强大、持久且可扩展的数据结构，用于实现消息传递和日志处理等场景。Stream 数据结构类似于日志文件，消息以有序的方式存储在流中，同时还支持消费组的概念，允许多个消费者并行处理消息。