+++
date = '2023-04-09T14:28:31+08:00'
draft = false
title = 'Usage and Reflections on Java Exception Handling'
tags = ["Java"]
+++

### Concepts

The concept of exception handling originated in early programming languages such as LISP, PL/I, and CLU. These languages first introduced exception handling mechanisms to detect and handle error conditions during program execution. Exception handling mechanisms were subsequently widely adopted and developed in programming languages such as Ada, Modula-3, C++, Python, and Java. In Java, exception handling provides a method for handling errors and abnormal situations while the program is running. The exception handling mechanism allows a program to continue execution when it encounters an error, rather than crashing immediately. This mechanism makes the program more robust and fault-tolerant. Exceptions are divided into two categories: Checked Exceptions and Unchecked Exceptions.

**Checked Exceptions:**

Checked exceptions refer to those that must be handled at compile time. They are usually caused by programmer errors or problems with external resources. Examples include `IOException`, `FileNotFoundException`, etc. Checked exceptions must be declared in the method signature using the `throws` keyword, or caught and handled in a `try-catch` block within the method body.

**Unchecked Exceptions:**

Unchecked exceptions refer to those that are not mandatory to handle at compile time. They are usually caused by programming errors, such as `NullPointerException`, `ArrayIndexOutOfBoundsException`, etc. Unchecked exceptions inherit from the `java.lang.RuntimeException` class and do not need to be declared in the method signature, nor do they need to be forcibly caught and handled.

The relationship between them is shown below:

![image-20250215142923833](https://s2.loli.net/2025/02/15/d68wjyv4cUHAIGs.png)

### Exception Handling

Java uses the `try/catch` keywords for catching exceptions and the `throw` keyword to declare or throw an exception. Example code is as follows:

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

In this example, we attempt to get the length of a `null` string. When calling `nullString.length()`, a `NullPointerException` is thrown. We use a `try-catch` statement to catch and handle the exception.

### Custom Exceptions

Official Java exceptions cannot foresee all possible errors. Sometimes you need to combine them with your own business scenarios, such as the following cases:

1. When built-in Java exception classes cannot accurately describe the abnormal situation you encounter.
2. When you need to create a specific set of exceptions for a particular domain or business logic.
3. When you want to provide more context information or specific error codes to the caller through custom exception classes.

Building a specific exception is simple: inherit from an existing exception class (preferably one with a similar meaning). For example, here we create an exception representing an insufficient account balance:

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

Next, we use this custom exception in business logic code:

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

The caller can catch and handle this custom exception:

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

As seen, custom exceptions allow us to more clearly express abnormal situations that may occur in business logic while providing more contextual information to the caller. We also use the `java.util.logging` tool to log the output.

### Multi-Catch

In early versions of Java, handling multiple exceptions without a common base class required writing a `catch` statement for each exception type, as follows:

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
            // Choose which exception to throw based on parameters
            if (args.length > 0 && "type1".equals(args[0])) {
                throw new CustomException1("This is a custom exception type 1.");
            } else {
                throw new CustomException2("This is a custom exception type 2.");
            }
        } catch (CustomException1 e) {
            // Execute this block when CustomException1 occurs
            System.err.println("Error occurred: " + e.getMessage());
        } catch (CustomException2 e) {
            // Execute this block when CustomException2 occurs
            System.err.println("Error occurred: " + e.getMessage());
        }
    }
}
```

Such code is not only hard to read but also not concise enough.

The multi-catch mechanism allows catching multiple exception types in a single `catch` statement. This method avoids code duplication and makes exception handling more concise. Here is an example:

```java
public class MultiCatchExample {

