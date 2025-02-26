+++
date = '2023-04-06T14:32:03+08:00'
draft = false
title = 'Java Stream 流式编程的介绍'
tags = ["Java"]
+++

### 概述

Stream API 是 Java 中引入的一种新的数据处理方法。它提供了一种高效且易于使用的方法来处理数据集合。Stream API 支持函数式编程，可以让我们以简洁、优雅的方式进行数据操作，还有使用 Stream 的两大原因：

1. 在大多数情况下，将对象存储在集合中就是为了处理它们，因此你会发现你把编程 的主要焦点从集合转移到了流上。
2. 当 Lambda 表达式和方法引用（method references），流（Stream）结合使用的时候会让人感觉自成一体，行云流水的感觉



先展示一段简单的流式编程：

```java
import java.util.Random;

public class Randoms {
    
    public static void main(String[] args) {
        // 随机展示 5 至 20 之间不重复的整数并进行排序
        new Random(47)
                .ints(5, 20)
                .distinct()             // 使流中的整数不重复
                .limit(7)       		// 获取前 7 个元素
                .sorted()               // 排序
                .forEach(System.out::println);
    }
}
```

输出结果：

```sh
6
10
13
16
17
18
19
```

实际上函数式的编程风格是声明式（Declarative programming）的，它声明了要做什么， 而不是指明（每一步）如何做。

相同的程序，相比声明式风格，命令式（Imperative）编程的形式（指明每一步如何做），代码阅读起来会更难理解：

```java
import java.util.Random;
import java.util.SortedSet;
import java.util.TreeSet;

public class ImperativeRandoms {

    public static void main(String[] args) {
        Random rand = new Random(47);
        SortedSet<Integer> rints = new TreeSet<>();
        while (rints.size() < 7) {
            int r = rand.nextInt(20);
            if (r < 5) continue;
            rints.add(r);
        }
        System.out.println(rints);
    }
}
```

输出结果：

```sh
[7, 8, 9, 11, 13, 15, 18]
```

所以使用流式编程的几个理由：

1. 表达力强，清晰的语义
2. 内部迭代 internal iteration （看不见迭代过程）更简单的处理并发
3. 流式懒加载的，只在绝对必要时才计算



Java 8 通过在添加接口中添加 default 关键字，通过默认方法的方式将流式 Stream 方法平滑地嵌入到现有的类中，

流操作的类型有三种：

1. 创建流：生产流
2. 修改流元素：中间操作
3. 消费流元素：终端操作，收集流元素，通常式汇入一个集合



### 创建流

通过 `Stream.of()`  很容见的将一组元素转化为流：

```java
import java.util.stream.Stream;

public class StreamOf {

    public static void main(String[] args) {
        // 创建流
        Stream.of(new Bubble(1), new Bubble(2), new Bubble(3))
                .forEach(System.out::println);

        Stream.of("It's ", "a ", "wonderful ", "day ", "for ", "pie!")
                .forEach(System.out::print);

        System.out.println();
        Stream.of(3.14159, 2.718, 1.618)
                .forEach(System.out::println);
    }
}
```

输出结果：

```sh
Bubble 1
Bubble 2
Bubble 3
It's a wonderful day for pie!
3.14159
2.718
1.618
```

通过 `stream()` 方法很容易将传统的集合转化为 Stream：

```java
public class CollectionToStream {

    public static void main(String[] args) {
        List<Bubble> bubbles = Arrays.asList(new Bubble(1), new Bubble(2), new Bubble(3));

        System.out.println(bubbles.stream()  // 将集合转换成为流
                .mapToInt(b -> b.i)          // 获取流中所有元素，对元素进行应用操作，并产生新的对象，这里的 mapToInt 中间操作会转换成为包含整型数字的 IntStream
                .sum());                     // 合计

        HashSet<String> w = new HashSet<>(Arrays.asList("It's a wonderful day for pie!".split(" ")));
        w.stream()
                .map(x -> x + " ")
                .forEach(System.out::print);        // stream 遍历并且打印 Set 中的元素
        System.out.println();

        Map<String, Double> m = new HashMap<>();
        m.put("pi", 3.14159);
        m.put("e", 2.718);
        m.put("phi", 1.618);
        m.entrySet().stream()
                .map(e -> e.getKey() + ": " + e.getValue())
                .forEach(System.out::println);      // stream 遍历并且打印 Map 中的元素
    }
}
```

输出结果：

