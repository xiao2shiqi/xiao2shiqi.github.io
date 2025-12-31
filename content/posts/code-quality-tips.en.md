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

Writing unit tests is a good software development practice that can improve code quality, maintainability, and reliability, while also improving development efficiency and supporting continuous integration and continuous delivery.

#### Getting Started with Unit Testing

To get started with unit testing, we usually begin with **Static Testing**, as it is simple and easy to understand. Static testing refers to pre-defining all test methods and test data when writing test cases. These will not change at runtime. Common annotations in JUnit for static testing include `@Test`, `@Before`, `@After`, etc. Let's look at a simple example of static testing.

First, ensure your `pom.xml` file includes JUnit dependencies:

```xml
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-api</artifactId>
        <version>5.8.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.8.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

Then, create a simple calculator class—this would typically be your actual business class in practice:

```java
public class SimpleCalculator {

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }
}
```

Then create the corresponding test class in the same directory under `/test`:

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class SimpleCalculatorTest {

    // Executes once before all test methods. This method must be static.
    @BeforeAll
    static void setup() {
        System.out.println("BeforeAll - Initialize shared resources, such as a database connection");
    }

    // Executes once after all test methods. This method must be static.
    @AfterAll
    static void tearDown() {
        System.out.println("AfterAll - Clean up shared resources, such as closing a database connection");
    }

    // Executes before each test method. Used to set the initial state required for the test method.
    @BeforeEach
    void init() {
        System.out.println("BeforeEach - Initialize data required for the test instance");
    }

    // Executes after each test method. Used to clean up resources used by the test method.
    @AfterEach
    void cleanup() {
        System.out.println("AfterEach - Clean up resources used by the test instance");
    }

    // Annotates a test method to test a specific function.
    @Test
    void testAddition() {
        System.out.println("Test - Test addition function");
        SimpleCalculator calculator = new SimpleCalculator();
        assertEquals(5, calculator.add(2, 3), "2 + 3 should be 5");
    }

    // Add another test method
    @Test
    void testSubtraction() {
        System.out.println("Test - Test subtraction function");
        SimpleCalculator calculator = new SimpleCalculator();
        assertEquals(1, calculator.subtract(3, 2), "3 - 2 should be 1");
    }
}
```

In the program above, you can see common JUnit annotations:

* `@BeforeAll`: Executes once before all test methods. This method must be static.
* `@AfterAll`: Executes once after all test methods. This method must be static.
* `@BeforeEach`: Executes before each test method. Used to set the initial state required by the test method.
* `@AfterEach`: Executes after each test method. Used to clean up resources used by the test method.
* `@Test`: Annotates a test method for testing a specific function.

For a Maven project, you can run tests using the following command in the directory:

```sh
mvn test
```

Output:

```sh
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running SimpleCalculatorTest
BeforeAll - Initialize shared resources, such as a database connection
BeforeEach - Initialize data required for the test instance
Test - Test addition function
AfterEach - Clean up resources used by the test instance
BeforeEach - Initialize data required for the test instance
Test - Test subtraction function
AfterEach - Clean up resources used by the test instance
AfterAll - Clean up shared resources, such as closing a database connection
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.058 s - in SimpleCalculatorTest
[INFO] 
[INFO] Results:
[INFO]
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

Alternatively, you can run tests directly in IDEA:

![Unit test execution results](https://s2.loli.net/2025/02/13/d2jT8yszFNOQGvE.png)

This is a simple example of static testing.

#### Dynamic Testing

Dynamic testing refers to generating test methods and test data at runtime. In dynamic testing, test methods and data are not determined at compile time but are generated dynamically based on specific conditions or data sources at runtime. In static tests, sample data is limited, making it hard to cover all situations and reach high coverage. **JUnit 5** introduces dynamic testing, which is more complex, flexible, and suitable for complex scenarios. Let's see the difference through an example. We'll create a `MyStringUtil` class with a `reverse()` method:

```java
public class MyStringUtil {
    public String reverse(String input) {
        if (input == null) {
            return null;
        }
        return new StringBuilder(input).reverse().toString();
    }
}
```

In a static test class, we use `@Test` to define 3 methods covering various cases:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class MyStringUtilStaticTest {

    private MyStringUtil stringUtil = new MyStringUtil();

    @Test
    void reverseString() {
        // Reverse string 'hello'
        assertEquals("olleh", stringUtil.reverse("hello"));
    }

    @Test
    void reverseEmptyString() {
        // Reverse empty string
        assertEquals("", stringUtil.reverse(""));
    }

    @Test
    void handleNullString() {
        // Handle null string
        assertEquals(null, stringUtil.reverse(null));
    }
}
```

Then use dynamic testing to achieve the same result:

```java
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

import java.util.Arrays;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.DynamicTest.dynamicTest;

public class MyStringUtilDynamicTest {

    private MyStringUtil stringUtil = new MyStringUtil();

    // Uses @TestFactory to define a dynamic test factory method
    // Returns a Collection<DynamicTest>
    @TestFactory
    Collection<DynamicTest> reverseStringDynamicTests() {
        // Contains 3 dynamic test cases, created using the dynamicTest() method
        return Arrays.asList(
                dynamicTest("Dynamic Test: Reverse string 'hello'", () -> assertEquals("olleh", stringUtil.reverse("hello"))),
                dynamicTest("Dynamic Test: Reverse empty string", () -> assertEquals("", stringUtil.reverse(""))),
                dynamicTest("Dynamic Test: Handle null string", () -> assertEquals(null, stringUtil.reverse(null)))
        );
    }
}
```

