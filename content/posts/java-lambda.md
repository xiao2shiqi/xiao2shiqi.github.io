+++
date = '2023-04-02T14:33:49+08:00'
draft = false
title = 'Java Lambda 函数式编程方法介绍'
+++

### 概述

#### 背景

函数式编程的理论基础是阿隆佐·丘奇（Alonzo Church）于 1930 年代提出的 λ 演算（Lambda Calculus）。λ 演算是一种形式系统，用于研究函数定义、函数应用和递归。它为计算理论和计算机科学的发展奠定了基础。随着 Haskell（1990年）和 Erlang（1986年）等新一代函数式编程语言的诞生，函数式编程开始在实际应用中发挥作用。



#### 函数式的价值

随着硬件越来越便宜，程序的规模和复杂性都在呈线性的增长。这一切都让编程工作变得困难重重。我们想方设法使代码更加一致和易懂。我们急需一种 **语法优雅，简洁健壮，高并发，易于测试和调试** 的编程方式，这一切恰恰就是 **函数式编程（FP）** 的意义所在。

函数式语言已经产生了优雅的语法，这些语法对于非函数式语言也适用。 例如：如今 Python，Java 8 都在吸收 FP 的思想，并且将其融入其中，你也可以这样想：

> OO（object oriented，面向对象）是抽象数据，FP（functional programming，函数 式编程）是抽象行为。



### 新旧对比

用传统形式和 Java 8 的方法引用、Lambda 表达式分别演示。代码示例：

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
        strategy = new Soft(); // [1] 构建默认的 Soft
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
                new Strategy() { // [2] Java 8 以前的匿名内部类
                    public String approach(String msg) {
                        return msg.toUpperCase() + "!";
                    }
                },
                msg -> msg.substring(0, 5), // [3] 基于 Ldmbda 表达式，实例化 interface
                Unrelated::twice // [4] 基于 方法引用，实例化 interface
        };
        Strategize s = new Strategize("Hello there");
        s.communicate();
        for(Strategy newStrategy : strategies) {
            s.changeStrategy(newStrategy); // [5] 使用默认的 Soft 策略
            s.communicate(); // [6] 每次调用 communicate() 都会产生不同的行为
        }
    }
}
```

输出结果：

```sh
hello there?
HELLO THERE!
Hello
Hello there Hello there
```



### Lambda 表达式

Lambda 表达式是使用**最小可能**语法编写的函数定义：（原则）

1. Lambda 表达式产生函数，而不是类
2. Lambda 语法尽可能少，这正是为了使 Lambda 易于编写和使用

Lambda 用法：

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

    static Body bod = h -> h + " No Parens!"; // [1] 一个参数时，可以不需要扩展 ()， 但这是一个特例
    static Body bod2 = (h) -> h + " More details"; // [2] 正常情况下的使用方式
    static Description desc = () -> "Short info"; // [3] 没有参数的情况下的使用方式
    static Multi mult = (h, n) -> h + n; // [4] 多参数情况下的使用方式

    static Description moreLines = () -> { 
        // [5] 多行代码情况下使用 `{}` + `return` 关键字
        // （在单行的 Lambda 表达式中 `return` 是非法的）
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

输出结果：

```sh
Oh! No Parens!
Hi! More details
Short info
Pi! 3.14159
moreLines()
from moreLines()
```

总结：Lambda 表达式通常比匿名内部类产生更易读的代码，因此我们将尽可能使用它们。



### 方法引用

方法引用由类名或者对象名，后面跟着 `::`  然后跟方法名称，

使用示例：

```java
interface Callable { // [1] 单一方法的接口（重要）
    void call(String s);
}

class Describe {
    void show(String msg) { // [2] 符合 Callable 接口的 call() 方法实现
        System.out.println(msg);
    }
}

public class MethodReferences {
    static void hello(String name) { // [3] 也符合 call() 方法实现
        System.out.println("Hello, " + name);
    }

    static class Description {
        String about;

        Description(String desc) {
            about = desc;
        }

        void help(String msg) { // [4] 静态类的非静态方法
            System.out.println(about + " " + msg);
        }
    }