```sh
6
a pie! It's for wonderful day 
phi: 1.618
e: 2.718
pi: 3.14159
```

#### 随机数流

Java 8 的 `Random` 类也集成流的方法，很方便的创建随机数流：

```java
import java.util.Random;
import java.util.stream.Stream;

// 生成随机数流
public class RandomGenerators {

    public static <T> void show(Stream<T> stream) {
        stream.limit(4).forEach(System.out::println);
        System.out.println("++++++++++");
    }

    public static void main(String[] args) {
        Random rand = new Random(47);
        show(rand.ints().boxed());
        show(rand.longs().boxed());
        show(rand.doubles().boxed());
        // 控制上限和下限
        show(rand.ints(10, 20).boxed());
        show(rand.longs(50, 100).boxed());
        show(rand.doubles(20, 30).boxed());
        // 控制流大小
        show(rand.ints(2).boxed());
        show(rand.longs(2).boxed());
        show(rand.doubles(2).boxed());
        // 控制流大小和上限和下限
        show(rand.ints(3, 3, 9).boxed());
        show(rand.longs(3, 12, 22).boxed());
        show(rand.doubles(3, 11.5, 12.3).boxed());
    }
}
```

输出结果：

```sh
-1172028779
1717241110
-2014573909
229403722
++++++++++
2955289354441303771
3476817843704654257
-8917117694134521474
4941259272818818752
++++++++++
# ……………………
```



#### int 整型范围

Stream API 对基本数据类型生成流提供便捷的方法，例如对一段整型序列求和，展示新旧代码对比

```java
import java.util.stream.IntStream;

public class Ranges {

    public static void main(String[] args) {
        // 传统方法
        int result = 0;
        for (int i = 0; i < 20; i++) {
            result += i;
        }
        System.out.println(result);

        // 使用流
        System.out.println(IntStream.range(0, 20).sum());
    }
}
```

输出结果：

```sh
190
190
```

#### generate()

Stream API 还可以结合 Supplier<T> 函数接口来创建流，例如，创建一个随机数序列：

```java
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class StreamGenerateExample {

    public static void main(String[] args) {
        Random random = new Random();
        Stream<Integer> randomNumbers = Stream.generate(random::nextInt);

        // 生成 10 个随机数放入集合中
        List<Integer> integers = randomNumbers
                .limit(10)
                .collect(Collectors.toList());

        integers.forEach(System.out::println);
    }
}
```

输出结果：

```sh
514000574
1771591868
600289224
-1474939200
-276604430
-876159270
509964750
-497958443
811408347
703285366
```

#### iterate()

`Stream.iterate` 是 Java 8 引入的 Stream API 的一部分，它接受一个种子值（seed）和一个一元函数（unary operator），然后生成一个无限的、顺序的流。流中的每个元素都是通过对前一个元素应用一元函数生成的。与 `Stream.generate` 类似， `Stream.iterate` 常常用于生成一个斐波那契数列，代码示例：

```java
import java.util.stream.Stream;

public class Fibonacci {
    int x = 1;

    Stream<Integer> numbers() {
        return Stream.iterate(0, i -> {
            int result = x + i;
            x = i;
            return result;
        });
    }

    public static void main(String[] args) {
        Fibonacci fbi = new Fibonacci();
        fbi.numbers()
                .skip(20)           // 丢弃前 20 个
                .limit(10)     // 取 10 个
                .forEach(System.out::println);
    }
}
```

输出结果：

```sh
6765
10946
17711
28657
46368
75025
121393
196418
317811
514229
```

`Stream.iterate` 和 `Stream.generate` 都是 Java 8 引入的 Stream API 的一部分，它们用于生成无限的顺序流。稍不留神就容易把它们搞混，可以通过以下的方式来区分它们：

**iterate**：

- 它接受一个种子值（seed）和一个一元函数（unary operator）。
- 它生成的流中的每个元素都是通过对前一个元素应用一元函数生成的。
- 适用于需要生成基于前一个值的序列的场景，例如生成递增/递减序列、斐波那契数列等。



**generate**：

- 它接受一个 `Supplier<T>` 类型的参数。
- 它生成的流中的每个元素都是由提供的 `Supplier` 生成的。
- 适用于生成独立于前一个值的序列的场景，例如生成随机数序列、常量序列等。



#### Arrays

`Arrays`  类中的  `stream()`  方法用于将数组转换为  `Stream`。以下是使用 `Arrays.stream()` 方法的一些示例：

