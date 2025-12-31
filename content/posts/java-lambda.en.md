+++
date = '2023-04-02T14:33:49+08:00'
draft = false
title = 'Introduction to Functional Programming with Java Lambda'
tags = ["Java"]
+++

### Overview

#### Background

The theoretical foundation of functional programming is the λ-calculus (Lambda Calculus) proposed by Alonzo Church in the 1930s. λ-calculus is a formal system for studying function definition, function application, and recursion. It laid the foundation for the development of computation theory and computer science. With the birth of a new generation of functional programming languages such as Haskell (1990) and Erlang (1986), functional programming began to play a role in practical applications.

#### The Value of Functional Programming

As hardware becomes cheaper, the scale and complexity of programs grow linearly. All of this makes programming work increasingly difficult. We seek ways to make code more consistent and understandable. We urgently need a programming method that is **syntax-elegant, concise and robust, high-concurrency, and easy to test and debug**. This is exactly where **Functional Programming (FP)** comes in.

Functional languages have produced elegant syntax that is also applicable to non-functional languages. For example, today Python and Java 8 are absorbing FP ideas and integrating them. You can think of it like this:

> OO (Object-Oriented) is about abstracting data; FP (Functional Programming) is about abstracting behavior.

### Old vs. New Comparison

Let's demonstrate using traditional forms versus Java 8's method references and Lambda expressions. Example code:

```java
interface Strategy {
    String approach(String msg);
}

class Soft implements Strategy {
    public String approach(String msg) {
        return msg.toLowerCase() + "?";
    }
}

class Unrelated {
    static String twice(String msg) {
        return msg + " " + msg;
    }
}

public class Strategize {

    Strategy strategy;
    String msg;
    Strategize(String msg) {
        strategy = new Soft(); // [1] Build default Soft
        this.msg = msg;
    }

    void communicate() {
        System.out.println(strategy.approach(msg));
    }

    void changeStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    public static void main(String[] args) {
        Strategy[] strategies = {
                new Strategy() { // [2] Anonymous inner class before Java 8
                    public String approach(String msg) {
                        return msg.toUpperCase() + "!";
                    }
                },
                msg -> msg.substring(0, 5), // [3] Instantiate interface based on Lambda expression
                Unrelated::twice // [4] Instantiate interface based on method reference
        };
        Strategize s = new Strategize("Hello there");
        s.communicate();
        for(Strategy newStrategy : strategies) {
            s.changeStrategy(newStrategy); // [5] Use default Soft strategy
            s.communicate(); // [6] Each call to communicate() produces different behavior
        }
    }
}
```

Output:

```sh
hello there?
HELLO THERE!
Hello
Hello there Hello there
```

### Lambda Expressions

A Lambda expression is a function definition written with the **smallest possible** syntax: (Principles)

1. Lambda expressions produce functions, not classes.
2. Lambda syntax is kept to a minimum specifically to make Lambdas easy to write and use.

Lambda Usage:

```java
interface Description {
    String brief();
}

interface Body {
    String detailed(String head);
}

interface Multi {
    String twoArg(String head, Double d);
}

public class LambdaExpressions {

    static Body bod = h -> h + " No Parens!"; // [1] When there's one parameter, parentheses () are not required, but this is a special case
    static Body bod2 = (h) -> h + " More details"; // [2] Normal usage
    static Description desc = () -> "Short info"; // [3] Usage with no parameters
    static Multi mult = (h, n) -> h + n; // [4] Usage with multiple parameters

    static Description moreLines = () -> { 
        // [5] Use `{}` + `return` keyword for multiple lines of code
        // (In a single-line Lambda expression, `return` is implicit and manual use is illegal)
        System.out.println("moreLines()");
        return "from moreLines()";
    };

    public static void main(String[] args) {
        System.out.println(bod.detailed("Oh!"));
        System.out.println(bod2.detailed("Hi!"));
        System.out.println(desc.brief());
        System.out.println(mult.twoArg("Pi! ", 3.14159));
        System.out.println(moreLines.brief());
    }
}
```

Output:

```sh
Oh! No Parens!
Hi! More details
Short info
Pi! 3.14159
moreLines()
from moreLines()
```

Summary: Lambda expressions generally produce more readable code than anonymous inner classes, so we will use them whenever possible.

### Method References

A method reference consists of a class name or object name, followed by `::` and then the method name.

Example Usage:

```java
interface Callable { // [1] Interface with a single method (important)
    void call(String s);
}

class Describe {
    void show(String msg) { // [2] Implementation of call() conforming to Callable interface
        System.out.println(msg);
    }
}

public class MethodReferences {
    static void hello(String name) { // [3] Also conforms to call() implementation
        System.out.println("Hello, " + name);
    }

    static class Description {
        String about;

        Description(String desc) {
            about = desc;
        }

        void help(String msg) { // [4] Non-static method of a static class
            System.out.println(about + " " + msg);
        }
    }

    static class Helper {
        static void assist(String msg) { // [5] Static method of a static class, conforms to call()
            System.out.println(msg);
        }
    }

    public static void main(String[] args) {
        Describe d = new Describe();
        Callable c = d::show; // [6] Create Callable interface implementation via method reference
        c.call("call()"); // [7] Call show() method through instance call() method

        c = MethodReferences::hello; // [8] Method reference to a static method
        c.call("Bob");

        c = new Description("valuable")::help; // [9] Method reference to an instance method of an object
        c.call("information");

        c = Helper::assist; // [10] Method reference to a static method
        c.call("Help!");
    }
}
```

Output:

```sh
call()
Hello, Bob
valuable information
Help!
```

#### Runnable Interface

Changing Runnable interface writing using Lambda and method references:

```java
// Combining method references with Runnable interface

class Go {
    static void go() {
        System.out.println("Go::go()");
    }
}

public class RunnableMethodReference {

    public static void main(String[] args) {

        new Thread(new Runnable() {
            public void run() {
                System.out.println("Anonymous");
            }
        }).start();

        new Thread(
                () -> System.out.println("lambda")
        ).start();

        new Thread(Go::go).start();		// Create Runnable implementation reference via method reference
    }
}
```

Output:

```sh
Anonymous
lambda
Go::go()
```

#### Unbound Method References

When using unbound references, an object must be provided first:

```java
// Unbound method references refer to ordinary methods without an associated object
class X {
    String f() {
        return "X::f()";
    }
}

interface MakeString {
    String make();
}

interface TransformX {
    String transform(X x);
}

public class UnboundMethodReference {

    public static void main(String[] args) {
        // MakeString sp = X::f;       // [1] You cannot call f() without an X object parameter because it's an instance method of X
        TransformX sp = X::f;       // [2] You can call f() if the first parameter is an X object. Using an unbound reference, the functional method's signature no longer matches the method reference's exactly
        X x = new X();
        System.out.println(sp.transform(x));      // [3] Pass x object, calls x.f()
        System.out.println(x.f());      // Equivalent effect
    }
}
```

Output:

```sh
X::f()
X::f()
```

We can prove through more examples that a connection is established between unbound method references and interfaces:

```java
package com.github.xiao2shiqi.lambda;

// Combined use of unbound methods and multiple parameters
class This {
    void two(int i, double d) {}
    void three(int i, double d, String s) {}
    void four(int i, double d, String s, char c) {}
}
interface TwoArgs {
    void call2(This athis, int i, double d);
}
interface ThreeArgs {
    void call3(This athis, int i, double d, String s);
}
interface FourArgs {
    void call4(
            This athis, int i, double d, String s, char c);
}

public class MultiUnbound {

    public static void main(String[] args) {
        TwoArgs twoargs = This::two;
        ThreeArgs threeargs = This::three;
        FourArgs fourargs = This::four;
        This athis = new This();
        twoargs.call2(athis, 11, 3.14);
        threeargs.call3(athis, 11, 3.14, "Three");
        fourargs.call4(athis, 11, 3.14, "Four", 'Z');
    }
}
```

#### Constructor References

You can capture references to constructors and then build objects through these references.