    static class Helper {
        static void assist(String msg) { // [5] 静态类的静态方法，符合 call() 方法
            System.out.println(msg);
        }
    }

    public static void main(String[] args) {
        Describe d = new Describe();
        Callable c = d::show; // [6] 通过方法引用创建 Callable 的接口实现
        c.call("call()"); // [7] 通过该实例 call() 方法调用 show() 方法

        c = MethodReferences::hello; // [8] 静态方法的方法引用
        c.call("Bob");

        c = new Description("valuable")::help; // [9] 实例化对象的方法引用
        c.call("information");

        c = Helper::assist; // [10] 静态方法的方法引用
        c.call("Help!");
    }
}
```

输出结果：

```sh
call()
Hello, Bob
valuable information
Help!
```



#### Runnable 接口

使用 Lambda 和方法引用改变 Runnable 接口的写法：

```java
// 方法引用与 Runnable 接口的结合使用

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

        new Thread(Go::go).start();		// 通过 方法引用创建 Runnable 实现的引用
    }
}
```

输出结果：

```sh
Anonymous
lambda
Go::go()
```



#### 未绑定的方法引用

使用未绑定的引用时，需要先提供对象：

```java
// 未绑定的方法引用是指没有关联对象的普通方法
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
        // MakeString sp = X::f;       // [1] 你不能在没有 X 对象参数的前提下调用 f()，因为它是 X 的方法
        TransformX sp = X::f;       // [2] 你可以首个参数是 X 对象参数的前提下调用 f()，使用未绑定的引用，函数式的方法不再与方法引用的签名完全相同
        X x = new X();
        System.out.println(sp.transform(x));      // [3] 传入 x 对象，调用 x.f() 方法
        System.out.println(x.f());      // 同等效果
    }
}
```

输出结果：

```sh
X::f()
X::f()
```

我们通过更多示例来证明，通过未绑的方法引用和 interface 之间建立关联：

```java
package com.github.xiao2shiqi.lambda;

// 未绑定的方法与多参数的结合运用
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

#### 构造函数引用

可以捕获构造函数的引用，然后通过引用构建对象

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
        // 通过 ::new 关键字赋值给不同的接口，然后通过 make() 构建不同的实例
        MakeNoArgs mna = Dog::new; // [1] 将构造函数的引用交给 MakeNoArgs 接口
        Make1Arg m1a = Dog::new; // [2] …………
        Make2Args m2a = Dog::new; // [3] …………
        Dog dn = mna.make();
        Dog d1 = m1a.make("Comet");
        Dog d2 = m2a.make("Ralph", 4);
    }
}
```



#### 总结

* 方法引用在很大程度上可以理解为创建一个函数式接口的实例
* 方法引用实际上是一种简化 Lambda 表达式的语法糖，它提供了一种更简洁的方式来创建一个函数式接口的实现
* 在代码中使用方法引用时，实际上是在创建一个匿名实现类，引用方法实现并且覆盖了接口的抽象方法
* 方法引用大多用于创建函数式接口的实现



### 函数式接口

* Lambda 包含类型推导
* Java 8 引入 `java.util.function` 包，解决类型推导的问题

通过函数表达式创建 Interface：

```java
// 使用 @FunctionalInterface 注解强制执行此 “函数式方法” 模式
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

        // FunctionalAnnotation 没有实现 Functional 接口，所以不能直接赋值
