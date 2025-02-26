+++
date = '2023-04-09T14:28:31+08:00'
draft = false
title = 'Java 异常处理的使用和思考'
tags = ["Java"]
+++

###  概念

异常处理的概念起源于早期的编程语言，如 LISP、PL/I 和 CLU。这些编程语言首次引入了异常处理机制，以便在程序执行过程中检测和处理错误情况。异常处理机制随后在 Ada、Modula-3、C++、Python、Java 等编程语言中得到了广泛采用和发展。在 Java 中，异常处理是提供一种在程序运行时处理错误和异常情况的方法。异常处理机制使得程序能够在遇到错误时继续执行，而不是立即崩溃。这种机制使程序更具有健壮性和容错性。异常分为两类：受检异常（Checked Exceptions）和非受检异常（Unchecked Exceptions）



**受检异常（Checked Exceptions）：**

受检异常是指那些在编译时必须处理的异常。它们通常是由程序员的错误或外部资源问题引起的。例如，`IOException`、`FileNotFoundException` 等。受检异常必须在方法签名中使用 `throws` 关键字声明，或者在方法体内用 `try-catch` 块捕获和处理。



**非受检异常（Unchecked Exceptions）：**

非受检异常是指那些在编译时不强制要求处理的异常。它们通常是由编程错误引起的，如空指针异常（`NullPointerException`）、数组越界（`ArrayIndexOutOfBoundsException`）等。非受检异常继承自 `java.lang.RuntimeException` 类，不需要在方法签名中声明，也不需要强制捕获和处理。

它们的关系如下：

