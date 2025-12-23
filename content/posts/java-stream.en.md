+++
date = '2023-04-06T14:32:03+08:00'
draft = false
title = 'Introduction to Java Stream Programming'
tags = ["Java"]
+++

### What is a Stream?

A Stream is a sequence of elements supporting sequential and parallel aggregate operations. It focuses on the "what" (declarative) rather than the "how" (imperative). 

**Key Characteristics:**
- **No Storage**: Streams don't store data; they move it from a source (collection, array, I/O) through a pipeline.
- **Functional**: Operations don't modify the source; they return new streams.
- **Lazy Evaluation**: Intermediate operations are only performed when a terminal operation is called.
- **Possibly Infinite**: Unlike collections, streams can be unbounded (e.g., a stream of random numbers).

### Stream Pipeline Stages

1. **Creation**: `list.stream()`, `Stream.of(a, b)`, `IntStream.range(1, 10)`.
2. **Intermediate Operations**: (Lazy) `filter`, `map`, `sorted`, `distinct`.
3. **Terminal Operations**: (Triggers execution) `collect`, `forEach`, `reduce`, `count`, `anyMatch`.

### Common Operations

#### Creation
- `Stream.generate(Math::random).limit(10)`
- `Stream.iterate(0, n -> n + 2).limit(5)` (Generates 0, 2, 4, 6, 8)

#### Intermediate
- **filter(Predicate)**: Selects elements.
- **map(Function)**: Transforms elements.
- **flatMap(Function)**: Flattens a stream of streams into a single stream.
- **peek(Consumer)**: Performs an action for each element (mainly for debugging).

#### Terminal
- **collect(Collectors.toList())**: Accumulates elements into a collection.
- **reduce(BinaryOperator)**: Combines elements into a single result (e.g., sum).
- **allMatch/anyMatch/noneMatch**: Returns a boolean based on a condition.

### The Optional Class

Many terminal operations return an `Optional<T>` to avoid `NullPointerException` if the stream is empty.
```java
Optional<String> first = list.stream().findFirst();
first.ifPresent(System.out::println);
String result = first.orElse("Default");
```

### Parallel Streams

You can switch to parallel processing simply by calling `.parallelStream()`. However, this should be used with caution as it adds overhead and is only beneficial for large datasets or computationally expensive tasks.

### Summary

The Stream API revolutionized data processing in Java. It allows developers to write code that is more expressive, easier to read, and less prone to errors compared to traditional `for` loops.
