+++
date = '2023-04-02T14:33:49+08:00'
draft = false
title = 'Introduction to Java Lambda Functional Programming'
tags = ["Java"]
+++

### Overview

Functional programming is based on **Lambda Calculus**, a formal system for studying functions developed by Alonzo Church in the 1930s. Languages like Haskell and Erlang brought these concepts into practical use. Java 8 introduced these features to handle growing program complexity through a more concise and robust style.

> **OO is about abstracting data; FP is about abstracting behavior.**

### Traditional vs. Lambda Style

Before Java 8, we used anonymous inner classes for strategies or callbacks. This was verbose.

#### Old Way: Anonymous Inner Class
```java
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        System.out.println("Handled!");
    }
});
```

#### New Way: Lambda Expression
```java
button.addActionListener(e -> System.out.println("Handled!"));
```

### Lambda Syntax

A Lambda expression consists of:
1. **Parameters**: `(x, y)`
2. **Arrow**: `->`
3. **Body**: `{ ... }` or a single statement.

```java
// Multiple parameters
BinaryOperator<Integer> add = (x, y) -> x + y;

// No parameters
Runnable r = () -> System.out.println("Running");

// Multiple lines
Function<String, String> process = s -> {
    String result = s.trim().toUpperCase();
    return result + "!";
};
```

### Method References

Method references (`::`) are a shorthand for Lambdas that simply call an existing method.

1. **Static Methods**: `Integer::parseInt`
2. **Instance Methods of a Particular Object**: `System.out::println`
3. **Instance Methods of an Arbitrary Object of a Particular Type**: `String::toUpperCase`
4. **Constructors**: `Dog::new`

### Functional Interfaces

A functional interface is an interface with exactly one abstract method. The `@FunctionalInterface` annotation helps the compiler enforce this.

Core interfaces in `java.util.function`:
- `Predicate<T>`: Returns `boolean`.
- `Consumer<T>`: Returns `void`.
- `Function<T, R>`: Returns `R`.
- `Supplier<T>`: Returns `T`.
- `UnaryOperator<T>`: Returns `T` (same as input type).

### Higher-Order Functions

A function that takes one or more functions as arguments or returns a function as its result.

```java
public static Function<Integer, Integer> multiplier(int factor) {
    return x -> x * factor;
}
```

### Closures and Variable Capture

Lambdas can use variables from their outer scope, but these variables must be `final` or "effectively final" (not modified after assignment).

### Composition

Lambdas can be combined to form complex logic.
```java
Predicate<String> isValid = s -> s != null && !s.isEmpty();
Predicate<String> shortValid = isValid.and(s -> s.length() < 10);
```

### Summary

Lambda expressions and functional programming features shifted Java toward a more declarative style, reducing boilerplate and making concurrent programming easier to manage.