The logic in the dynamic test class is as follows:
1. Define a dynamic test factory method `reverseStringDynamicTests()` using `@TestFactory`.
2. The method returns a `Collection<DynamicTest>` containing the cases.
3. Each case is created using `dynamicTest()`.

This covers the basics of unit testing. For detailed usage of JUnit 5, please refer to the official documentation.

#### Unit Testing + DbC

Unit testing should follow the **Design By Contract (DbC)** style as much as possible:

> Design By Contract (DbC) is a software development method emphasizing clear definitions of input and output agreements (contracts) for each module or function. These include pre-conditions, post-conditions, and potential exceptions. Implementations must satisfy these agreements, or an error/exception is triggered.

This might be abstract, so let's look at an example using assertions:

```java
public class BankAccount {
    private double balance;

    public BankAccount(double balance) {
        this.balance = balance;
    }
    
    public void withdraw(double amount) {
        assert amount > 0 : "Amount must be positive";
        assert amount <= balance : "Insufficient balance";
        
        balance -= amount;
        
        assert balance >= 0 : "Balance can't be negative";
    }
    
    public double getBalance() {
        return balance;
    }
}
```

In this example:
* `assert amount > 0 : "Amount must be positive";` means withdrawal amount `amount` must be greater than 0.
* `assert amount <= balance : "Insufficient balance";` means `amount` must be less than or equal to `balance`.
* `assert balance >= 0 : "Balance can't be negative";` means the remaining balance must be non-negative.

Assertions can be enabled with the `-ea` JVM parameter. However, since built-in assertions can be inconvenient, the Guava team added a `Verify` class that is always enabled. Use it similarly to assertions.

#### Test-Driven Development (TDD)

TDD is a software development method where tests are written before the code. The core idea is to think about expected results first. Developers then write minimal code to pass the test, then refactor for quality.

Process:

<img src="https://s2.loli.net/2025/02/13/qPmuehfXRAldc6N.png" alt="TDD" style="zoom: 50%;" />

As a long-term TDD practitioner, I summarize its benefits:

1. **Improve Maintainability**: We often fear maintaining code without tests. TDD's robust tests provide a safety net for refactoring.
2. **Faster Development**: Many developers delay testing until after feature implementation, but then more features pile up. It's better to write tests first.
3. **Higher Quality Delivery**: Code with tests is vastly different from code without them. Untested code is unfit for production.

### Logging

Adequate logging helps developers understand the program's operation and locate problems faster, improving stability and reliability. It also tracks performance and behavior for optimization.

#### Log Output

Example of printing a simple log:
1. Add SLF4J dependency (Maven):

```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>1.7.30</version>
</dependency>
```

2. Add an implementation like Logback or Log4j2:

```xml
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.3</version>
</dependency>
```

3. Code to log "Hello World":

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

SLF4J defines several levels to control output:

| Level | Content |
| --- | --- |
| TRACE | Fine-grained details for debugging. |
| DEBUG | Detailed info for debugging (variable values, method calls). |
| INFO | Operational status (startup, shutdown, DB connections). |
| WARN | Warning of potential issues that don't affect normal operation. |
| ERROR | Error information, including fatal errors. |

Different levels help minimize file size and provide quick localization. Dev environments usually use TRACE/DEBUG, while production uses INFO/WARN. These are configured in `logback.xml`.

#### Log Configuration

Basic `logback.xml` example (outputs to console and file):

```xml
<configuration>
  <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
      <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
  </appender>

  <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>/var/log/myapp.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>/var/log/myapp.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>7</maxHistory>
    </rollingPolicy>
    <encoder>
      <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
  </appender>

  <root level="INFO">
    <appender-ref ref="CONSOLE" />
    <appender-ref ref="FILE" />
  </root>
</configuration>
```

Two appenders are defined: CONSOLE and FILE (with daily rotation and 7-day retention). The root logger is set to INFO.

### Static Code Analysis

Static scan tools help find problems early, improving quality and security. They also enforce style consistency for better team collaboration and smoother CodeReviews.

| Tool Name | GitHub Address |
| --- | --- |
| FindBugs | https://github.com/findbugsproject/findbugs |
| PMD | https://github.com/pmd/pmd |
| Checkstyle | https://github.com/checkstyle/checkstyle |
| SonarQube | https://github.com/SonarSource/sonarqube |
| IntelliJ IDEA | https://github.com/JetBrains/intellij-community/ |

It's recommended to integrate these into CI/CD for automated checks.

### Code Review

Manual Code Review is the final step. Despite earlier tests and tools, manual checks are still necessary because static tools have limitations:
1. They only check for common syntax, security, and vulnerability patterns.
2. They identify issues but may not offer the best design solutions.
3. They only ensure compliance with specific standards, not overall logic quality or readability.

Manual Code Review advantages:
1. Discovery of complex logic issues, unreasonable designs, or unnecessary complexity.
2. Experts can provide better solutions based on experience.
3. Promotes team collaboration and learning through code sharing and discussion.

Combining static analysis and manual review ensures a more comprehensive audit.

### Summary

In modern software development, Unit Testing, TDD, Logging, Static Analysis, and manual Code Review are essential practices for ensuring software quality, maintainability, and team growth.

**Unit Testing** allows early bug detection and improves reliability and readability. **TDD** helps developers better understand requirements and avoid bugs. **Logging** tracks program status for debugging and optimization. **Static Analysis** provides automated checks for common errors. **Manual Code Review** offers deep insights and promotes team learning.

Following these practices and using appropriate tools will lead to more robust and high-quality software.