```java
import java.util.Arrays;

public class ArraysStreamExample {

    public static void main(String[] args) {
        // IntStream
        int[] integer = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        Arrays.stream(integer)
                .filter(n -> n % 2 == 0)
                .forEach(System.out::println);

        // Stream<String>
        String[] words = {"hello", "world", "java", "stream"};
        Arrays.stream(words)
                .map(String::toUpperCase)
                .forEach(System.out::println);

        // DoubleStream
        double[] doubles = {1.0, 3.5, 7.2, 8.8, 12.0, 15.5};
        double average = Arrays.stream(doubles)
                .average()
                .orElse(0.0);
        System.out.println("Average: " + average);
    }
}
```

输出结果：

```sh
2
4
6
8
10
HELLO
WORLD
JAVA
STREAM
Average: 8.0
```



### 中间操作

中间操作（intermediate operations）是那些在 Stream 上执行的操作，但不会触发流的处理。它们通常返回一个新的 Stream，该 Stream 包含应用了某种操作后的元素。

以下是一些常见的中间操作：

1. `filter(Predicate<T> predicate)`：根据给定的谓词筛选 Stream 中的元素。
2. `map(Function<T, R> mapper)`：将 Stream 中的每个元素转换为另一种类型，根据给定的映射函数。
3. `flatMap(Function<T, Stream<R>> mapper)`：将每个元素转换为另一个 Stream，然后将所有这些流连接成一个 Stream。
4. `distinct()`：返回一个去重后的 Stream，其中每个元素只出现一次。
5. `sorted()`：返回一个按自然顺序排序的 Stream。
6. `sorted(Comparator<T> comparator)`：根据给定的比较器返回一个排序后的 Stream。
7. `peek(Consumer<T> action)`：对 Stream 中的每个元素执行给定的操作，但不会改变 Stream 中的元素。通常用于调试目的。



注意：中间操作是惰性的，也就是说，它们只在终端操作被调用时才会实际执行。例如 `forEach`、`collect`、`reduce` 等



#### 跟踪和调试

`Stream.peek()` 是一个中间操作，它接受一个 `Consumer`，并允许您在流的每个元素上执行某个操作，同时保持流的元素不变。通常用于调试目的，因为它允许您查看流处理过程中的中间结果。示例：

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Peeking {

    public static void main(String[] args) {
        List<String> names = Arrays.asList("John", "Alice", "Bob", "Cindy", "David");

        List<String> result = names.stream()
                .filter(name -> name.length() > 3)
                .peek(name -> System.out.println("Filtered name: " + name))
                .map(String::toUpperCase)
                .peek(name -> System.out.println("Mapped name: " + name))
                .collect(Collectors.toList());

        System.out.println("Result: " + result);
    }
}
```

以上代码逻辑是：

1. 首先通过 `filter` 操作筛选出长度大于3的名字
2. 然后，我们使用 `peek()` 来打印筛选后的名字
3. 接下来，我们使用 `map` 操作将筛选后的名字转换为大写形式
4. 然后我们再次使用 `peek()` 来打印转换后的名字
5. 最后，我们通过 `collect` 操作将流中的元素收集到一个新的 `List` 中，并打印结果

输出结果：

```sh
Filtered name: John
Mapped name: JOHN
Filtered name: Alice
Mapped name: ALICE
Filtered name: Cindy
Mapped name: CINDY
Filtered name: David
Mapped name: DAVID
Result: [JOHN, ALICE, CINDY, DAVID]
```



#### 排序

`Stream.sorted()` 可以通过内置的比较器，很容易的对集合进行排序

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class Peeking {

    public static void main(String[] args) {
        List<String> names = Arrays.asList("John", "Alice", "Bob", "Cindy", "David");

        List<String> result = names.stream()
                .sorted(Comparator.reverseOrder())
                .map(String::toLowerCase)
                .collect(Collectors.toList());

        System.out.println("Result: " + result);
    }
}
```

输出结果：

```sh
Result: [john, david, cindy, bob, alice]
```



#### 过滤元素

常见的场景，Stream API 提供以下函数进行过滤：

* distinct()：消除流中重复的元素，相比创建 Set 成本低的多
* filter(Predicate)：根据 Predicate 逻辑进行过滤，剩下的元素传递给后面的流



