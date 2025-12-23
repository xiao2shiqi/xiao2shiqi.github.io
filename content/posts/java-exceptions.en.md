+++
date = '2023-05-18T14:38:19+08:00'
draft = false
title = 'Reflections on Java Exception Handling'
tags = ["Java"]
+++

### 1. Classification of Java Exceptions

Java exceptions are basically divided into two categories: **Checked Exceptions** and **Unchecked Exceptions (Runtime Exceptions)**.

#### Checked Exceptions
These are exceptions that the compiler forces you to handle (either via `try-catch` or `throws`). They usually represent external factors that the program cannot control, such as a file not being found or a network interruption.

#### Unchecked Exceptions (Runtime Exceptions)
These occur during the execution of the program, such as `NullPointerException`, `ArrayIndexOutOfBoundsException`, or `IllegalArgumentException`. They usually indicate programming errors or logic flaws.

### 2. The Exception Hierarchy

All exception classes are subclasses of `java.lang.Throwable`.
- **Error**: Represents serious problems that a typical application should not try to catch (e.g., `OutOfMemoryError`).
- **Exception**: The root class for all exceptions that an application might want to catch.
    - **RuntimeException**: The root for all unchecked exceptions.
    - **Other subclasses**: These are checked exceptions.

### 3. Best Practices for Exception Handling

#### Avoid Empty Catch Blocks
Catching an exception and doing nothing is a dangerous practice. It hides bugs and makes debugging impossible. At the very least, log the exception.

#### Catch Specific Exceptions
Avoid catching the general `Exception` class. Catch specific exceptions (like `IOException`) to handle different error scenarios appropriately.

#### Use Finally for Resource Cleanup
Always use `finally` blocks or **try-with-resources** (introduced in Java 7) to ensure resources like database connections or file streams are closed, even if an exception occurs.

```java
try (BufferedReader br = new BufferedReader(new FileReader(path))) {
    return br.readLine();
} catch (IOException e) {
    log.error("Failed to read file", e);
}
```

#### Don't Use Exceptions for Flow Control
Exceptions are expensive in terms of performance (due to stack trace generation). Do not use them for normal program logic (e.g., using `try-catch` to check if a string is a number instead of using a validator).

#### Log and Rethrow
If you catch an exception but cannot handle it, log it and then rethrow it (either the same exception or a custom business exception). Ensure the original cause is preserved.

```java
try {
    // some code
} catch (SQLException e) {
    log.error("Database error occurred", e);
    throw new MyBusinessException("Internal server error", e); // Preserve cause
}
```

### 4. Custom Exceptions

Create custom exceptions to represent specific business errors. This improves code readability and allows for centralized error handling in web frameworks like Spring (using `@ControllerAdvice`).

```java
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}
```

### 5. Summary

Effective exception handling is a hallmark of robust code. By following these principles—using proper hierarchy, avoiding silent failures, and managing resources correctly—you can build systems that are much easier to maintain and troubleshoot.
