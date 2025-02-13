+++
date = '2023-04-25T14:44:13+08:00'
draft = false
title = '提高代码质量的几条参考建议'
+++

### 单元测试

#### 什么是单元测试 ？

单元测试通常是指对一个函数或方法测试。单元测试的目的是验证每个单元的行为是否符合预期，并且在修改代码时能够快速检测到任何潜在的问题。通过编写测试用例，我们可以验证这些模块在特定输入下是否产生正确的输出。单元测试的目的是确保每个模块在各种情况下都能正常运行。



#### 写单元测试的好处

可以带来以下几个好处：

1. 提高代码质量：单元测试可以我们提前的发现代码中的潜在问题，例如边界条件、异常情况等，从而减少出错的概率。
2. 提高代码可维护性：单元测试可以帮助开发人员理解代码的功能和实现细节，从而更容易维护和修改代码。
3. 提高代码可靠性：修改代码后，可以通过单元测试可以帮助开发人员验证代码的正确性，从而提高代码的可靠性。

写单元测试是一种良好的软件开发实践，可以提高代码质量、可维护性和可靠性，同时也可以提高开发效率和支持持续集成和持续交付。



#### 单元测试入门

上手单元测试，通常同时从静态测试（Static Test）开始，因为它简单，好理解，静态测试（Static Test）是指在编写测试用例时，我们提前定义好所有的测试方法和测试数据。这些测试方法和数据在编译时就已经确定，不会在运行时发生变化。Junit 中的静态测试通常的常规注解，如 @Test、@Before、@After 等。先来看看一组简单的静态测试示例。

首先，确保你的 `pom.xml` 文件包含 JUnit 的依赖：

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

然后，创建一个简单的计算器类，通常这里替换为你实际要测试的业务类：

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

然后在 `/test` 的相同目录下创建对应的测试类

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class SimpleCalculatorTest {

    // 在所有测试方法执行前，仅执行一次。这个方法需要是静态的。
    @BeforeAll
    static void setup() {
        System.out.println("BeforeAll - 初始化共享资源，例如数据库连接");
    }

    // 在所有测试方法执行后，仅执行一次。这个方法需要是静态的。
    @AfterAll
    static void tearDown() {
        System.out.println("AfterAll - 清理共享资源，例如关闭数据库连接");
    }

    // 在每个测试方法执行前，都会执行一次。用于设置测试方法所需的初始状态。
    @BeforeEach
    void init() {
        System.out.println("BeforeEach - 初始化测试实例所需的数据");
    }

    // 在每个测试方法执行后，都会执行一次。用于清理测试方法使用的资源。
    @AfterEach
    void cleanup() {
        System.out.println("AfterEach - 清理测试实例所用到的资源");
    }

    // 标注一个测试方法，用于测试某个功能。
    @Test
    void testAddition() {
        System.out.println("Test - 测试加法功能");
        SimpleCalculator calculator = new SimpleCalculator();
        assertEquals(5, calculator.add(2, 3), "2 + 3 应该等于 5");
    }

    // 再添加一个测试方法
    @Test
    void testSubtraction() {
        System.out.println("Test - 测试减法功能");
        SimpleCalculator calculator = new SimpleCalculator();
        assertEquals(1, calculator.subtract(3, 2), "3 - 2 应该等于 1");
    }
}
```

以上程序，可以看到 Junit 常用注解使用说明：

* @BeforeAll：在所有测试方法执行前，仅执行一次。这个方法需要是静态的
* @AfterAll：在所有测试方法执行后，仅执行一次。这个方法需要是静态的
* @BeforeEach：在每个测试方法执行前，都会执行一次。用于设置测试方法所需的初始状态
* @AfterEach：在每个测试方法执行后，都会执行一次。用于清理测试方法使用的资源
* @Test：标注一个测试方法，用于测试某个功能



如果是 maven 项目，可以在目录下执行命令执行测试：

```sh
mvn test
```

输出结果：

```sh
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running SimpleCalculatorTest
BeforeAll - 初始化共享资源，例如数据库连接
BeforeEach - 初始化测试实例所需的数据
Test - 测试加法功能
AfterEach - 清理测试实例所用到的资源
BeforeEach - 初始化测试实例所需的数据
Test - 测试减法功能
AfterEach - 清理测试实例所用到的资源
AfterAll - 清理共享资源，例如关闭数据库连接
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