简单看一个示例：

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class DistinctAndFilterExample {

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 2, 1, 4, 5, 4, 6, 7, 7, 8);
        List<Integer> result = numbers.stream()
                .distinct()     // 1: 消除重复元素
                .filter(e -> e % 2 == 0)        //2: 筛选出偶数
                .collect(Collectors.toList());      //3: 将结果放入 List 中

        System.out.println(result);
    }
}
```

以上代码逻辑很简单：

1. 使用 `distinct()` 方法删除重复元素
2. 使用 `filter()` 方法筛选出偶数
3. 我们通过 `collect()` 方法将处理后的 Stream 转换回 List

输出结果：

```sh
[2, 4, 6, 8]
```



#### 操作元素

对元素的操作主要通过 `map(Function)` 来完成，在上面的示例代码中也有看到过，常见于以下场景：

1. 类型转换
2. 数据转换
3. 对象属性提取

> 类似函数 mapToInt，mapToLong，mapToDouble 操作都一样，只是结果分别为：IntStream，LongStream，DoubleStream

以下是一个简单的使用示例：

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class MapExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Using map(Function) to square each number
        List<Integer> squaredNumbers = numbers.stream()
                                              .map(number -> number * number)
                                              .collect(Collectors.toList());

        System.out.println("Original list: " + numbers);
        System.out.println("Squared numbers: " + squaredNumbers);
    }
}
```

输出结果：

```sh
Original list: [1, 2, 3, 4, 5]
Squared numbers: [1, 4, 9, 16, 25]
```



#### 合并流

某些情况，我们输入源的流可能是一个复杂的多层嵌套的数据结构，我们想在处理流数据的同时，顺便也更更改它的结构，例如把它展开为一个展平为单层数据结构，那么 `flatMap()` 中间函数就会派上用场：

* `flatMap()`：与 map() 所作的事情相同，但它将这些生成的 Stream 合并为一个单一的 Stream



##### 有啥用 ?

`flatMap()` 在函数式编程和流式处理中非常有用，因为它可以解决一些常见的数据处理问题。

1. 展平嵌套数据结构：在处理复杂的数据结构时，我们经常会遇到嵌套的集合，例如列表的列表、集合的集合等。`flatMap()` 可以将这些嵌套的数据结构展平为一个单一的流，从而简化后续的数据处理和操作。
2. 合并多个流：在某些情况下，我们需要将多个流合并成一个流，以便对所有流中的数据执行相同的操作。`flatMap()` 可以帮助我们将这些流合并为一个流，从而提高代码的可读性和可维护性。
3. 动态生成流：`flatMap()` 使我们能够根据流中的每个元素动态生成新的流，并将这些新生成的流合并为一个流。这对于根据流中的数据动态创建数据处理管道非常有用。
4. 更高效的操作链：在某些情况下，使用 `flatMap()` 可以减少对流中数据的遍历次数，从而提高操作链的效率。例如，如果我们需要先对流中的每个元素执行映射操作，然后再执行筛选操作，我们可以使用 `flatMap()` 将这两个操作组合在一起，从而减少对流的遍历次数。



展平嵌套数据结构：例如，将一个列表的列表转换为一个包含所有元素的平面列表：

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FlatMapExample {

    public static void main(String[] args) {
        List<List<Integer>> nestedList = Arrays.asList(
                Arrays.asList(1, 2, 3),
                Arrays.asList(4, 5, 6),
                Arrays.asList(7, 8, 9)
        );

        List<Integer> flatList = nestedList.stream()
                .flatMap(list -> list.stream())
                .collect(Collectors.toList());

        System.out.println("Nested list: " + nestedList);
        System.out.println("Flat list: " + flatList);
    }
}
```

输出结果：

```sh
Nested list: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
Flat list: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```



合并多个流：

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class FlatMapExample {

    public static void main(String[] args) {
        List<String> list1 = Arrays.asList("a", "b", "c");
        List<String> list2 = Arrays.asList("d", "e", "f");
        List<String> list3 = Arrays.asList("g", "h", "i");

        // 创建包含多个列表的流
        Stream<List<String>> listsStream = Stream.of(list1, list2, list3);

        // 使用 flatMap() 合并多个流
        List<String> mergedList = listsStream.flatMap(list -> list.stream())
                .collect(Collectors.toList());

        System.out.println("Merged list: " + mergedList);
    }
}
```

说明以下上面的示例的代码：

1. 首先创建了一个包含三个列表的流（`listsStream`）
2. 使用 `flatMap()` 方法将这些列表转换为单独的流，并将这些流合并为一个流
3. 最后，我们使用 `collect()` 方法将合并后的流转换为一个列表（`mergedList`）