//        Functional fac = fa;      // Incompatible ?

        // 但可以通过 Lambda 将函数赋值给接口 （类型需要匹配）
        Functional f = fa::goodbye;
        FunctionalNoAnn fna = fa::goodbye;
        Functional fl = a -> "Goodbye, " + a;
        FunctionalNoAnn fnal = a -> "Goodbye, " + a;
    }
}
```

以上是自己创建 函数式接口的示例。

但在 `java.util.function` 包旨在创建一组完整的预定义接口，使得我们一般情况下不需再定义自己的接口。

在 `java.util.function` 的函数式接口的基本使用基本准测，如下

1. 只处理对象而非基本类型，名称则为 Function，Consumer，Predicate 等，参数通过泛型添加
2. 如果接收的参数是基本类型，则由名称的第一部分表示，如 LongConsumer， DoubleFunction，IntPredicate 等
3. 如果返回值为基本类型，则用 To 表示，如 ToLongFunction  和 IntToLongFunction
4. 如果返回值类型与参数类型一致，则是一个运算符
5. 如果接收两个参数且返回值为布尔值，则是一个谓词（Predicate）
6. 如果接收的两个参数类型不同，则名称中有一个 Bi



#### 基本类型

下面枚举了基于 Lambda 表达式的所有不同 Function 变体的示例：

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
    // 根据不同参数获得对象的函数表达式
    static Function<Foo, Bar> f1 = f -> new Bar(f);
    static IntFunction<IBaz> f2 = i -> new IBaz(i);
    static LongFunction<LBaz> f3 = l -> new LBaz(l);
    static DoubleFunction<DBaz> f4 = d -> new DBaz(d);
    // 根据对象类型参数，获得基本数据类型返回值的函数表达式
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

        // 基本类型的相互转换
        long applyAsLong = f8.applyAsLong(12);
        double applyAsDouble = f9.applyAsDouble(12);
        int applyAsInt = f10.applyAsInt(12);
        double applyAsDouble1 = f11.applyAsDouble(12);
        int applyAsInt1 = f12.applyAsInt(13.0);
        long applyAsLong1 = f13.applyAsLong(13.0);
    }
}
```

以下是用表格整理基本类型相关的函数式接口：

| 函数式接口           | 特征                                     | 用途                                           | 方法名                           |
| -------------------- | ---------------------------------------- | ---------------------------------------------- | -------------------------------- |
| Function<T, R>       | 接受一个参数，返回一个结果               | 将输入参数转换成输出结果，如数据转换或映射操作 | R apply(T t)                     |
| IntFunction<R>       | 接受一个 int 参数，返回一个结果          | 将 int 值转换成输出结果                        | R apply(int value)               |
| LongFunction<R>      | 接受一个 long 参数，返回一个结果         | 将 long 值转换成输出结果                       | R apply(long value)              |
| DoubleFunction<R>    | 接受一个 double 参数，返回一个结果       | 将 double 值转换成输出结果                     | R apply(double value)            |
| ToIntFunction<T>     | 接受一个参数，返回一个 int 结果          | 将输入参数转换成 int 输出结果                  | int applyAsInt(T value)          |
| ToLongFunction<T>    | 接受一个参数，返回一个 long 结果         | 将输入参数转换成 long 输出结果                 | long applyAsLong(T value)        |
| ToDoubleFunction<T>  | 接受一个参数，返回一个 double 结果       | 将输入参数转换成 double 输出结果               | double applyAsDouble(T value)    |
| IntToLongFunction    | 接受一个 int 参数，返回一个 long 结果    | 将 int 值转换成 long 输出结果                  | long applyAsLong(int value)      |
| IntToDoubleFunction  | 接受一个 int 参数，返回一个 double 结果  | 将 int 值转换成 double 输出结果                | double applyAsDouble(int value)  |
| LongToIntFunction    | 接受一个 long 参数，返回一个 int 结果    | 将 long 值转换成 int 输出结果                  | int applyAsInt(long value)       |
| LongToDoubleFunction | 接受一个 long 参数，返回一个 double 结果 | 将 long 值转换成 double 输出结果               | double applyAsDouble(long value) |
| DoubleToIntFunction  | 接受一个 double 参数，返回一个 int 结果  | 将 double 值转换成 int 输出结果                | int applyAsInt(double value)     |
| DoubleToLongFunction | 接受一个 double 参数，返回一个 long 结果 | 将 double 值转换成 long 输出结果               | long applyAsLong(double value)   |



#### 非基本类型