```java
class Dog {
    String name;
    int age = -1; // For "unknown"
    Dog() { name = "stray"; }
    Dog(String nm) { name = nm; }
    Dog(String nm, int yrs) {
        name = nm;
        age = yrs;
    }
}

interface MakeNoArgs {
    Dog make();
}

interface Make1Arg {
    Dog make(String nm);
}

interface Make2Args {
    Dog make(String nm, int age);
}

public class CtorReference {
    public static void main(String[] args) {
        // Assign to different interfaces using the ::new keyword, then build different instances via make()
        MakeNoArgs mna = Dog::new; // [1] Give constructor reference to MakeNoArgs interface
        Make1Arg m1a = Dog::new; // [2] ...
        Make2Args m2a = Dog::new; // [3] ...
        Dog dn = mna.make();
        Dog d1 = m1a.make("Comet");
        Dog d2 = m2a.make("Ralph", 4);
    }
}
```

#### Summary

* Method references can largely be understood as creating an instance of a functional interface.
* Method references are actually a form of syntactic sugar that simplifies Lambda expressions, providing a more concise way to create a functional interface implementation.
* When using a method reference in code, you are actually creating an anonymous implementation class that references the method implementation and overrides the interface's abstract method.
* Method references are mostly used to create implementations of functional interfaces.

### Functional Interfaces

* Lambdas include type inference.
* Java 8 introduced the `java.util.function` package to solve type inference issues.

Creating Interfaces through function expressions:

```java
// Use @FunctionalInterface annotation to enforce this "functional method" pattern
@FunctionalInterface
interface Functional {
    String goodbye(String arg);
}

interface FunctionalNoAnn {
    String goodbye(String arg);
}

public class FunctionalAnnotation {
    // goodbye
    public String goodbye(String arg) {
        return "Goodbye, " + arg + "!";
    }

    public static void main(String[] args) {
        FunctionalAnnotation fa = new FunctionalAnnotation();

        // FunctionalAnnotation does not implement the Functional interface, so it cannot be directly assigned
//        Functional fac = fa;      // Incompatible?

        // But functions can be assigned to interfaces via Lambda (types must match)
        Functional f = fa::goodbye;
        FunctionalNoAnn fna = fa::goodbye;
        Functional fl = a -> "Goodbye, " + a;
        FunctionalNoAnn fnal = a -> "Goodbye, " + a;
    }
}
```

Above is an example of creating your own functional interface.

However, the `java.util.function` package is designed to provide a complete set of predefined interfaces, so we generally don't need to define our own.

Basic principles for using functional interfaces in `java.util.function` are as follows:

1. If it only handles objects rather than basic types, the names are `Function`, `Consumer`, `Predicate`, etc. Parameters are added via generics.
2. If the accepted parameters are basic types, they are indicated by the first part of the name, e.g., `LongConsumer`, `DoubleFunction`, `IntPredicate`, etc.
3. If the return value is a basic type, it's indicated by `To`, e.g., `ToLongFunction` and `IntToLongFunction`.
4. If the return value type is the same as the parameter type, it is an `Operator`.
5. If it accepts two parameters and returns a boolean value, it is a `Predicate`.
6. If it accepts two parameters of different types, there is a `Bi` in the name.

#### Basic Types

Below are examples of all different `Function` variants based on Lambda expressions:

