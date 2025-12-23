+++
date = '2023-04-17T14:24:51+08:00'
draft = false
title = 'Redis Stream: A Better Message Queue'
tags = ["Redis", "Database"]
+++

> **Requires Redis 5.0.0+**

### Overview

Redis Stream is a powerful log-like data structure. While Redis already had Lists and Sets, Stream was built specifically for high-throughput, persistent messaging with features like **Consumer Groups** and **Acknowledged delivery**.

### Core Commands

#### XADD: Appending Data
```sh
XADD my-stream * name "John" age 30
```
- `*` tells Redis to auto-generate the ID.
- Returns an ID like `1681138020163-0` (Timestamp-Sequence).

#### XLEN: Getting Length
Returns the number of messages in the stream.

#### XRANGE: Querying
Fetch a range of messages by ID.
- `XRANGE my-stream - +` (All messages from beginning to end).
- `XREVRANGE my-stream + - COUNT 1` (Get the very last message).

#### XREAD: Blocking Read
Similar to `BLPOP` for lists but for streams.
```sh
XREAD BLOCK 5000 STREAMS my-stream $
```
- `BLOCK 5000`: Wait for up to 5 seconds.
- `$`: Only listen for *new* messages sent after the command was issued.

### Stream Maintenance (MAXLEN)

To prevent memory leaks, limit the stream size.
- `XADD my-stream MAXLEN 1000 * ...`
- `XTRIM my-stream MAXLEN 1000`

### Consumer Groups (Scaling Out)

Consumer Groups allow multiple workers to share the workload of one stream.

1. **Create Group**:
   ```sh
   XGROUP CREATE my-stream my-group $ MKSTREAM
   ```
2. **Read from Group**:
   ```sh
   XREADGROUP GROUP my-group consumer-1 STREAMS my-stream >
   ```
   The `>` symbol retrieves messages that have never been delivered to any other consumer in the group.

3. **ACK (Acknowledgment)**:
   After processing, you must acknowledge.
   ```sh
   XACK my-stream my-group 1681480968241-0
   ```

### Reliability: PEL and XCLAIM

When a message is delivered to a consumer, it enters the **Pending Entries List (PEL)**. If the consumer crashes before calling `XACK`, the message stays in the PEL.

- **XPENDING**: Inspect the PEL to see stuck messages.
- **XCLAIM**: Another consumer can "claim" an old stuck message to process it, ensuring no data is lost.

### Summary

Redis Stream turns Redis into a full-blown message broker with features rivaling specialized tools like Kafka or RabbitMQ, but with the simplicity and performance Redis is known for.
