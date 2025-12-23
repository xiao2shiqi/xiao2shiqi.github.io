+++
date = '2023-05-21T14:17:27+08:00'
draft = false
title = 'Understanding and Applying Java Reflection'
tags = ["Java"]
+++

### 1. Overview

Reflection allows a Java program to inspect or manipulate its own internal structure at runtime. It can access class names, fields, methods, and constructors without knowing them at compile time.

### 2. Why Reflection?

- **Dynamic Loading**: `Class.forName(name)` allows loading plugins or drivers at runtime.
- **Dynamic Invocation**: Frameworks like Spring use it to call methods on Bean instances.
- **Generic Inspection**: Writing code that can work with any object (e.g., serializing a JSON string).

### 3. Usage Scenarios

- **Frameworks**: Spring (Dependency Injection), JUnit (finding `@Test` methods).
- **ORM**: Hibernate/MyBatis mapping DB rows to POJO fields.
- **Dynamic Proxy**: Routing method calls at runtime.
- **Unit Testing**: Accessing private fields or methods for validation.

### 4. The `Class` Object

The `java.lang.Class` object is the entry point.
Ways to get it:
- `MyClass.class`
- `obj.getClass()`
- `Class.forName("com.package.MyClass")`

With a `Class` object, you can call `newInstance()`, `getMethods()`, `getFields()`, etc.

### 5. Type Checking

- **`instanceof`**: A keyword for compile-time types.
- **`isInstance(obj)`**: The dynamic reflection version. 

### 6. Dynamic Proxy

Useful for AOP (Aspect Oriented Programming), where you want to wrap an object's methods with additional logic (logging, transactions).

```java
InvocationHandler handler = new MyHandler(realObject);
MyInterface proxy = (MyInterface) Proxy.newProxyInstance(
    MyInterface.class.getClassLoader(),
    new Class[] { MyInterface.class },
    handler
);
```

### 7. Violating Access Rights

Reflection can access private members.
```java
Field privateField = MyClass.class.getDeclaredField("secret");
privateField.setAccessible(true);
String value = (String) privateField.get(obj);
```
*Note: This can break encapsulation and should be used with extreme caution.*

### 8. Summary

Reflection is the "magic" underlying major Java frameworks. While it offers unmatched flexibility, it comes with costs:
- **Performance**: Reflection is slower than direct calls.
- **Security**: It can be restricted by Security Managers.
- **Maintenance**: It makes code harder to read and breaks compile-time safety.

Use it when you need a generic, dynamic solution; avoid it for standard business logic.
