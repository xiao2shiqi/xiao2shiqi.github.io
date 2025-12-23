+++
date = '2023-05-24T14:15:08+08:00'
draft = false
title = 'Understanding and Applying Java Generics'
tags = ["Java"]
+++

### 1. Overview

Generics sanitize your code by providing:
- **Safety**: Compile-time type checking.
- **Reusability**: Using `<T>` for generic structures.
- **Cleanliness**: Reducing boilerplate casting.

Java generics are implemented via **Type Erasure**, meaning the type information exists only during compilation to ensure backward compatibility.

### 2. Basic Evolution

1. **Concrete Types**: `IntList` only handles integers.
2. **Object Container**: `ObjectList` handles everything but requires non-safe casting.
3. **Generics**: `GenericList<T>` handles everything with full type safety.

### 3. Tuples: Simple Data Objects

When you need to return multiple values of different types without a dedicated POJO:
```java
class Tuple<T1, T2> {
    private T1 first;
    private T2 second;
    // ...
}
```

### 4. Generic Interfaces and Methods

- **Interfaces**: `interface Container<T>` allows for flexible implementation.
- **Methods**: Prefer making methods generic rather than the whole class if possible.
  ```java
  public static <T> T getFirst(T[] array) { ... }
  ```

### 5. Type Erasure: The Bitter Compromise

At runtime, `List<String>` and `List<Integer>` are both just `ArrayList`. This was chosen to support code written before Java 5.

**Issues with Erasure:**
- You can't use `instanceof` with specific generic types.
- You can't create an array of T (`new T[10]`).
- You can't use primitives (`int`) as `<T>`.
- Information is lost if you try to use reflection on generic fields in a running program.

### 6. Generic Bounds (PECS)

- **Upper Bound (`? extends T`)**: Can read as T, but cannot write. (Producer Extends)
- **Lower Bound (`? super T`)**: Can write T or subclasses, but only read as Object. (Consumer Super)
- **Unbounded (`?`)**: Can accept any list, but acts as read-only. Better than `List<Object>` because it promotes type-agnostic code.

**PECS Rule**: "Producer Extends, Consumer Super." Use `extends` to read from a generic collection, and `super` to write to one.

### 7. Summary

Generics drastically improved Java's type safety and expressive power. Despite the limitations of Type Erasure, they remain a foundational tool for any modern Java developer.