    public static void main(String[] args) {
        try {
            // Choose which exception to throw based on parameters
            if (args.length > 0 && "type1".equals(args[0])) {
                throw new CustomException1("This is a custom exception type 1.");
            } else {
                throw new CustomException2("This is a custom exception type 2.");
            }
        } catch (CustomException1 | CustomException2 e) {
            // Execute this block when either CustomException1 or CustomException2 occurs
            System.err.println("Error occurred: " + e.getMessage());
        }
    }
}
```

### Rethrowing Exceptions

In some cases, you may want to pass an exception to the caller for handling instead of handling it in the current method. Or you may need to perform some processing operations when catching an exception, such as logging, resource cleanup, or adding extra contextual information. In this case, you can handle the exception in the `catch` block and then rethrow the original exception or throw a new exception containing extra information:

```java
public class RethrowExceptionExample {
    public static void main(String[] args) {
        try {
            doSomething();		// Method that may throw an exception
        } catch (IOException e) {
            // Exception handling logic
            System.err.println("An error occurred: " + e.getMessage());            
            // Rethrow the exception
            throw e;
        }
    }
}
```

### Better NPE

NPE (NullPointerExceptions) are very common exceptions. Before JDK 14, the information obtained from an NPE was limited. JDK 15 introduced a new feature called "Helpful NullPointerExceptions," which improves the diagnosis of NullPointerExceptions. In previous JDK versions, when a NullPointerException occurred, the exception message usually did not provide enough context to help developers locate the specific location of the problem.

Example code:

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

In JDK 14 and earlier versions, the output:

```sh
# You can't see what went wrong at all
null
java.lang.NullPointerException
java.lang.NullPointerException
```

In JDK 15 and later versions, the output:

```sh
# Get more detailed NPE information
null
java.lang.NullPointerException: Cannot read field "s" because "c.b.a" is null
java.lang.NullPointerException: Cannot read field "a" because "c.b" is null
```

### The Scavenger: finally

When an unexpected exception occurs, the program terminates. However, for many operations that require cleanup, this is unacceptable, such as:

* Closing resources: Resources opened in the `try` block, such as files, database connections, network connections, etc., need to be correctly closed after completion.
* Releasing locks: In concurrent programming, locks may be used to synchronize code. If an exception occurs before the lock is released, it may prevent other threads from acquiring the lock.
* Rolling back transactions: In database programming, a series of operations may need to be performed in a transaction. If any of these operations fail, the transaction needs to be rolled back.
* Restoring state: Some operations may require changing the state of an object or system. After the operation is complete, the original state may need to be restored.

For the above programs, `finally` is very important; it can handle these cleanup operations.

Example code:

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

In the above code, regardless of whether an error occurs, `finally` ensures that the file is correctly closed.

### Constraints on Exceptions

Java has many constraints and limitations on exceptions in object-oriented programming, with the following main purposes:

* Maintain subtype substitutability: When a subclass overrides a parent class method or implements an interface method, the subclass method should satisfy the contract of the parent class or interface method.
* Avoid unexpected exceptions: If a subclass method can throw arbitrary exceptions, the caller may encounter unexpected exception types when handling exceptions, leading to program errors.
* Improve code readability: By limiting exception inheritance and implementation rules, the code can be made clearer and easier to understand.
* Promote good design practices: If a subclass method can throw arbitrary exceptions, programmers might over-rely on exceptions to handle error conditions, making the code hard to maintain.

When using exceptions in interfaces and inheritance, the following rules must be followed:

1. A subclass can throw the same exceptions as the interface or parent class method.
2. A subclass can choose not to throw any exceptions, even if the interface or parent class method declares them. This means the implementation class method has already handled these exceptions.
3. A subclass can throw exceptions of the same type as those declared by the interface or parent class (or their subclasses), as the subclass exception still conforms to the interface method's contract.

Example code:

```java
class CustomException extends RuntimeException {}
class CustomExceptionChild extends CustomException {}
interface MyInterface {
    void myMethod() throws CustomException;
}

class MyClass1 implements MyInterface {
    // 1: Throw the same exception as the interface method
    @Override
//    public void myMethod() throws FileNotFoundException {     // Compilation error, cannot throw a different type of exception
    public void myMethod() throws CustomException {
        // ...
    }
}

class MyClass2 implements MyInterface {
    // 2: No problem even if no exceptions are thrown
    @Override
    public void myMethod() {
    }
}

class MyClass3 implements MyInterface {
    // 3: Throw a subclass exception of the one declared in the interface (or the same type)
    @Override
    public void myMethod() throws CustomExceptionChild {
        // ...
    }
}
```

### try-with-resources

Introduced in Java 7, regarding automatic resource management. There is a better option for handling resources that need to be closed (such as files, database connections, network connections, etc.): using `try-with-resources`. It has the following advantages over `try-catch-finally`:

1. **Simpler code**: Compared to explicitly closing resources in `finally`, using try-with-resources automatically closes resources, making the code more concise and readable.
2. **Avoid resource leaks**: Using try-with-resources ensures that resources are automatically closed upon exiting the `try` block, reducing the risk of resource leaks.
3. **Fewer errors**: Try-with-resources can correctly handle exceptions during the resource closing process and provide complete exception information, helping to reduce errors.

Example code:

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

In this example, we use a try-with-resources statement to create a `BufferedReader` instance. `BufferedReader` implements the `AutoCloseable` interface, so when exiting the `try` block, `reader` automatically calls the `close()` method to release resources.

To take a closer look at try-with-resources, we can create a custom `AutoCloseable` class:

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

Output:

```sh
Creating First
Creating Second
In body
Closing Second
Closing First
```

Exiting the try block calls the `close()` method of both objects and closes them in reverse order of creation. (Order is important).

Using try-with-resources is safe; if you use an object in the try header that is not `AutoCloseable`, a compilation error will occur:

```java
class Anything {}