通过使用 `flatMap()`，我们可以轻松地将多个流合并为一个流，从而简化数据处理和操作，输出结果：

```sh
Merged list: [a, b, c, d, e, f, g, h, i]
```



##### 和 map() 区别

- `map()` 主要用于转换流中的元素，但保持流的结构不变。
- `flatMap()` 和 `flatMap(Function)` 主要用于将嵌套或多层数据结构展平为单层数据结构。



##### 如何选择 ?

* 如果你只需要对流中的元素执行某种操作或计算，而不需要改变流的结构，那么 `map()` 是一个很好的选择
* 如果你需要将多个 Stream 合并为一个 Stream，或者将嵌套数据结构展平为单层数据结构，那么 `flatMap()` 是一个更合适的选择



### Optional 类

Optional 主要用于在流中处理一些空元素，但是它还可以应用在代码的其他地方，它带来以下一些好处，例如：

* 避免 NullPointerException：Optional 类帮助您更优雅地处理可能为 null 的值
* 提高代码可读性：使用 Optional 类可以让您的代码更具表现力，更容易理解
* 更好的 API 设计：使用 Optional 类可以让您的 API 更清晰地表达预期行为，例如，返回值可能为空的情况。



#### 流里面的 Optional

在使用 Stream 时，很多操作都会返回 `Optional ` 对象，例如：

* findFirst(): 返回 Stream 中的第一个对象，使用 Optional 包装
* findAny(): 返回 Stream 中任意一个对象，使用 Optional 包装
* max(): 返回 Stream 中最大的对象，使用 Optional 包装
* min(): 返回 Stream 中最小的对象，使用 Optional 包装
* average(): 返回 Stream 中所有对象的平均值，使用 OptionalDouble 包装



示例代码：

```java
import java.util.*;

public class OptionalExample {

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9);

        Optional<Integer> firstNumber = numbers.stream().filter(n -> n % 2 == 0).findFirst();
        System.out.println("findFirst() example: " + firstNumber.orElse(-1));   // 输出：2

        Optional<Integer> anyNumber = numbers.stream().filter(n -> n > 2).findAny();
        System.out.println("findAny() example: " + anyNumber.orElse(-1));   // 输出：3

        Optional<Integer> maxNumber = numbers.stream().max(Comparator.naturalOrder());
        System.out.println("max() example: " + maxNumber.orElse(-1)); // 输出：9

        Optional<Integer> minNumber = numbers.stream().min(Comparator.naturalOrder());
        System.out.println("min() example: " + minNumber.orElse(-1)); // 输出：1

        OptionalDouble average = numbers.stream().mapToInt(Integer::intValue).average();
        System.out.println("average() example: " + (average.isPresent() ? average.getAsDouble() : -1)); // 输出：5.0
    }
}
```

输出结果：

```sh
findFirst() example: 2
findAny() example: 3
max() example: 9
min() example: 1
average() example: 5.0
```

示例代码还展示一些解包 Optional 的操作：

* ifPresent(Consumer)：当值存在时调用 Consumer，否则什么也不做
* orElse(otherObject)：如果值存在则直接返回，否则生成 otherObject



Optional 还提供更灵活的 Supplier 函数式接口的调用：

* orElseGet(Supplier)：如果值存在则直接返回，否则使用 Supplier 函数生成一 个可替代对象
* orElseThrow(Supplier)：如果值存在直接返回，否则使用 Supplier 函数生成一 个异常

可以通过以下示例代码来理解：

```java
public class OptionalExample {

    public static void main(String[] args) {
        // 生成一个空 Optional
        Optional<String> optionalValue = Optional.empty();

        // orElseGet() 示例
        String value1 = optionalValue.orElseGet(() -> "Default value");
        System.out.println("Value 1: " + value1); // 输出：Value 1: Default value

        // orElseThrow() 示例
        try {
            String value2 = optionalValue.orElseThrow(
                () -> new IllegalStateException("Value is not present")
            );
            System.out.println("Value 2: " + value2);
        } catch (RuntimeException e) {
            // 输出：Exception caught: Value is not present
            System.out.println("Exception caught: " + e.getMessage()); 
        }
    }
}
```

输出结果：

```sh
Value 1: Default value
Exception caught: Value is not present
```



#### 创建 Optional

我们也可以在自己的代码里面创建 Optional 对象，有以下几个静态方法可以使用：