```java
class Foo {}

class Bar {
    Foo f;
    Bar(Foo f) { this.f = f; }
}

class IBaz {
    int i;
    IBaz(int i) { this.i = i; }
}

class LBaz {
    long l;
    LBaz(long l) { this.l = l; }
}

class DBaz {
    double d;
    DBaz(double d) { this.d = d; }
}

public class FunctionVariants {
    // Function expressions to get objects based on different parameters
    static Function<Foo, Bar> f1 = f -> new Bar(f);
    static IntFunction<IBaz> f2 = i -> new IBaz(i);
    static LongFunction<LBaz> f3 = l -> new LBaz(l);
    static DoubleFunction<DBaz> f4 = d -> new DBaz(d);
    // Function expressions to get basic data type return values based on object type parameters
    static ToIntFunction<IBaz> f5 = ib -> ib.i;
    static ToLongFunction<LBaz> f6 = lb -> lb.l;
    static ToDoubleFunction<DBaz> f7 = db -> db.d;
    static IntToLongFunction f8 = i -> i;
    static IntToDoubleFunction f9 = i -> i;
    static LongToIntFunction f10 = l -> (int)l;
    static LongToDoubleFunction f11 = l -> l;
    static DoubleToIntFunction f12 = d -> (int)d;
    static DoubleToLongFunction f13 = d -> (long)d;

    public static void main(String[] args) {
        // apply usage examples
        Bar b = f1.apply(new Foo());
        IBaz ib = f2.apply(11);
        LBaz lb = f3.apply(11);
        DBaz db = f4.apply(11);

        // applyAs* usage examples
        int i = f5.applyAsInt(ib);
        long l = f6.applyAsLong(lb);
        double d = f7.applyAsDouble(db);

        // Conversion between basic types
        long applyAsLong = f8.applyAsLong(12);
        double applyAsDouble = f9.applyAsDouble(12);
        int applyAsInt = f10.applyAsInt(12);
        double applyAsDouble1 = f11.applyAsDouble(12);
        int applyAsInt1 = f12.applyAsInt(13.0);
        long applyAsLong1 = f13.applyAsLong(13.0);
    }
}
```

Below is a table organizing functional interfaces related to basic types:

| Functional Interface | Features | Purpose | Method Name |
| -------------------- | ---------------------------------------- | ---------------------------------------------- | -------------------------------- |
| Function<T, R> | Accepts one parameter, returns one result | Converts input parameter to output result, e.g., data conversion or mapping | R apply(T t) |
| IntFunction<R> | Accepts one int parameter, returns one result | Converts int value to output result | R apply(int value) |
| LongFunction<R> | Accepts one long parameter, returns one result | Converts long value to output result | R apply(long value) |
| DoubleFunction<R> | Accepts one double parameter, returns one result | Converts double value to output result | R apply(double value) |
| ToIntFunction<T> | Accepts one parameter, returns one int result | Converts input parameter to int output result | int applyAsInt(T value) |
| ToLongFunction<T> | Accepts one parameter, returns one long result | Converts input parameter to long output result | long applyAsLong(T value) |
| ToDoubleFunction<T> | Accepts one parameter, returns one double result | Converts input parameter to double output result | double applyAsDouble(T value) |
| IntToLongFunction | Accepts one int parameter, returns one long result | Converts int value to long output result | long applyAsLong(int value) |
| IntToDoubleFunction | Accepts one int parameter, returns one double result | Converts int value to double output result | double applyAsDouble(int value) |
| LongToIntFunction | Accepts one long parameter, returns one int result | Converts long value to int output result | int applyAsInt(long value) |
| LongToDoubleFunction | Accepts one long parameter, returns one double result | Converts long value to double output result | double applyAsDouble(long value) |
| DoubleToIntFunction | Accepts one double parameter, returns one int result | Converts double value to int output result | int applyAsInt(double value) |
| DoubleToLongFunction | Accepts one double parameter, returns one long result | Converts double value to long output result | long applyAsLong(double value) |

#### Non-Basic Types

When using functional interfaces, the name doesn't matter—as long as the parameter types and return type are the same. Java will map your method to the interface method. Example:

```java
import java.util.function.BiConsumer;

class In1 {}
class In2 {}

public class MethodConversion {

    static void accept(In1 in1, In2 in2) {
        System.out.println("accept()");
    }

    static void someOtherName(In1 in1, In2 in2) {
        System.out.println("someOtherName()");
    }

    public static void main(String[] args) {
        BiConsumer<In1, In2> bic;

        bic = MethodConversion::accept;
        bic.accept(new In1(), new In2());

        // When using functional interfaces, the name doesn't matter—as long as the parameter types and return type are the same. Java will map your method to the interface method.
        bic = MethodConversion::someOtherName;
        bic.accept(new In1(), new In2());
    }
}
```

Output:

```sh
accept()
someOtherName()
```

