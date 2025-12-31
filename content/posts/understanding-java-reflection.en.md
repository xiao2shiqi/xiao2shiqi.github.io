+++
date = '2023-05-21T14:17:27+08:00'
draft = false
title = 'Understanding and Applying Java Reflection'
tags = ["Java"]
+++


### Overview

Reflection is a mechanism that provides the ability to dynamically obtain class information and manipulate class members (fields, methods, constructors, etc.) at runtime. Through reflection, we can perform dynamic lookups and calls at runtime when the specific type is unknown during compilation. Although Java is a static compiled language, the inclusion of reflection provides an alternative way to operate on objects directly, giving Java some flexibility and dynamism. We will explore it in detail in this article.

#### Why is Reflection Needed?

The main reasons Java needs reflection include:

1. **Dynamic Loading and Creation of Classes at Runtime**: Classes in Java are loaded at compile time, but sometimes there's a need to dynamically load and create required classes based on certain conditions during runtime. Reflection provides this capability, making programs more flexible and dynamic.
2. **Dynamic Method Invocation**: Dynamically calling methods in a class based on the class and object obtained through reflection is extremely useful for class enhancement frameworks (like Spring's `AOP`), security frameworks (verifying permissions before method calls), and injecting general business logic (like logging).
3. **Retrieving Class Information**: Through reflection, you can obtain various information about a class, such as its name, parent class, interfaces, fields, and methods. This allows us to inspect a class's properties and methods at runtime and operate on them as needed.

#### Example Code

Here is a simple example showing basic reflection operations:

```java
import java.lang.reflect.Method;

public class ReflectionExample {
    public static void main(String[] args) {
        // Assume a class name is unknown at compile time but its method needs to be called at runtime
        String className = "com.example.MyClass";

        try {
            // Use reflection to dynamically load the class
            Class<?> clazz = Class.forName(className);

            // Use reflection to get a specific method
            Method method = clazz.getMethod("myMethod");

            // Use reflection to create an object
            Object obj = clazz.getDeclaredConstructor().newInstance();

            // Use reflection to invoke the method
            method.invoke(obj);

        } catch (ClassNotFoundException e) {
            System.out.println("Class not found: " + className);
        } catch (NoSuchMethodException e) {
            System.out.println("Method not found");
        } catch (Exception e) {
            System.out.println("Other exception: " + e.getMessage());
        }
    }
}
```

In this example, we assume specific class and method names are unknown at compile time, but need to be loaded, instantiated, and called based on runtime conditions. Using reflection, we pass the class name as a string and use `Class.forName()` to load it. Then, we use `getMethod()` to get the method object, `newInstance()` (or `getDeclaredConstructor().newInstance()`) to create an instance, and `invoke()` to call the method.

#### Usage Scenarios

Great technology is only as good as its practical application. In daily development, reflection is frequently seen in:

1. **Frameworks and Libraries**: Many frameworks use reflection for plugin-based architectures or extension mechanisms. For example, Spring uses reflection for Dependency Injection and `AOP` (Aspect-Oriented Programming).
2. **ORM (Object-Relational Mapping)**: ORM frameworks map object models to relational databases. Through reflection, they dynamically read object attributes and annotations at runtime to generate `SQL` statements and execute DB operations.
3. **Dynamic Proxy**: A common design pattern implemented via reflection. It allows creating proxy objects at runtime and intercepting calls to the original object's methods, which is useful for logging, performance statistics, and transaction management.
4. **Debugging Tools**: During development and debugging, it's sometimes necessary to inspect object structures or call methods dynamically for testing. Reflection provides a convenient way to inspect and manipulate internal object info, e.g., using `getDeclaredFields()` or `getMethod()`.
5. **Unit Testing**: Sometimes you need to mock or replace object behavior for effective testing. Reflection allows creating mock instances at runtime and replacing original objects to control and verify test behavior.

### Class Object

The `Class` object is the first step in reflection. Since any runtime use of type information requires a reference to its `Class` object, it is core to reflection. It represents the metadata of a Java class, including its structure, fields, methods, and other information.

Common ways to obtain a `Class` object:

```java
// Using the class name
Class<?> clazz = Class.forName("com.example.MyClass");

// Using a class literal
Class<?> clazz = MyClass.class;

// Using an object's getClass() method
MyClass obj = new MyClass();
Class<?> clazz = obj.getClass();
```

> Note: If `Class.forName()` cannot find the class, it throws a `ClassNotFoundException`.

Once you have the `Class` object, you can perform various reflection operations:

```java
String className = clazz.getName(); // Get fully qualified name
int modifiers = clazz.getModifiers(); // Get modifiers like public, abstract
Class<?> superClass = clazz.getSuperclass(); // Get direct parent class
Class<?>[] interfaces = clazz.getInterfaces(); // Get array of implemented interfaces
Constructor<?>[] constructors = clazz.getConstructors(); // Get public constructors
Method[] methods = clazz.getMethods(); // Get public methods
Field[] fields = clazz.getFields(); // Get public fields
Object obj = clazz.getDeclaredConstructor().newInstance(); // Create instance
```

### Type Checking

Reflection code often involves checking and judging types to perform specific logical operations. Here are several ways to check types in Java:

#### `instanceof` Keyword

The `instanceof` operator checks if an object is an instance of a specific class or its subclass. It returns a boolean.

**1: Avoiding Type Casting Errors**

Before casting, `instanceof` can check the actual type to avoid `ClassCastException`:

```java
if (obj instanceof MyClass) {
    MyClass myObj = (MyClass) obj;
    // Perform operations specific to MyClass
}
```

**2: Polymorphism Check**

Judge specific types to execute different logic:

```java
if (animal instanceof Dog) {
    Dog dog = (Dog) animal;
    dog.bark();
} else if (animal instanceof Cat) {
    Cat cat = (Cat) animal;
    cat.meow();
}
```

**3: Interface Implementation Check**

Check if an object implements a specific interface:

```java
if (obj instanceof MyInterface) {
    MyInterface myObj = (MyInterface) obj;
    myObj.doSomething();
}
```

**4: Inheritance Relationship Check**

Determine if an object is a subclass instance:

```java
if (obj instanceof MyBaseClass) {
    MyBaseClass myObj = (MyBaseClass) obj;
    // Perform MyBaseClass operations
}
```

`instanceof` has limitations:
1. **Cannot match primitive types**: it works only on reference types.
2. **Cannot match against Class object types**: you can only compare it with named types.
3. **Cannot judge generic type parameters**: due to type erasure, `instanceof` cannot directly check if an object is an instance of a generic type like `ArrayList<String>`.

> While `instanceof` is convenient, overuse can indicate a design flaw, potentially violating good object-oriented principles. You should favor polymorphism and interfaces over excessive type checking.

#### `isInstance()` Function

The `java.lang.Class` class provides the `isInstance()` method, which is more suitable for reflection scenarios:

```java
Class<?> clazz = MyClass.class;
boolean result = clazz.isInstance(obj);
```

Differences between `isInstance()` and `instanceof`:
1. `isInstance()` takes an object parameter, whereas `instanceof` takes a reference type as its operand. `isInstance()` allows dynamic type determination, while `instanceof` requires the type to be specified at compile time.
2. `isInstance()` is a general method applicable to any `Class` object. `instanceof` is only for reference types.
3. `isInstance()` performing checks at runtime. `instanceof` is a compile-time check mechanism.
4. `isInstance()` can use wildcard types (`<?>`) to check generic information, whereas `instanceof` cannot directly check generic parameters due to erasure.

### Proxy

#### Proxy Pattern

The Proxy pattern is a structural design pattern where a proxy object is used to control access to an original object. The proxy acts as an intermediary, enabling additional control or extensions without modifying the original object.

```java
// Abstract object interface
interface Image {
    void display();
}

// Real object
class RealImage implements Image {
    private String fileName;

    public RealImage(String fileName) {
        this.fileName = fileName;
        loadFromDisk();
    }

    private void loadFromDisk() {
        System.out.println("Loading image:" + fileName);
    }

    @Override
    public void display() {
        System.out.println("Displaying image:" + fileName);
    }
}

// Proxy object
class ImageProxy implements Image {
    private String filename;
    private RealImage realImage;

    public ImageProxy(String filename) {
        this.filename = filename;
    }

    @Override
    public void display() {
        if (realImage == null) {
            realImage = new RealImage(filename);
        }
        realImage.display();
    }
}

public class ProxyPatternExample {
    public static void main(String[] args) {
        Image image = new ImageProxy("test_10mb.jpg");
        // First access: loads the real object
        image.display();
        // Second access: uses the already loaded object
        image.display();
    }
}
```

Output:
```sh
Loading image:test_10mb.jpg
Displaying image:test_10mb.jpg
Displaying image:test_10mb.jpg
```

In the proxy object, by controlling the loading and access to the real object, we implement lazy loading and additional operations.

#### Dynamic Proxy

Java dynamic proxy is a mechanism for dynamically generating proxy classes and objects at runtime, without needing to pre-define them. It uses Java reflection and inserts logic before or after method calls.

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

// Abstract object interface
interface Image {
    void display();
}

// Real object
class RealImage implements Image {
    private String filename;

    public RealImage(String filename) {
        this.filename = filename;
        loadFromDisk();
    }

    private void loadFromDisk() {
        System.out.println("Loading image: " + filename);
    }

    public void display() {
        System.out.println("Displaying image: " + filename);
    }
}

// Proxy handler implementation
class ImageProxyHandler implements InvocationHandler {

    private Object realObject;

    public ImageProxyHandler(Object realObject) {
        this.realObject = realObject;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        Object result = null;
        if (method.getName().equals("display")) {
            System.out.println("Proxy: before display");
            result = method.invoke(realObject, args);
            System.out.println("Proxy: after display");
        }
        return result;
    }
}

public class DynamicProxyExample {

    public static void main(String[] args) {
        Image realImage = new RealImage("image.jpg");
        Image proxyImage = (Image) Proxy.newProxyInstance(
            Image.class.getClassLoader(), 
            new Class[]{Image.class}, 
            new ImageProxyHandler(realImage)
        );
        proxyImage.display();
    }
}
```

Output:
```sh
Loading image: image.jpg
Proxy: before display
Displaying image: image.jpg
Proxy: after display
```

Dynamic proxies offer more flexibility in controlling and extending methods without explicit proxy class creation. They are commonly used in `AOP` (Aspect-Oriented Programming) for tasks like logging and transaction management.

### Violating Access Rights

In Java, reflection can bypass access restrictions on private members.

```java
import java.lang.reflect.Field;

class MyClass {
    private String privateField = "Private Field Value";
}

public class ReflectionExample {

    public static void main(String[] args) throws Exception {
        MyClass myObj = new MyClass();
        Field privateField = MyClass.class.getDeclaredField("privateField");

        // Cancel access restriction
        privateField.setAccessible(true);

        // Get value
        String fieldValue = (String) privateField.get(myObj);
        System.out.println("Original value of privateField: " + fieldValue);

        // Modify value
        privateField.set(myObj, "New Field Value");

        // Verify modification
        fieldValue = (String) privateField.get(myObj);
        System.out.println("Modified value of privateField: " + fieldValue);
    }
}
```

Output:
```java
Original value of privateField: Private Field Value
Modified value of privateField: New Field Value
```

Through reflection, you can also:
* Call private methods.
* Instantiate non-public constructors.
* Access/modify static fields and methods.
* Bypass access modifier checks.

While reflection can break through private access, it should be used with caution. Private members are typically internal details meant for encapsulation. Over-reliance can harm code readability, stability, and security.

### Summary

Since its introduction in `JDK 1.1`, reflection has been widely used. It provides developers with the ability to dynamically obtain class information, call methods, and access fields. Historically, it has been used in framework and tool development, dynamic class loading, annotation processing, and the proxy pattern. It adds significant flexibility, extensibility, and dynamism to Java. Today, reflection remains vital in areas like `ORM`, `AOP`, dependency injection, and unit testing. Popular frameworks like `Spring`, `Hibernate`, and `JUnit` make extensive use of it. Reflection technology continues to evolve, likely seeing further improvements in performance, security, and modularity in future Java platforms. However, it must be used prudently as it involves dynamic code generation and bypassing access limits, which can harm performance and readability, or introduce security vulnerabilities if used improperly. Developers should fully understand its principles and risks and follow best practices.