* Optional.empty()：创建一个空的 `Optional` 对象。这个对象不包含任何值
* Optional.of()：使用一个非空值创建一个 `Optional` 对象。如果传入的值为 null，将抛出一个空指针异常
* Optional.ofNullable()：创建一个可能为 null 的 `Optional` 对象



示例代码：

```java
import java.util.*;

public class OptionalExample {
    
    public static void main(String[] args) {
        // 生成一个空的 Optional
        Optional<String> emptyOptional = Optional.empty();
        // 生成一个不为空的 Optional
        Optional<String> optionalWithValue = Optional.of("hello world");
        // 可能为空的 Optional
        Optional<String> optionalWithValue1 = Optional.ofNullable("hello world"); // 非空值
        Optional<String> optionalWithValue2 = Optional.ofNullable(null); // 空值
    }
}
```



#### 操作 Optional

创建 Optional 对象后，可以通过内置的函数对 Optional 进行更多的操作，常见的有：

* filter(Predicate): 对象的值满足给定的 Predicate，则返回该 Optional 对象
* map(Function): 使用给定的 Function 对该值进行转换，并返回一个包含转换后值的新 Optional 对象
* flatMap(Function): 使用给定的 Function 对该值进行转换，并返回一个包含转换后值的新 Optional 对象。



示例代码：

```java
import java.util.*;

public class OptionalExample {

    public static void main(String[] args) {
        Optional<Integer> optionalValue1 = Optional.of(10);
        Optional<Integer> optionalValue2 = Optional.empty();

        // 使用 filter() 方法
        Optional<Integer> filteredValue1 = optionalValue1.filter(value -> value > 5);
        System.out.println("Filtered value 1: " + filteredValue1.orElse(-1));
        
        // 使用 map() 方法
        Optional<String> mappedValue1 = optionalValue1.map(value -> "Value is: " + value);
        System.out.println("Mapped value 1: " + mappedValue1.orElse("Not present"));
        
        // 使用 flatMap() 方法
        Optional<String> flatMappedValue1 = optionalValue2.flatMap(value -> Optional.of("Value is: " + value));
        System.out.println("FlatMapped value 1: " + flatMappedValue1.orElse("Not present"));
    }
}
```

输出结果：

```sh
Filtered value 1: 10
Mapped value 1: Value is: 10
FlatMapped value 1: Not present
```

注意：这里的 `flatMap()` 与  `map()` 方法不同，`flatMap()` 会改变 Optional 结构本身，`map()` 则不会



### 终端操作

终端操作（Terminal Operations）是我们在流管道中所做的最后一件事，通过该操作获得流中的结果



#### 数组

通过以下方法，可以轻易的收集一个流，并且将流转为数组：

* toArray()：转换为对象数组
* toArray(generator)：转换为特定类型的数组



示例代码：

```java
import java.util.Arrays;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class StreamToArrayExample {

    public static void main(String[] args) {
        // 转换为对象数组
        Stream<String> stringStream1 = Stream.of("apple", "banana", "cherry");
        System.out.println("Stream to array 1: " + Arrays.toString(stringStream1.toArray()));

        // 转换为特定类型的数组
        Stream<String> stringStream2 = Stream.of("apple", "banana", "cherry");
        String[] stringArray = stringStream2.toArray(String[]::new);
        System.out.println("Stream to array 2: " + Arrays.toString(stringArray));

        // 对于基本类型的数组，可以使用特定的流类
        int[] array = IntStream.range(1, 6).toArray();
        System.out.println("Stream to array 3: " + Arrays.toString(array));
    }
}
```

输出结果：

```sh
Stream to array 1: [apple, banana, cherry]
Stream to array 2: [apple, banana, cherry]
Stream to array 3: [1, 2, 3, 4, 5]
```



#### 循环

Stream 中提供 2 个循环遍历方法，用于消费流，分别如下：

* forEach()：遍历流，在并行流中不保证流的顺序
* forEachOrdered()：遍历流，在并行流中保证按照流中元素的顺序执行操作



我们通过以下示例代码来证明：

```java
import java.util.Arrays;
import java.util.List;

public class ForEachOrderedParallelExample {

    public static void main(String[] args) {
        List<String> stringList = Arrays.asList("apple", "banana", "cherry", "date", "fig", "grape");

        // 顺序流
        System.out.println("Sequential stream:");
        stringList.stream().forEachOrdered(System.out::println);

        // 并行流 （乱序）
        System.out.println("\nParallel stream with forEach:");
        stringList.parallelStream().forEach(System.out::println);

        // 并行流 （顺序）
        System.out.println("\nParallel stream with forEachOrdered:");
        stringList.parallelStream().forEachOrdered(System.out::println);
    }
}
```