在使用函数接口时，名称无关紧要——只要参数类型和返回类型相同。Java 会将你的方法映射到接口方法。示例：

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

        // 在使用函数接口时，名称无关紧要——只要参数类型和返回类型相同。Java 会将你的方法映射到接口方法。
        bic = MethodConversion::someOtherName;
        bic.accept(new In1(), new In2());
    }
}
```

输出结果：

```sh
accept()
someOtherName()
```

将方法引用应用于基于类的函数式接口（即那些不包含基本类型的函数式接口）

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
        // 无参数，返回一个结果
        Supplier<AA> s = ClassFunctionals::f1;
        s.get();
        // 比较两个对象，用于排序和比较操作
        Comparator<AA> c = ClassFunctionals::f2;
        c.compare(new AA(), new AA());
        // 执行操作，通常是副作用操作，不需要返回结果
        Consumer<AA> cons = ClassFunctionals::f3;
        cons.accept(new AA());
        // 执行操作，通常是副作用操作，不需要返回结果，接受两个参数
        BiConsumer<AA, BB> bicons = ClassFunctionals::f4;
        bicons.accept(new AA(), new BB());
        // 将输入参数转换成输出结果，如数据转换或映射操作
        Function<AA, CC> f = ClassFunctionals::f5;
        CC cc = f.apply(new AA());
        // 将两个输入参数转换成输出结果，如数据转换或映射操作
        BiFunction<AA, BB, CC> bif = ClassFunctionals::f6;
        cc = bif.apply(new AA(), new BB());
        // 接受一个参数，返回 boolean 值： 测试参数是否满足特定条件
        Predicate<AA> p = ClassFunctionals::f7;
        boolean result = p.test(new AA());
        // 接受两个参数，返回 boolean 值，测试两个参数是否满足特定条件
        BiPredicate<AA, BB> bip = ClassFunctionals::f8;
        result = bip.test(new AA(), new BB());
        // 接受一个参数，返回一个相同类型的结果，对输入执行单一操作并返回相同类型的结果，是 Function 的特殊情况
        UnaryOperator<AA> uo = ClassFunctionals::f9;
        AA aa = uo.apply(new AA());
        // 接受两个相同类型的参数，返回一个相同类型的结果，将两个相同类型的值组合成一个新值，是 BiFunction 的特殊情况
        BinaryOperator<AA> bo = ClassFunctionals::f10;
        aa = bo.apply(new AA(), new AA());
    }
}
```

以下是用表格整理的非基本类型的函数式接口：

| 函数式接口          | 特征                                           | 用途                                                         | 方法名                  |
| ------------------- | ---------------------------------------------- | ------------------------------------------------------------ | ----------------------- |
| Supplier<T>         | 无参数，返回一个结果                           | 获取值或实例，工厂模式，延迟计算                             | T get()                 |
| Comparator<T>       | 接受两个参数，返回 int 值                      | 比较两个对象，用于排序和比较操作                             | int compare(T o1, T o2) |
| Consumer<T>         | 接受一个参数，无返回值                         | 执行操作，通常是副作用操作，不需要返回结果                   | void accept(T t)        |
| BiConsumer<T, U>    | 接受两个参数，无返回值                         | 执行操作，通常是副作用操作，不需要返回结果，接受两个参数     | void accept(T t, U u)   |
| Function<T, R>      | 接受一个参数，返回一个结果                     | 将输入参数转换成输出结果，如数据转换或映射操作               | R apply(T t)            |
| BiFunction<T, U, R> | 接受两个参数，返回一个结果                     | 将两个输入参数转换成输出结果，如数据转换或映射操作           | R apply(T t, U u)       |
| Predicate<T>        | 接受一个参数，返回 boolean 值                  | 测试参数是否满足特定条件                                     | boolean test(T t)       |
| BiPredicate<T, U>   | 接受两个参数，返回 boolean 值                  | 测试两个参数是否满足特定条件                                 | boolean test(T t, U u)  |
| UnaryOperator<T>    | 接受一个参数，返回一个相同类型的结果           | 对输入执行单一操作并返回相同类型的结果，是 Function 的特殊情况 | T apply(T t)            |
| BinaryOperator<T>   | 接受两个相同类型的参数，返回一个相同类型的结果 | 将两个相同类型的值组合成一个新值，是 BiFunction 的特殊情况   | T apply(T t1, T t2)     |



#### 多参数函数式接口