![image-20250215142923833](https://s2.loli.net/2025/02/15/d68wjyv4cUHAIGs.png)



### 异常处理

Java 使用 `try/catch` 关键字进行异常捕获，使用 `throw` 声明抛出异常，示例代码如下：

```java
public class NullPointerExceptionExample {
    public static void main(String[] args) {
        String nullString = null;
        try {
            int length = nullString.length();
        } catch (NullPointerException e) {
            System.out.println("Caught NullPointerException!");
            e.printStackTrace();
        }
    }
}
```

在这个示例中，我们尝试获取一个 `null` 字符串的长度。当调用 `nullString.length()` 时，会抛出 `NullPointerException`。我们使用 `try-catch` 语句捕获异常并处理它



### 自定义异常

Java 官方异常不可能预见所有可能发生的错误，有时候你需要结合自己的业务场景，例如以下场景：

1. 当内置的 Java 异常类无法准确描述你所遇到的异常情况时。
2. 需要为特定领域或业务逻辑创建一组特定的异常。
3. 当希望通过自定义异常类向调用者提供更多的上下文信息或特定的错误代码时。



构建特定的异常，这也很简单，继承已有的异常类（最好继承含义差不多的），如下，我们创建一个表示账户余额不足的异常：

```java
public class InsufficientBalanceException extends RuntimeException {
    private double balance;
    private double amount;

    public InsufficientBalanceException(double balance, double amount) {
        super("Insufficient balance: " + balance + ", required amount: " + amount);
        this.balance = balance;
        this.amount = amount;
    }

    public double getBalance() {
        return balance;
    }

    public double getAmount() {
        return amount;
    }
}
```

接下来，我们在业务逻辑代码中使用这个自定义异常：

```java
public class BankAccount {
    private double balance;

    public BankAccount(double balance) {
        this.balance = balance;
    }

    public void withdraw(double amount) throws InsufficientBalanceException {
        if (amount > balance) {
            throw new InsufficientBalanceException(balance, amount);
        }
        balance -= amount;
    }
}
```

调用者可以捕获并处理这个自定义异常：

```java
public class BankAccountTest {
    private static final Logger logger = Logger.getLogger(BankAccountTest.class.getName());

    public static void main(String[] args) {
        BankAccount account = new BankAccount(1000.00);
        try {
            account.withdraw(2000.00);
        } catch (InsufficientBalanceException e) {
            System.out.println("Error: " + e.getMessage());
            System.out.println("Current balance: " + e.getBalance());
            System.out.println("Required amount: " + e.getAmount());
            
            logger.log(Level.SEVERE, "An exception occurred", e);
        }
    }
}
```

可以看到自定义异常使我们能够更清晰地表达业务逻辑中可能出现的异常情况，同时为调用者提供更多关于异常的上下文信息。我们还使用 `java.util.logging` 工具将输出记录到日志中



### 多重捕获

在 Java 早起版本，处理多个没有共同基类的异常，需要为每一个异常类型编写一个 catch 语句处理，如下：

```java
class CustomException1 extends Exception {
    public CustomException1(String message) {
        super(message);
    }
}

class CustomException2 extends Exception {
    public CustomException2(String message) {
        super(message);
    }
}

public class SingleCatchException {

    public static void main(String[] args) {
        try {
            // 根据参数选择抛出哪种异常
            if (args.length > 0 && "type1".equals(args[0])) {
                throw new CustomException1("This is a custom exception type 1.");
            } else {
                throw new CustomException2("This is a custom exception type 2.");
            }
        } catch (CustomException1 e) {
            // 当 CustomException1 发生时，执行此代码块
            System.err.println("Error occurred: " + e.getMessage());
        } catch (CustomException2 e) {
            // 当 CustomException2 发生时，执行此代码块
            System.err.println("Error occurred: " + e.getMessage());
        }
    }
}
```

这样的代码不仅难以阅读，而且也不够简洁。

多重异常捕获机制，它允许在一个 `catch` 语句中捕获多个异常类型。这种方法可以避免重复的代码，使异常处理更加简洁。以下是一个使用多重异常捕获机制的示例：

```java
public class MultiCatchExample {

    public static void main(String[] args) {
        try {
            // 根据参数选择抛出哪种异常
            if (args.length > 0 && "type1".equals(args[0])) {
                throw new CustomException1("This is a custom exception type 1.");
            } else {
                throw new CustomException2("This is a custom exception type 2.");
            }
        } catch (CustomException1 | CustomException2 e) {
            // 当 CustomExceptionType1 或 CustomExceptionType2 发生时，执行此代码块
            System.err.println("Error occurred: " + e.getMessage());
        }
    }
}
```



### 重新抛出异常

在某些情况下，你可能希望将异常传递给调用者处理，而不是在当前方法中处理。或者需要在捕获异常时执行一些处理操作，如记录日志、清理资源或者添加额外的上下文信息。在这种情况下，你可以在 `catch` 块中处理异常，然后重新抛出原始异常或抛出一个新的异常，包含额外的信息，如下：

```java
public class RethrowExceptionExample {
    public static void main(String[] args) {
        try {
            doSomething();		// 可能会抛出异常的方法
        } catch (IOException e) {
            // 异常处理逻辑
            System.err.println("An error occurred: " + e.getMessage());            
            // 重新抛出异常
            throw e;
        }
    }
}
```



### 更好的 NPE

NPE（NullPointerExceptions）是很常见异常，在 JDK 14 以前遇到 NPE 异常，能得到信息有限，JDK 15 引入了一项名为“Helpful NullPointerExceptions”的新功能，这项功能改进了 NullPointerException (NPE) 的诊断。在之前的 JDK 版本中，当发生 NullPointerException 时，异常信息通常并不提供足够的上下文来帮助开发人员定位问题的具体位置。



示例代码：

```java
class A {
    String s;
    public A(String s) {
        this.s = s;
    }
}

class B {
    A a;
    public B(A a) {
        this.a = a;
    }
}

class C {
    B b;
    public C(B b) {
        this.b = b;
    }
}

public class BetterNullPointerReports {

    public static void main(String[] args) {
        C[] ca = {
                new C(new B(new A(null))),
                new C(new B(null)),
                new C(null)
        };

        for (C c : ca) {
            try {
                System.out.println(c.b.a.s);
            } catch (NullPointerException npe) {
                System.out.println(npe);
            }
        }
    }
}
```

在 JDK 14 及之前的版本中，输出结果：

```sh
# 你根本看不出哪里出了问题
null
java.lang.NullPointerException
java.lang.NullPointerException
```

在 JDK 15 及之后的版本中，输出结果：

```sh
# 得到更详细的 NPE 信息
null
java.lang.NullPointerException: Cannot read field "s" because "c.b.a" is null
java.lang.NullPointerException: Cannot read field "a" because "c.b" is null
```



### 清道夫：finally

当程序发生了非预期的异常，那么程序会终止运行，但是对于很多需要执行清理操作，这是不可接受的，例如：

* 关闭资源：在 `try` 块中打开的资源，如文件、数据库连接、网络连接等，需要在完成操作后确保被正确关闭
* 释放锁：在并发编程中，可能会使用锁来同步代码。在释放锁之前，如果发生异常，可能会导致其他线程无法获取锁
* 回滚事务：在数据库编程中，可能需要在事务中执行一系列操作。如果这些操作中的任何一个失败，事务需要回滚
* 恢复状态：在执行某些操作时，可能需要更改对象或系统的状态。在操作完成后，可能需要恢复原始状态

对于以上的程序来说，finally 就非常重要了，它可以解决以上程序的清理操作。



示例代码：

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class FinallyExample {

    public static void main(String[] args) {
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader("example.txt"));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    System.err.println("Error closing file: " + e.getMessage());
                }
            }
        }
    }
}
```

在以上代码中，无论程序是否出错，`finally` 都可以确保文件被正确关闭



### 异常的约束

Java 在面向对象中对异常存在颇多约束和限制，其主要目的如下：

* 保持子类型可替换性：当子类覆盖父类的方法或实现接口的方法时，子类的方法应该满足父类或接口方法的约定
* 避免意外的异常：如果子类方法可以抛出任意异常，那么调用者在处理异常时可能遇到意外的异常类型，导致程序出错
* 提高代码可读性：通过限制异常的继承和实现规则，可以使得代码更加清晰和易于理解
* 促进良好的设计实践：如果子类方法可以抛出任意异常，那么程序员可能会过度依赖异常来处理错误情况，导致代码难以维护



在接口和继承中使用异常，需要遵循以下规则：

1. 子类可以抛出与接口或者父类方法相同的异常。
2. 子类可以不抛出任何异常，即使接口或父类方法声明了异常。这意味着实现类的方法已经处理了这些异常。
3. 子类可以抛出接口方法或父类声明异常的相同类型的异常，因为子类异常依然符合接口方法的约定。



代码示例：

```java
class CustomException extends RuntimeException {}
class CustomExceptionChild extends CustomException {}
interface MyInterface {
    void myMethod() throws CustomException;
}