输出结果：

```sh
Sequential stream:
apple
banana
cherry
date
fig
grape

Parallel stream with forEach:
date
grape
fig
cherry
banana
apple

Parallel stream with forEachOrdered:
apple
banana
cherry
date
fig
grape
```



#### 集合

主要用于将流中的元素收集到不同类型的结果容器，如集合、字符串或其他数据结构。它的主要方法有：

* collect(Collector)：使用 Collector 收集流元素到结果集合中



我们看看如何把 Stream 收集为常见的 `List`，`Set`，`Map`，还有 `String` ，示例代码：

```java
public class CollectExample {

    public static void main(String[] args) {
        // 收集到 List
        List<String> collectedList = Stream.of("apple", "banana", "orange", "grape")
                .map(String::toUpperCase)
                .collect(Collectors.toList());
        System.out.println("Collected List: " + collectedList);

        // 收集到 Set
        Set<String> collectedSet = Stream.of("apple", "banana", "orange", "grape")
                .map(String::toLowerCase)
                .collect(Collectors.toSet());
        System.out.println("Collected Set: " + collectedSet);

        // 收集到 Map
        Map<String, Integer> map = Stream.of("apple", "banana", "orange", "grape")
                .map(String::toUpperCase)
                .collect(Collectors.toMap(s -> s, String::length));
        System.out.println("Collected Map: " + map);

        // 收集到 String，使用逗号分隔
        String joinedString  = Stream.of("apple", "banana", "orange", "grape")
                .map(String::toUpperCase)
                .collect(Collectors.joining(","));
        System.out.println("Joined String: " + joinedString);
    }
}
```

输出结果：

```sh
Collected List: [APPLE, BANANA, ORANGE, GRAPE]
Collected Set: [banana, orange, apple, grape]
Collected Map: {APPLE=5, GRAPE=5, BANANA=6, ORANGE=6}
Joined String: APPLE,BANANA,ORANGE,GRAPE
```

说明：在这里我们只是简单介绍了几个 Collectors 的运用示例。

实际上，它还有一些非常复杂的操作实现，可通过查看 `java.util.stream.Collectors` 的 API 文档了解



#### 组合

用于对流中的元素执行累积操作，将它们减少为一个值。`reduce` 的使用场景包括对流中的元素执行聚合操作，例如求和、求积、求最大值、求最小值等。`Stream` 里面的 `reduce` 方法有以下几种形式：

* reduce(BinaryOperator)：使用给定的累积器函数，对流中的元素进行累积操作。返回一个 `Optional<T>`
* reduce(identity, BinaryOperator)： 使用给定的初始值（identity）和累积器函数，对流中的元素进行累积操作。因此如果流为空，identity 就是结果



先看看 reduce 的示例代码：

```java
import java.util.OptionalInt;
import java.util.stream.IntStream;

public class ReduceExample {

    public static void main(String[] args) {
        // 求和
        OptionalInt sum = IntStream.range(0, 100).reduce(Integer::sum);
        sum.ifPresent(System.out::println);

        // 求积
        OptionalInt numbers = IntStream.range(0, 100).reduce((a, b) -> a * b);
        numbers.ifPresent(System.out::println);

        // 求最大值
        OptionalInt max = IntStream.range(0, 100).reduce(Integer::max);
        max.ifPresent(System.out::println);

        // 求最小值
        OptionalInt min = IntStream.range(0, 100).reduce(Integer::min);
        min.ifPresent(System.out::println);
        
        // 使用给定的初始值（identity）和累积器函数，对流中的元素进行累积操作，这里返回 int 值
        int reduced = IntStream.range(0, 100).reduce(10, Integer::sum);
        System.out.println(reduced);
    }
}
```

输出结果：

```sh
4950
0
99
0
4960
```

还有一种 `reduce(identity, BiFunction, BinaryOperator)`：更复杂的使用形式暂不介绍。我建议可以显式地组合 map() 和 reduce() 来更简单的表达它。



#### 匹配

在 Stream 中的终端操作中，提供 `allMatch`, `anyMatch`, 和 `noneMatch` 它们用于检查流中的元素是否满足某个条件：