public class TryAnything {
    public static void main(String[] args) {
        // If the class we defined is not an AutoCloseable object, a compilation error occurs
        try (Anything a = new Anything()) {     // compile error
            System.out.println("In body");
        } catch (Exception e) {
            System.out.println("Exception caught");
        }
    }
}
```

### Exception Type Matching

When Java throws an exception, it matches based on the exception type. Exception handlers check `catch` clauses from top to bottom to see if they are compatible with the thrown exception type. When a compatible `catch` clause is found, Java executes that clause's code to handle the exception. Note that Java only executes the first `catch` clause compatible with the thrown exception type.

Example code:

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

In this example, we throw a `FileNotFoundException`. Java checks `catch` clauses from top to bottom to see if they are compatible with `FileNotFoundException`. Since `FileNotFoundException` is a subclass of `IOException`, it is compatible with both `FileNotFoundException` and `IOException` `catch` clauses. However, Java only executes the first compatible `catch` clause, which is the `FileNotFoundException` clause. If no compatible `catch` clause is found, Java continues searching the call stack for an exception handler until a suitable handler is found or the program terminates.

Output:

```
Handling FileNotFoundException: File not found
```

### Guidance for Use

Exceptions seem simple, but there are many best practices to follow during handling, such as:

* Don't catch an exception unless you know how to handle it (too much error handling code can easily interfere with the logic and readability of main code).
* Don't swallow exceptions: Catching an exception without handling it causes it to disappear, making it impossible to troubleshoot online issues.
* Catch specific exceptions: Try to catch specific exception classes rather than the generalized `Exception` class.
* Use multi-catch as much as possible to simplify repetitive code and improve readability.
* Use Try-With-Resources to clean up resources whenever possible.
* Custom exceptions: Create custom exceptions for abnormal situations specific to your application when needed.

### Are Checked Exceptions... Bad?

Checked exceptions have sparked much controversy in Java. Some consider them a beneficial design that improves code reliability, while others view them as a poor design leading to code redundancy and maintenance difficulties. For instance, Martin Fowler (author of *UML Distilled*, *Refactoring*) has stated in his blog:

> On the whole I think exceptions are good, but Java’s checked exceptions are more trouble than they are worth.

So what problems do checked exceptions bring? Common complaints include:

1. Forced error handling: Checked exceptions force developers to handle abnormal situations, resulting in main code being filled with many codes unrelated to business logic.
2. Code redundancy: Checked exceptions can lead to a large number of `try-catch` blocks, increasing redundancy and affecting readability.
3. Exception propagation: For cases where an exception needs to be passed through multiple layers of method calls, checked exceptions may force developers to add exception declarations to every method.

### Go Doesn't Have Exceptions Either

The success of the Go language in recent years has reinforced this view. Go has no concept of checked exceptions, yet its code can still have high reliability. This shows that checked exceptions are not the only way to improve code reliability. The designers of Go intentionally avoided introducing checked exceptions for several reasons:

* Code simplicity: Go's designers wanted to keep code simple and avoid a lot of redundant code caused by exception handling.
* Explicit error handling: Go encourages developers to handle errors explicitly rather than implicitly through exception mechanisms.
* Reduced complexity: Exception mechanisms increase program complexity. Go's designers wanted to make programs simpler and easier to understand by avoiding exception mechanisms.
* Performance overhead: Exception handling mechanisms may bring a certain performance overhead; by returning an `error` type, this can be avoided.

Example code:

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

In this example, we define a function named `divide` that takes two integers `a` and `b` and calculates their quotient. If `b` is zero, the function returns a non-null `error` value to indicate an error occurred. Otherwise, it returns the quotient and a null `error` value. In the `main` function, we call `divide` twice. For the first call, `divide` returns a null `error`, and we print the result. For the second call, `divide` returns a non-null `error`, and we use `if err != nil` to check this value; if it's not null, we print the error message.

Output:

```sh
Result: 5
Error: division by zero
```

This is how Go handles errors. Although Go does not introduce checked exceptions, it still possesses an effective error handling mechanism. Using multiple return values (value, error) makes the code more concise and readable while encouraging developers to handle errors explicitly. This design philosophy aligns with Go's goal of simplicity and efficiency.

### Summary

Finally, while checked exceptions can improve code reliability and robustness in some scenarios, they may lead to redundancy and maintenance difficulties in others. To many, the disadvantages outweigh the advantages. However, this doesn't mean checked exceptions should never be used. In certain cases, reasonable use of checked exceptions can help improve code robustness and reliability. The key is to clarify the purpose of exception handling. In actual development, one can weigh the use of checked exceptions based on needs and the team's coding conventions.