class MyClass1 implements MyInterface {
    // 1：抛出与接口方法相同异常
    @Override
//    public void myMethod() throws FileNotFoundException {     // 编译错误，不能抛出不同类型的异常
    public void myMethod() throws CustomException {
        // ...
    }
}

class MyClass2 implements MyInterface {
    // 2：即使不抛出任何异常，也没有问题
    @Override
    public void myMethod() {
    }
}

class MyClass3 implements MyInterface {
    // 3: 抛出接口方法声明异常的子类异常（或者父类，既相同类型即可）
    @Override
    public void myMethod() throws CustomExceptionChild {
        // ...
    }
}
```



### try-with-resources

在 Java 7 中，关于自动管理资源。在处理需要关闭的资源（如文件、数据库连接、网络连接等）有了更好的选择，那就是使用 `try-catch-finally` 进行处理，它对比 `finally` 具有以下优势：

1. **简化代码**：相比 `finally` 显示关闭资源，使用 Try-With-Resources，可以自动关闭资源，从而使代码更简洁、易读。
2. **避免资源泄漏**：使用 Try-With-Resources 能够确保在退出 `try` 代码块时自动关闭资源，降低资源泄漏的风险。
3. **减少错误**：Try-With-Resources 能够正确地处理资源关闭过程中的异常，并提供完整的异常信息，有助于减少错误。



示例代码：

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TryWithResourcesExample {

    public static void main(String[] args) {
        String fileName = "example.txt";

        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }
}
```

在这个示例中，我们使用 Try-With-Resources 语句创建了一个 `BufferedReader` 实例。`BufferedReader` 实现了 `Closeable` 接口，因此在退出 `try` 代码块时，`reader` 会自动调用 `close()` 方法以释放资源。

为了一探 Try-With-Resources 的究竟，我们可以创建自定义的 `AutoCloseable` 类：

```java
class Reporter implements AutoCloseable {
    String name = getClass().getSimpleName();
    public Reporter() {
        System.out.println("Creating " + name);
    }
    @Override
    public void close() throws Exception {
        System.out.println("Closing " + name);
    }
}
class First extends Reporter {}
class Second extends Reporter {}

public class AutoCloseableDetails {
    public static void main(String[] args) {
        try (First f = new First(); Second s = new Second()) {
            System.out.println("In body");
        } catch (Exception e) {
            System.out.println("Exception caught");
        }
    }
}
```

输出结果：

```sh
Creating First
Creating Second
In body
Closing Second
Closing First
```

退出 try 块会调用两个对象的 close() 方法，并以与创建顺序相反的顺序关闭它们。（顺序很重要）。

使用 Try-With-Resource 是很安全的，假设你随意在 Try 头使用对象，会出现编译错误：

```java
class Anything {}

public class TryAnything {
    public static void main(String[] args) {
        // 假设我们定义的类，不是 AutoCloseable 的对象，会出现编译错误
        try (Anything a = new Anything()) {     // compile error
            System.out.println("In body");
        } catch (Exception e) {
            System.out.println("Exception caught");
        }
    }
}
```



### 异常类型匹配

Java 在抛出异常时，会根据异常类型进行匹配。异常处理程序会从上到下依次检查 `catch` 子句，看它们是否与抛出的异常类型兼容。当发现兼容的 `catch` 子句时，Java 就会执行该子句的代码来处理异常。请注意，Java 只会执行与抛出异常类型兼容的第一个 `catch` 子句。

示例代码：

```java
public class ExceptionMatchingExample {
    public static void main(String[] args) {
        try {
            // ... Some code that may throw exceptions ...
            throw new FileNotFoundException("File not found");
        } catch (FileNotFoundException e) {
            System.out.println("Handling FileNotFoundException: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("Handling IOException: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Handling general exception: " + e.getMessage());
        }
    }
}
```