或者可以直接在 IDEA 中执行测试，如下：

![单元测试运行结果](https://s2.loli.net/2025/02/13/d2jT8yszFNOQGvE.png)

以上就是静态测试的简单示例



#### 动态测试

动态测试（Dynamic Test）：动态测试是指在编写测试用例时，我们可以在运行时生成测试方法和测试数据。这些测试方法和数据在编译时不确定，而是在运行时根据特定条件或数据源动态生成。因为在静态单元测试中，由于测试样本数据有限，通常很难覆盖所有情况，覆盖率到了临界值就很难提高。**JUnit 5** 中引入动态测试，相比静态测试更复杂，当然也更灵活，也更适合复杂的场景。接下来通过一个简单的示例来展示**动态测试和静态测试的区别**，我们创建 `MyStringUtil` 类，它有一个方法 `reverse()` 用于反转字符串，如下：

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

在静态测试类中，我们使用 `@Test` 定义 3 个方法来尝试覆盖 `reverse()` 可能得多种情况：

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class MyStringUtilStaticTest {

    private MyStringUtil stringUtil = new MyStringUtil();

    @Test
    void reverseString() {
        // 反转字符串 'hello'
        assertEquals("olleh", stringUtil.reverse("hello"));
    }

    @Test
    void reverseEmptyString() {
        // 反转空字符串
        assertEquals("", stringUtil.reverse(""));
    }

    @Test
    void handleNullString() {
        // 处理 null 字符串
        assertEquals(null, stringUtil.reverse(null));
    }
}
```

然后用动态测试来实现同样的测试用例：

```java
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

import java.util.Arrays;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.DynamicTest.dynamicTest;

public class MyStringUtilDynamicTest {

    private MyStringUtil stringUtil = new MyStringUtil();

    // 使用 @TestFactory 注解定义了一个动态测试工厂方法 reverseStringDynamicTests()
    // 工厂方法返回一个 Collection<DynamicTest>
    @TestFactory
    Collection<DynamicTest> reverseStringDynamicTests() {
        // 包含了 3 个动态测试用例，每个测试用例使用 dynamicTest() 方法创建
        return Arrays.asList(
                dynamicTest("动态测试：反转字符串 'hello'", () -> assertEquals("olleh", stringUtil.reverse("hello"))),
                dynamicTest("动态测试：反转空字符串", () -> assertEquals("", stringUtil.reverse(""))),
                dynamicTest("动态测试：处理 null 字符串", () -> assertEquals(null, stringUtil.reverse(null)))
        );
    }
}
```

在动态测试类中逻辑如下：

1. 使用 `@TestFactory` 注解定义了一个动态测试工厂方法 `reverseStringDynamicTests()`。
2. 工厂方法返回一个 `Collection<DynamicTest>`，其中包含了 3 个动态测试用例。
3. 每个测试用例使用 `dynamicTest()` 方法创建。

以上就是基本的单元测试使用方法，关于 Junit 5 的具体使用并不打算在这里详解，有兴趣可以去参考 Junit 5 的官方文档



#### 单元测试 + Dbc

编写单元测试需要尽可能的遵循 **契约式设计 (Design By Contract, DbC)** 代码风格，关于契约式设计可以参考以下的描述：

> 契约式设计 (Design By Contract, DbC) 是一种软件开发方法，它强调在软件开发中对于每个模块或者函数，应该明确定义其输入和输出的约定（契约）。这些契约可以包括前置条件（preconditions）和后置条件（postconditions），以及可能发生的异常情况。在代码实现时，必须满足这些约定，否则就会引发错误或者异常。

这样说可能比较抽象，可以通过以下的示例代码来理解，如何使用断言来实现契约式设计：

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

在这个示例中，我们使用了 Java 中的断言（assertion）来实现契约式设计。具体来说：

* `assert amount > 0 : "Amount must be positive";` 表示取款金额 `amount` 必须大于 0
* `assert amount <= balance : "Insufficient balance";` 表示取款金额 `amount` 必须小于等于账户余额 `balance`
* `assert balance >= 0 : "Balance can't be negative";` 表示取款完成后，账户余额 `balance` 的值应该为非负数

可以通过使用 JVM 的 `-ea` 参数来开启断言功能，不过因为启用 Java 本地断言很麻烦，Guava 团队添加一个始终启用的用来替换断言的 Verify 类。他们建议静态导入 Verify 方法。用法和断言差不多，这里就不过多赘述了。



#### 测试驱动开发 TDD

测试驱动开发（TDD）是一种软件开发方法，也是我个人非常推崇的一种软件开发方法，就是在编写代码之前编写单元测试。TDD 的核心思想是在编写代码之前，先编写测试用例。开发人员在编写代码前先思考预期结果，以便能够编写测试用例。接着开发人员编写足够简单的代码来通过测试用例，再对代码进行重构以提高质量和可维护性。

如图：

<img src="https://s2.loli.net/2025/02/13/qPmuehfXRAldc6N.png" alt="TDD" style="zoom: 50%;" />

作为 TDD 的长期实践者，我总结 TDD 能带来的好处如下：

1. 提高可维护性：通常我们不敢去维护一段代码的原因是没有测试，TDD 建立的完善测试，可以为重构代码提供保障
2. 更快速的开发：很多开发总想着实现功能后再去补测试，但通常功能实现后，还会有更多的功能，所以尽量在功能开始前先写测试
3. 更高质量的交付：这里就不必多说了，通过测试的代码和没有测试的代码，是完全不一样的。未经测试的代码根本不具备上生产的条件



### 日志

充足的日志可以帮助开发人员更好地了解程序的运行情况。通过查看日志，可以了解程序中发生了什么事情，以及在哪里发生了问题。这可以帮助开发人员更快地找到和解决问题，从而提高程序的稳定性和可靠性。此外，日志还可以用于跟踪程序的性能和行为，以便进行优化和改进。



#### 日志输出

通过以下是打印简单日志的示例：

1. 首先，你需要在项目中添加SLF4J的依赖。你可以在Maven或Gradle中添加以下依赖：

```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>1.7.30</version>
</dependency>
```

2. 接下来，你需要选择一个SLF4J的实现，例如Logback或Log4j2，并将其添加到项目中。你可以在Maven或Gradle中添加以下依赖：

```xml
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.3</version>
</dependency>
```

3. 在代码中，你可以使用以下代码打印Hello World：

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

这将使用SLF4J打印一条信息，其中包含“Hello World”字符串。你可以在控制台或日志文件中查看此信息。



#### 日志等级

主要是为了帮助开发人员更好地控制和管理日志输出。SLF4J 定义了多个日志级别：

| 日志级别 | 内容                                                         |
| -------- | ------------------------------------------------------------ |
| TRACE    | 用于跟踪程序的细节信息，通常用于调试。                       |
| DEBUG    | 用于调试程序，输出程序中的详细信息，例如变量的值、方法的调用等。 |
| INFO     | 用于输出程序的运行状态信息，例如程序启动、关闭、连接数据库等。 |
| WARN     | 用于输出警告信息，表示程序可能存在潜在的问题，但不会影响程序的正常运行。 |
| ERROR    | 用于输出错误信息，表示程序发生了错误，包括致命错误。         |

不同的日志级别用于记录不同的信息。这样做的目的不仅可以减少不必要的日志输出和文件大小，还可以提供快速定位的能力，例如开发环境通常使用 TRACE、DEBUG 日志，生产环境通常使用 INFO，WARN 日志等。这些信息都可以在 `logback.xml` 日志配置文件里面配置。



#### 日志配置

以下是一个基本的 logback 配置文件示例，该配置文件将日志输出到控制台和文件中：

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

在此配置文件中，定义了两个 appender：

1. 一个用于将日志输出到控制台（CONSOLE）
2. 一个用于将日志输出到文件（FILE）

控制台的日志格式使用了 pattern 格式化方式，而文件的日志使用了 RollingFileAppender 实现每日轮换，并定义了最多保存 7 天的日志历史。同时，定义了一个根（root）级别为 INFO 的 logger，它会将日志输出到 CONSOLE 和 FILE 两个 appender 中，其他日志级别（TRACE、DEBUG、WARN、ERROR）则按照默认配置输出到根 logger 中。



### 代码静态检查

在 Java 静态扫描工具可以帮助开发人员在开发过程中及时发现和修复代码中的问题和错误，从而提高代码质量和安全性。这些静态扫描工具还可以约束代码风格，在团队协助开发中，统一的风格，可以增强团队协作和沟通，可以增加代码的可读性，可维护性，还减少不必要的讨论和争议，有利于后续的 CodeReview 进展。下面是一些常用的 Java 静态扫描工具：

| 工具名称      | Github 地址                                      |
| ------------- | ------------------------------------------------ |
| FindBugs      | https://github.com/findbugsproject/findbugs      |
| PMD           | https://github.com/pmd/pmd                       |
| Checkstyle    | https://github.com/checkstyle/checkstyle         |
| SonarQube     | https://github.com/SonarSource/sonarqube         |
| IntelliJ IDEA | https://github.com/JetBrains/intellij-community/ |

访问它们的 Github 地址也提供了更多的信息和支持，可以帮助开发人员更好地理解和使用这些工具。另外，建议在开发过程中，将这些工具集成到持续集成和持续交付的流程中，以便自动化地进行代码检查和修复。



### Code Review

人工的 CodeReview 通常是开发流程的最后一步，为什么前面做了那么多测试和检查工具，到最后还需要人工检查呢 ？

因为静态扫描工具通常只能检查一些简单的问题和错误，相比人工检查它存在以下局限性：

1. 只能检查例如语法错误、安全漏洞常见的错误等。
2. 只能检查问题和错误，但无法给出更好的建议和解决方案。（它提供的通用解决方案未必是最好的）
3. 静态扫描工具只能检查代码是否符合特定的规范和标准，但无法确保代码的质量和可读性。



相比机器扫描，人工 Code Review 可以提供以下不可替代的优势：

1. 可以发现更复杂的问题，例如：业务逻辑的问题、不合理的设计、不必要的复杂性等
2. 相比机器的建议，人工 Code Review 可以根据经验和知识，提供更好的解决方案和建议
3. 可以促进团队协作和学习，通过分享和讨论代码，可以提高开发人员的技能和知识，并提高团队的凝聚力和效率。

综上所述，虽然静态扫描工具可以帮助开发人员自动化地发现代码中的问题和错误，但 Code Review 仍然是一种必要的软件开发实践，可以提高代码的质量、可读性和可维护性，同时也可以促进团队协作和学习。因此，建议在开发过程中，将人工 Code Review 和静态扫描工具结合起来，以便更全面和深入地审核和审查代码。



### 总结

在现代软件开发中，单元测试、TDD、日志、静态检查扫描和人工 Code Review 都是必要的实践，可以帮助开发人员确保软件质量、提高代码可读性和可维护性，并促进团队协作和学习。

首先，单元测试是一种测试方法，用于测试代码的基本单元，例如函数、方法等。单元测试可以帮助开发人员及早发现和解决代码中的问题和错误，从而提高代码质量和可靠性。同时，单元测试还可以提高代码的可读性和可维护性，使代码更易于理解和修改。

其次，TDD（Test-Driven Development，测试驱动开发）是一种开发方法，要求在编写代码之前先编写测试用例。通过使用 TDD，开发人员可以更好地理解代码需求和规范，避免代码中的错误和问题，并提高代码的可读性和可维护性。

第三，日志是一种记录程序运行时状态和信息的方法。日志可以帮助开发人员调试程序，发现潜在的错误和问题，并提供更好的错误处理和处理方案。同时，日志还可以记录程序运行时的性能和状态，从而帮助开发人员分析和优化程序性能。

第四，静态检查扫描工具是一种自动化的代码审核和审查工具，可以帮助开发人员及早发现和解决代码中的问题和错误。通过使用静态检查扫描工具，开发人员可以更全面地检查代码中的问题和错误，并提高代码质量和可读性。

最后，人工 Code Review 是一种手动审核和审查代码的方法，可以更深入地检查代码中的问题和错误，并提供更好的解决方案和建议。人工 Code Review 可以促进团队协作和学习，提高代码质量和可读性，同时还可以遵循特定的编码规范和标准。

综上所述，单元测试、TDD、日志、静态检查扫描和人工 Code Review 都是必要的软件开发实践，可以提高代码质量、可读性和可维护性，并促进团队协作和学习。在进行软件开发时，应该尽可能地遵循这些实践，并使用相应的工具和技术进行代码审核和测试。