java.util.functional 中的接口是有限的，如果需要 3 个参数函数的接口怎么办？自己创建就可以了，如下：

```java
// 创建处理 3 个参数的函数式接口
@FunctionalInterface
public interface TriFunction<T, U, V, R> {
    
    R apply(T t, U u, V v);
}
```

验证如下：

```java
public class TriFunctionTest {
    static int f(int i, long l, double d) { return 99; }

    public static void main(String[] args) {
        // 方法引用
        TriFunction<Integer, Long, Double, Integer> tf1 = TriFunctionTest::f;
        // Lamdba 表达式
        TriFunction<Integer, Long, Double, Integer> tf2 = (i, l, d) -> 12;
    }
}
```



#### 高阶函数

高阶函数（Higher-order Function）其实很好理解，并且在函数式编程中非常常见，它有以下特点：

1. 接收一个或多个函数作为参数
2. 返回一个函数作为结果



先来看看一个函数如何返回一个函数：

```java
import java.util.function.Function;

interface FuncSS extends Function<String, String> {}        // [1] 使用继承，轻松创建属于自己的函数式接口

public class ProduceFunction {
    // produce() 是一个高阶函数：既函数的消费者，产生函数的函数
    static FuncSS produce() {
        return s -> s.toLowerCase();    // [2] 使用 Lambda 表达式，可以轻松地在方法中创建和返回一个函数
    }

    public static void main(String[] args) {
        FuncSS funcSS = produce();
        System.out.println(funcSS.apply("YELLING"));
    }
}
```

然后再看看，如何接收一个函数作为函数的参数：

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

总之，高阶函数使代码更加简洁、灵活和可重用，常见于 `Stream` 流式编程中



### 闭包

在 Java 中，闭包通常与 lambda 表达式和匿名内部类相关。简单来说，闭包允许在一个函数内部访问和操作其外部作用域中的变量。在 Java 中的闭包实际上是一个特殊的对象，它封装了一个函数及其相关的环境。这意味着闭包不仅仅是一个函数，它还携带了一个执行上下文，其中包括外部作用域中的变量。这使得闭包在访问这些变量时可以在不同的执行上下文中保持它们的值。

让我们通过一个例子来理解 Java 中的闭包：

```java
public class ClosureExample {
    public static void main(String[] args) {
        int a = 10;
        int b = 20;

        // 这是一个闭包，因为它捕获了外部作用域中的变量 a 和 b
        IntBinaryOperator closure = (x, y) -> x * a + y * b;

        int result = closure.applyAsInt(3, 4);
        System.out.println("Result: " + result); // 输出 "Result: 110"
    }
}
```

需要注意的是，在 Java 中，闭包捕获的外部变量必须是 `final` 或者是有效的 `final`（即在实际使用过程中保持不变）。这是为了防止在多线程环境中引起不可预测的行为和数据不一致。



### 函数组合

函数组合（Function Composition）意为 “多个函数组合成新函数”。它通常是函数式 编程的基本组成部分。

先看 Function 函数组合示例代码：

```java
import java.util.function.Function;

public class FunctionComposition {
    static Function<String, String> f1 = s -> {
        System.out.println(s);
        return s.replace('A', '_');
    },
    f2 = s -> s.substring(3),
    f3 = s -> s.toLowerCase(),
    // 重点：使用函数组合将多个函数组合在一起
    // compose 是先执行参数中的函数，再执行调用者
    // andThen 是先执行调用者，再执行参数中的函数
    f4 = f1.compose(f2).andThen(f3);        

    public static void main(String[] args) {
        String s = f4.apply("GO AFTER ALL AMBULANCES");
        System.out.println(s);
    }
}
```

代码示例使用了 Function 里的 compose() 和 andThen()，它们的区别如下：

* compose 是先执行参数中的函数，再执行调用者
* andThen 是先执行调用者，再执行参数中的函数

输出结果：

```sh
AFTER ALL AMBULANCES
_fter _ll _mbul_nces
```

然后，再看一段 Predicate 的逻辑运算演示代码：