* allMatch(Predicate) ：流的每个元素提供给 Predicate 都返回 true ，结果返回为 true
* anyMatch(Predicate)：流中任意一个元素提供的 Predicate 返回 true，结果返回 true
* noneMatch(Predicate)：流的每个元素提供的 Predicate 返回 false，结果返回 true

PS：以上计算都是短路操作，在匹配第一个结果时，则停止执行计算



下面是它们的使用场景和示例：

```java
import java.util.stream.Stream;

public class MatchExample {

    public static void main(String[] args) {
        // allMatch：检查流中的所有元素是否都满足某个条件
        boolean allEven = Stream.of(1, 2, 3, 4, 5).allMatch(num -> num % 2 == 0);
        System.out.println(allEven); // 输出：false

        // anyMatch：检查流中是否存在满足某个条件的元素
        boolean anyEven = Stream.of(1, 2, 3, 4, 5).anyMatch(num -> num % 2 == 0);
        System.out.println(anyEven); // 输出：true

        // noneMatch：检查流中是否不存在满足某个条件的元素
        boolean noneMatch = Stream.of(1, 2, 3, 4, 5).noneMatch(num -> num > 10);
        System.out.println(noneMatch);  // 输出：true
    }
}
```

输出结果：

```sh
false
true
true
```



#### 查找

在 Stream 中的终端操作中，可以根据 `Predicate` 获取指定的元素（在 Optional 章节介绍过），查找函数如下：

* findFirst()：查找第一个满足某个条件的元素，这在有序流中非常有用
* findAny()：在流中查找任意一个满足某个条件的元素，这在并行流中非常有用



代码示例：

```java
import java.util.Optional;
import java.util.stream.Stream;

public class FindExample {

    public static void main(String[] args) {
        // findFirst 示例
        Optional<Integer> first = Stream.of(1, 2, 3, 4, 5).filter(num -> num % 2 == 0).findFirst();
        first.ifPresent(System.out::println); // 输出：2

        // findAny 示例
        Optional<Integer> any = Stream.of(1, 2, 3, 4, 5, 6).filter(num -> num % 2 == 0).findAny();
        any.ifPresent(System.out::println); // 输出：2 或者 4 或者 6
    }
}
```



#### 统计

最后就是一些常见对流进行统计的函数了：

* count()：统计流中的元素数量
* max(Comparator)：根据给定的比较器查找流中的最大值
* min(Comparator)：根据给定的比较器查找流中的最小值



示例代码：

```java
// count: 流中的元素个数
System.out.println(Stream.of(1, 2, 3, 4, 5).count()); // 输出：5

List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
Optional<Integer> max = numbers.stream().max(Comparator.naturalOrder());
Optional<Integer> min = numbers.stream().min(Comparator.naturalOrder());

// max, min: 根据给定的比较器查找流中的最大值或最小值
max.ifPresent(System.out::println); // 输出：5
min.ifPresent(System.out::println); // 输出：1
```

输出结果：

```sh
5
5
1
```



以下方式是适用于基本数据类型的特殊流，它们提供了对流中数字的基本统计信息：

* average() ：求取流元素平均值
* max() 和 min()：数值流操作无需 Comparator
* sum()：对所有流元素进行求和

代码示例：

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
// average: 求取流元素平均值
numbers.stream().mapToInt(Integer::intValue).average().ifPresent(System.out::println);  // 输出：3.0
// max: 数值流求最大值
numbers.stream().mapToInt(Integer::intValue).max().orElse(0);  // 输出：5
// min: 数值流最小值
numbers.stream().mapToInt(Integer::intValue).min().orElse(0);  // 输出：1
// sum: 数值流求和
numbers.stream().mapToInt(Integer::intValue).sum();  // 输出：15
```

上例操作对于 LongStream 和 DoubleStream 同样适用



### 总结

函数式编程 对 Java 语言的编程范式产生了深远的影响。在 Stream API 出现之前，处理集合数据通常需要使用 for 循环、条件判断和辅助变量等。这样的代码往往冗长、复杂，不易阅读和维护。Stream API 的引入，让我们能以函数式编程的方式处理数据，提高了代码的简洁性、可读性和可维护性。随着函数式编程在软件开发领域的普及，Java 可能会引入更多的函数式编程特性，让我们能够更方便地使用函数式编程范式编写代码。随着函数式编程在软件开发领域的普及，Java 可能会引入更多的函数式编程特性，让我们能够更方便地使用函数式编程范式编写代码。  总之，Java 其未来依然充满潜力。随着技术的发展和需求的变化，Java 将不断演进，为开发者提供更好的编程体验