在这个示例中，我们抛出了一个 `FileNotFoundException`，Java 会从上到下检查 `catch` 子句，看它们是否与 `FileNotFoundException` 兼容。因为 `FileNotFoundException` 是 `IOException` 的子类，它与 `FileNotFoundException` 和 `IOException` 的 `catch` 子句兼容。但是，Java 只会执行第一个兼容的 `catch` 子句，即 `FileNotFoundException` 子句。如果没有找到兼容的 `catch` 子句，Java 会继续在调用栈中查找异常处理程序，直到找到一个合适的处理程序或者程序终止。

输出结果：

```java
Handling FileNotFoundException: File not found
```



### 使用指南

异常看似简单易懂，但在处理过程中还需要遵循许多最佳实践，例如：

* 除非你知道如何处理，否则不要捕获异常（错误处理代码太多，容易干扰主线代码的逻辑和可读性）
* 不要生吞异常：捕获异常不进行处理会导致异常消失，从而对于线上问题排查，无从下手
* 捕获具体异常：尽量捕获具体的异常类，而不是捕获泛化的 Exception 类
* 尽可能的使用多重异常捕获来简化重复代码，并且提高代码的可读性
* 尽可能的使用 Try-With-Resources 清理资源
* 自定义异常：在需要时，为特定于你的应用程序的异常情况创建自定义异常



### 检查型异常是 shit ?

检查型异常（checked exceptions）在 Java 中引发了很多争议。有些人认为它们是一种有益的设计，可以提高代码的可靠性，而另一些人则认为它们是一种糟糕的设计，会导致代码冗余和难以维护，例如 Martin Fowler （《UML 精粹》、《重构》）作者，也曾在博客发表称：

> 总的来说，我认为异常很不错，但是 Java 的检查型异常要比好处多

那么检查型异常究竟带来了什么问题 ？ 常见的槽点有：

1. 强制错误处理：检查型异常强制开发者处理异常情况，导致主线代码中充斥着大量和业务逻辑无关的代码
2. 代码冗余：检查型异常可能导致大量的 try-catch 代码块，增加代码冗余，影响代码可读性
3. 异常传递：对于一些需要在多层方法调用中传递异常的情况，检查型异常可能导致开发者不得不为每个方法添加异常声明



### Go 也没有异常啊

最几年 Go 语言的成功让很多人加深了这一观点，Go 语言没有检查型异常的概念，但它们的代码依然可以具有很高的可靠性。这表明检查型异常并非是提高代码可靠性的唯一方法。Go 语言的设计者们有意避免了引入检查型异常，主要有以下原因：

* 代码简洁性：Go 语言的设计者们希望保持代码简洁，避免因为异常处理而产生的大量冗余代码。
* 显示错误处理：Go 语言鼓励开发者显式地处理错误，而不是通过异常机制隐式地处理。
* 降低复杂性：异常机制会增加程序的复杂性。Go 语言的设计者们希望通过避免引入异常机制，让程序更简单易懂。
* 性能开销：异常处理机制可能会带来一定的性能开销，通过返回 error 类型，可以避免这种性能开销。



示例代码：

```go
package main

import (
    "errors"
    "fmt"
)

func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 2)
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result)
    }

    result, err = divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result)
    }
}
```

在这个示例中，我们定义了一个名为`divide`的函数，它接受两个整数参数`a`和`b`，计算它们的商。如果`b`为零，函数将返回一个非空的`error`类型值，以指示发生了错误。否则，函数将返回商和一个空`error`值。在 `main` 函数中，我们调用`divide`两次，一次使用一个非零除数，另一次使用零作为除数。对于第一次调用，`divide`将返回一个空的`error`值，我们就可以打印出计算结果。对于第二次调用，`divide`将返回一个非空的`error`值，我们使用`if err != nil`来检查这个值是否为`nil`，如果不是，就打印错误信息。

输出结果：

```sh
Result: 5
Error: division by zero
```

以上就是 Go 在处理异常的方式。尽管 Go 语言没有引入检查型异常，但它依然具备了一套有效的错误处理机制。使用多值返回（value, error）的方式，可以让代码更简洁、易读，同时鼓励开发者显式地处理错误。这种设计理念与 Go 语言追求简洁、高效的目标相一致。



### 陈述总结

最后，关于检查型异常在某些场景下可以提高代码的可靠性和健壮性，但在另一些场景下可能导致代码冗余和难以维护。在很多人看来弊大于利了。然而，这并不意味着在所有情况下都不应该使用检查型异常。在某些场景下，合理地使用检查型异常可以帮助提高代码的健壮性和可靠性。关键是要明确异常处理的目的，在实际开发中，可以根据需要和团队的编码规范来权衡使用检查型异常。