```java
public class PredicateComposition {
    static Predicate<String>
            p1 = s -> s.contains("bar"),
            p2 = s -> s.length() < 5,
            p3 = s -> s.contains("foo"),
            p4 = p1.negate().and(p2).or(p3);    // 使用谓词组合将多个谓词组合在一起，negate 是取反，and 是与，or 是或

    public static void main(String[] args) {
        Stream.of("bar", "foobar", "foobaz", "fongopuckey")
                .filter(p4)
                .forEach(System.out::println);
    }
}
```

p4 通过函数组合生成一个复杂的谓词，最后应用在 filter() 中：

* negate()：取反值，内容不包含 bar
* and(p2)：长度小于 5
* or(p3)：或者包含 f3

输出结果：

```sh
foobar
foobaz
```

在 `java.util.function` 中常用的支持函数组合的方法，大致如下：

| 函数式接口     | 方法名  | 描述                                                         |
| -------------- | ------- | ------------------------------------------------------------ |
| Function<T, R> | andThen | 用于从左到右组合两个函数，即：`h(x) = g(f(x))`               |
| Function<T, R> | compose | 用于从右到左组合两个函数，即：`h(x) = f(g(x))`               |
| Consumer<T>    | andThen | 用于从左到右组合两个消费者，按顺序执行两个消费者操作         |
| Predicate<T>   | and     | 用于组合两个谓词函数，返回一个新的谓词函数，满足两个谓词函数的条件 |
| Predicate<T>   | or      | 用于组合两个谓词函数，返回一个新的谓词函数，满足其中一个谓词函数的条件 |
| Predicate<T>   | negate  | 用于对谓词函数取反，返回一个新的谓词函数，满足相反的条件     |
| UnaryOperator  | andThen | 用于从左到右组合两个一元操作符，即：`h(x) = g(f(x))`         |
| UnaryOperator  | compose | 用于从右到左组合两个一元操作符，即：`h(x) = f(g(x))`         |
| BinaryOperator | andThen | 用于从左到右组合两个二元操作符，即：`h(x, y) = g(f(x, y))`   |



### 柯里化

柯里化（Currying）是函数式编程中的一种技术，它将一个接受多个参数的函数转换为一系列单参数函数。

让我们通过一个简单的 Java 示例来理解柯里化：

```java
public class CurryingAndPartials {
    static String uncurried(String a, String b) {
        return a + b;
    }

    public static void main(String[] args) {
        // 柯里化的函数，它是一个接受多参数的函数
        Function<String, Function<String, String>> sum = a -> b -> a + b;
        System.out.println(uncurried("Hi ", "Ho"));

        // 通过链式调用逐个传递参数
        Function<String, String> hi = sum.apply("Hi ");
        System.out.println(hi.apply("Ho"));

        Function<String, String> sumHi = sum.apply("Hup ");
        System.out.println(sumHi.apply("Ho"));
        System.out.println(sumHi.apply("Hey"));
    }
}
```

输出结果：

```sh
Hi Ho
Hi Ho
Hup Ho
Hup Hey
```

接下来我们添加层级来柯里化一个三参数函数：

```java
import java.util.function.Function;

public class Curry3Args {
    public static void main(String[] args) {
        // 柯里化函数
        Function<String,
                Function<String,
                        Function<String, String>>> sum = a -> b -> c -> a + b + c;

        // 逐个传递参数
        Function<String, Function<String, String>> hi = sum.apply("Hi ");
        Function<String, String> ho = hi.apply("Ho ");
        System.out.println(ho.apply("Hup"));
    }
}
```

输出结果：

```java
Hi Ho Hup
```

在处理基本类型的时候，注意选择合适的函数式接口：

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

输出结果：

```sh
9
```



### 总结

Lambda 表达式和方法引用并没有将 Java 转换成函数式语言，而是提供了对函数式编程的支持（Java 的历史包袱太重了），这些特性满足了很大一部分的、羡慕 Clojure 和 Scala 这类更函数化语言的 Java 程序员。阻止了他们投奔向那些语言（或者至少让他们在投奔之前做好准备）。总之，Lambdas 和方法引用是 Java 8 中的巨大改进