Applying method references to class-based functional interfaces (i.e., those that don't include basic types):

```java
import java.util.Comparator;
import java.util.function.*;

class AA {}
class BB {}
class CC {}

public class ClassFunctionals {

    static AA f1() { return new AA(); }
    static int f2(AA aa1, AA aa2) { return 1; }
    static void f3 (AA aa) {}
    static void f4 (AA aa, BB bb) {}
    static CC f5 (AA aa) { return new CC(); }
    static CC f6 (AA aa, BB bb) { return new CC(); }
    static boolean f7 (AA aa) { return true; }
    static boolean f8 (AA aa, BB bb) { return true; }
    static AA f9 (AA aa) { return new AA(); }
    static AA f10 (AA aa, AA bb) { return new AA(); }

    public static void main(String[] args) {
        // No parameters, returns a result
        Supplier<AA> s = ClassFunctionals::f1;
        s.get();
        // Compares two objects, used for sorting and comparison operations
        Comparator<AA> c = ClassFunctionals::f2;
        c.compare(new AA(), new AA());
        // Performs an operation, usually a side-effect operation, with no result returned
        Consumer<AA> cons = ClassFunctionals::f3;
        cons.accept(new AA());
        // Performs an operation, usually a side-effect operation, with no result returned, accepts two parameters
        BiConsumer<AA, BB> bicons = ClassFunctionals::f4;
        bicons.accept(new AA(), new BB());
        // Converts input parameter to output result, e.g., data conversion or mapping
        Function<AA, CC> f = ClassFunctionals::f5;
        CC cc = f.apply(new AA());
        // Converts two input parameters to an output result, e.g., data conversion or mapping
        BiFunction<AA, BB, CC> bif = ClassFunctionals::f6;
        cc = bif.apply(new AA(), new BB());
        // Accepts one parameter, returns a boolean: tests if parameter satisfy specific conditions
        Predicate<AA> p = ClassFunctionals::f7;
        boolean result = p.test(new AA());
        // Accepts two parameters, returns a boolean: tests if two parameters satisfy specific conditions
        BiPredicate<AA, BB> bip = ClassFunctionals::f8;
        result = bip.test(new AA(), new BB());
        // Accepts one parameter, returns a result of same type: performs a single operation on input and returns result of same type, a special case of Function
        UnaryOperator<AA> uo = ClassFunctionals::f9;
        AA aa = uo.apply(new AA());
        // Accepts two parameters of same type, returns a result of same type: combines two values of same type into new value, a special case of BiFunction
        BinaryOperator<AA> bo = ClassFunctionals::f10;
        aa = bo.apply(new AA(), new AA());
    }
}
```

Below is a table for non-basic type functional interfaces:

| Functional Interface | Features | Purpose | Method Name |
| ------------------- | ---------------------------------------------- | ------------------------------------------------------------ | ----------------------- |
| Supplier<T> | No parameters, returns a result | Getting a value or instance, factory pattern, lazy computation | T get() |
| Comparator<T> | Accepts two parameters, returns an int value | Compares two objects, used for sorting and comparison operations | int compare(T o1, T o2) |
| Consumer<T> | Accepts one parameter, no return value| Performs an operation, usually a side-effect, no result needed | void accept(T t) |
| BiConsumer<T, U> | Accepts two parameters, no return value | Performs an operation, usually a side-effect, accepts two parameters | void accept(T t, U u) |
| Function<T, R> | Accepts one parameter, returns a result | Converts input to output, e.g., data conversion or mapping | R apply(T t) |
| BiFunction<T, U, R> | Accepts two parameters, returns a result | Converts two inputs to one output, e.g., data conversion or mapping | R apply(T t, U u) |
| Predicate<T> | Accepts one parameter, returns boolean | Tests if parameter meets specific condition | boolean test(T t) |
| BiPredicate<T, U> | Accepts two parameters, returns boolean | Tests if two parameters meet specific condition | boolean test(T t, U u) |
| UnaryOperator<T> | Accepts one parameter, returns same type result| Performs operation on input and returns same type result, special Function | T apply(T t) |
| BinaryOperator<T> | Accepts two same type parameters, returns same type result | Combines two same type values into new value, special BiFunction | T apply(T t1, T t2) |

#### Multi-parameter Functional Interfaces

The interfaces in `java.util.function` are limited. What if you need a 3-parameter function interface? Just create it yourself, like this:

```java
// Create a functional interface to handle 3 parameters
@FunctionalInterface
public interface TriFunction<T, U, V, R> {
    
    R apply(T t, U u, V v);
}
```

Verification:

```java
public class TriFunctionTest {
    static int f(int i, long l, double d) { return 99; }

    public static void main(String[] args) {
        // Method reference
        TriFunction<Integer, Long, Double, Integer> tf1 = TriFunctionTest::f;
        // Lambda expression
        TriFunction<Integer, Long, Double, Integer> tf2 = (i, l, d) -> 12;
    }
}
```

#### Higher-Order Functions

Higher-order Functions are easy to understand and very common in functional programming. They have the following characteristics:

1. Accept one or more functions as parameters.
2. Return a function as a result.

First, let's see how a function returns a function:

```java
import java.util.function.Function;

interface FuncSS extends Function<String, String> {}        // [1] Use inheritance to easily create your own functional interface

public class ProduceFunction {
    // produce() is a higher-order function: a consumer of functions, a function that produces functions
    static FuncSS produce() {
        return s -> s.toLowerCase();    // [2] Using Lambda expressions, you can easily create and return a function within a method
    }

    public static void main(String[] args) {
        FuncSS funcSS = produce();
        System.out.println(funcSS.apply("YELLING"));
    }
}
```

Then, let's see how a function accepts another function as a parameter:

```java
class One {}
class Two {}

public class ConsumeFunction {
    static Two consume(Function<One, Two> onetwo) {
        return onetwo.apply(new One());
    }

    public static void main(String[] args) {
        Two two = consume(one -> new Two());
    }
}
```

In short, higher-order functions make code more concise, flexible, and reusable, commonly found in `Stream` programming.

### Closures

In Java, closures are usually associated with lambda expressions and anonymous inner classes. Simply put, a closure allows accessing and manipulating variables from its outer scope within a function. A closure in Java is actually a special object that encapsulates a function and its associated environment. This means a closure is not just a function; it also carries an execution context, including variables from the outer scope. This allows the closure to maintain the values of these variables in different execution contexts when accessing them.

Let's understand closures in Java through an example:

```java
public class ClosureExample {
    public static void main(String[] args) {
        int a = 10;
        int b = 20;

        // This is a closure because it captures variables a and b from the outer scope
        IntBinaryOperator closure = (x, y) -> x * a + y * b;

        int result = closure.applyAsInt(3, 4);
        System.out.println("Result: " + result); // Output "Result: 110"
    }
}
```

Note that in Java, external variables captured by a closure must be `final` or effectively `final` (i.e., remain unchanged during use). This is to prevent unpredictable behavior and data inconsistency in multi-threaded environments.

### Function Composition

Function Composition means "combining multiple functions into a new function." it's typically a fundamental part of functional programming.

First, see the `Function` composition example code:

```java
import java.util.function.Function;

public class FunctionComposition {
    static Function<String, String> f1 = s -> {
        System.out.println(s);
        return s.replace('A', '_');
    },
    f2 = s -> s.substring(3),
    f3 = s -> s.toLowerCase(),
    // Key point: combine multiple functions using function composition
    // compose executes the parameter function first, then the caller
    // andThen executes the caller first, then the parameter function
    f4 = f1.compose(f2).andThen(f3);        

    public static void main(String[] args) {
        String s = f4.apply("GO AFTER ALL AMBULANCES");
        System.out.println(s);
    }
}
```

The example uses `compose()` and `andThen()` from `Function`. Their differences are:

* `compose` executes the parameter function first, followed by the caller.
* `andThen` executes the caller first, followed by the parameter function.

Output:

```sh
AFTER ALL AMBULANCES
_fter _ll _mbul_nces
```

Next, see a logic operation demonstration code for `Predicate`:

```java
public class PredicateComposition {
    static Predicate<String>
            p1 = s -> s.contains("bar"),
            p2 = s -> s.length() < 5,
            p3 = s -> s.contains("foo"),
            p4 = p1.negate().and(p2).or(p3);    // Combine multiple predicates using predicate composition. negate is NOT, and is AND, or is OR

    public static void main(String[] args) {
        Stream.of("bar", "foobar", "foobaz", "fongopuckey")
                .filter(p4)
                .forEach(System.out::println);
    }
}
```

`p4` generates a complex predicate through function composition, eventually applied in `filter()`:

* `negate()`: Inverts the value, content does not contain "bar".
* `and(p2)`: Length is less than 5.
* `or(p3)`: Or contains "foo".

Output:

```sh
foobar
foobaz
```

Commonly used methods supporting function composition in `java.util.function` include:

| Functional Interface | Method Name | Description |
| -------------- | ------- | ------------------------------------------------------------ |
| Function<T, R> | andThen | For combining two functions from left to right, i.e., `h(x) = g(f(x))` |
| Function<T, R> | compose | For combining two functions from right to left, i.e., `h(x) = f(g(x))` |
| Consumer<T> | andThen | For combining two consumers from left to right, executing two consumer operations in sequence |
| Predicate<T> | and | For combining two predicate functions, returns a new predicate satisfying both conditions |
| Predicate<T> | or | For combining two predicate functions, returns a new predicate satisfying either condition |
| Predicate<T> | negate | For inverting a predicate function, returns a new predicate satisfying the opposite condition |
| UnaryOperator | andThen | For combining two unary operators from left to right, i.e., `h(x) = g(f(x))` |
| UnaryOperator | compose | For combining two unary operators from right to left, i.e., `h(x) = f(g(x))` |
| BinaryOperator | andThen | For combining two binary operators from left to right, i.e., `h(x, y) = g(f(x, y))` |

### Currying

Currying is a technique in functional programming that transforms a function accepting multiple parameters into a series of single-parameter functions.

Let's understand currying through a simple Java example:

```java
public class CurryingAndPartials {
    static String uncurried(String a, String b) {
        return a + b;
    }

    public static void main(String[] args) {
        // Curried function, a function that accepts multiple parameters
        Function<String, Function<String, String>> sum = a -> b -> a + b;
        System.out.println(uncurried("Hi ", "Ho"));

        // Passing parameters one by one via chain calls
        Function<String, String> hi = sum.apply("Hi ");
        System.out.println(hi.apply("Ho"));

        Function<String, String> sumHi = sum.apply("Hup ");
        System.out.println(sumHi.apply("Ho"));
        System.out.println(sumHi.apply("Hey"));
    }
}
```

Output:

```sh
Hi Ho
Hi Ho
Hup Ho
Hup Hey
```

Next, let's add levels to curry a three-parameter function:

```java
import java.util.function.Function;

public class Curry3Args {
    public static void main(String[] args) {
        // Curried function
        Function<String,
                Function<String,
                        Function<String, String>>> sum = a -> b -> c -> a + b + c;

        // Passing parameters one by one
        Function<String, Function<String, String>> hi = sum.apply("Hi ");
        Function<String, String> ho = hi.apply("Ho ");
        System.out.println(ho.apply("Hup"));
    }
}
```

Output:

```java
Hi Ho Hup
```

When dealing with basic types, make sure to choose the appropriate functional interface:

```java
import java.util.function.IntFunction;
import java.util.function.IntUnaryOperator;

public class CurriedIntAdd {
    public static void main(String[] args) {
        IntFunction<IntUnaryOperator> curriedIntAdd = a -> b -> a + b;
        IntUnaryOperator add4 = curriedIntAdd.apply(4);
        System.out.println(add4.applyAsInt(5));
    }
}
```

Output:

```sh
9
```

### Summary

Lambda expressions and method references have not converted Java into a functional language, but provided support for functional programming (Java's historical burden is too heavy). These features satisfy a large portion of Java programmers who envied more functional languages like Clojure and Scala, preventing them from defecting to those languages (or at least preparing them before they do). In short, Lambdas and method references are huge improvements in Java 8.
