+++
date = '2023-04-25T14:44:13+08:00'
draft = false
title = 'Several Reference Suggestions for Improving Code Quality'
tags = ["Java","Code Quality","Technical Management"]
+++

### Unit Testing

#### What is Unit Testing?

Unit testing usually refers to testing a single function or method. The purpose of unit testing is to verify whether the behavior of each unit meets expectations and to quickly detect any potential problems when modifying the code. By writing test cases, we can verify whether these modules produce the correct output for specific inputs. The goal is to ensure that each module runs normally in various situations.

#### Benefits of Writing Unit Tests

Writing unit tests brings several benefits:

1. **Improve code quality**: Unit tests allow us to discover potential problems in the code early, such as boundary conditions and exceptions, thereby reducing the probability of errors.
2. **Improve code maintainability**: Unit tests help developers understand the functionality and implementation details of the code, making it easier to maintain and modify.
3. **Improve code reliability**: After modifying the code, unit tests help developers verify the correctness of the code, thereby improving its reliability.

#### Getting Started with Unit Testing

To get started with unit testing, we usually begin with **Static Testing**, as it is simple and easy to understand. Static testing refers to pre-defining all test methods and test data when writing test cases. These will not change at runtime. Common annotations in JUnit for static testing include `@Test`, `@Before`, `@After`, etc.

First, ensure your `pom.xml` includes JUnit dependencies:

```xml
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-api</artifactId>
        <version>5.8.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

Then, create a simple calculator class:

```java
public class SimpleCalculator {
    public int add(int a, int b) { return a + b; }
    public int subtract(int a, int b) { return a - b; }
}
```

Create the corresponding test class in the `/test` directory:

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class SimpleCalculatorTest {

    @BeforeAll
    static void setup() { System.out.println("BeforeAll - Initialize shared resources"); }

    @BeforeEach
    void init() { System.out.println("BeforeEach - Initialize data per test method"); }

    @Test
    void testAddition() {
        SimpleCalculator calculator = new SimpleCalculator();
        assertEquals(5, calculator.add(2, 3), "2 + 3 should be 5");
    }
}
```

Wait, the previous code had more details. Let me translate the rest.

#### Dynamic Testing

Dynamic testing refers to generating test methods and test data at runtime. In **JUnit 5**, dynamic tests are introduced, which are more flexible and suitable for complex scenarios. Let's look at the difference through an example.

Assume we have a `MyStringUtil` class with a `reverse()` method:

```java
public class MyStringUtil {
    public String reverse(String input) {
        if (input == null) return null;
        return new StringBuilder(input).reverse().toString();
    }
}
```

In a dynamic test class, we use `@TestFactory`:

```java
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import static org.junit.jupiter.api.DynamicTest.dynamicTest;
// ...
@TestFactory
Collection<DynamicTest> reverseStringDynamicTests() {
    return Arrays.asList(
        dynamicTest("Dynamic Test: reverse 'hello'", () -> assertEquals("olleh", stringUtil.reverse("hello"))),
        dynamicTest("Dynamic Test: reverse empty", () -> assertEquals("", stringUtil.reverse(""))),
        dynamicTest("Dynamic Test: handle null", () -> assertEquals(null, stringUtil.reverse(null)))
    );
}
```

#### Unit Testing + DbC

Unit testing should follow the **Design By Contract (DbC)** style as much as possible. DbC emphasizes defining clear pre-conditions and post-conditions for each module.

```java
public void withdraw(double amount) {
    assert amount > 0 : "Amount must be positive";
    assert amount <= balance : "Insufficient balance";
    balance -= amount;
    assert balance >= 0 : "Balance can't be negative";
}
```

#### Test-Driven Development (TDD)

TDD is a software development method where you write unit tests before writing the code itself. The core cycle is: Red (Fail) -> Green (Pass) -> Refactor.

Benefits of TDD:
1. **Improve maintainability**: Comprehensive tests provide a safety net for refactoring.
2. **Faster development**: Avoids the "write code now, test later" trap which often results in more bugs.
3. **Higher quality delivery**: Untested code is essentially unfit for production.

### Logging

Adequate logging helps developers understand the program's operation and locate problems faster.

#### Log Output

Example of printing a simple log using SLF4J:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HelloWorld {
    private static final Logger logger = LoggerFactory.getLogger(HelloWorld.class);
    public static void main(String[] args) {
        logger.info("Hello World");
    }
}
```

#### Log Levels

SLF4J defines several levels:
- **TRACE**: Fine-grained details for debugging.
- **DEBUG**: Information useful for debugging.
- **INFO**: Operational status information.
- **WARN**: Potential issues that don't affect normal operation.
- **ERROR**: Errors that have occurred.

#### Log Configuration

An example `logback.xml` configuration can output to both the console and a file, often with rolling policies (e.g., saving logs for 7 days).

### Static Code Analysis

Static scan tools help find bugs, security vulnerabilities, and style issues automatically.
- **FindBugs**
- **PMD**
- **Checkstyle**
- **SonarQube**

It's recommended to integrate these tools into your CI/CD pipeline.

### Code Review

Why is manual Code Review still necessary after all these tests and tools? Machine tools have limitations:
1. They only check for common syntax or vulnerability patterns.
2. They cannot provide better design solutions.
3. They cannot ensure overall readability and logic correctness.

Manual Code Review advantages:
1. Discovery of complex logic issues and design flaws.
2. Sharing knowledge and promoting team collaboration and growth.

### Summary

In modern development, Unit Testing, TDD, Logging, Static Analysis, and manual Code Review are all essential practices for high-quality software. They help ensure reliability, maintainability, and promote team growth.
