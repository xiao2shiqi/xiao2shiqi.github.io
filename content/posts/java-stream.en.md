+++
date = '2023-04-06T14:32:03+08:00'
draft = false
title = 'Introduction to Stream Programming in Java'
tags = ["Java"]
+++

### Overview

The Stream API is a new data processing method introduced in Java. It provides an efficient and easy-to-use way to handle data collections. The Stream API supports functional programming, allowing us to perform data operations in a concise and elegant manner. There are two major reasons for using Streams:

1. In most cases, objects are stored in collections precisely to process them, so you will find your primary programming focus shifting from the collection to the stream.
2. When Lambda expressions, method references, and Streams are combined, the code feels cohesive and exceptionally smooth.

First, let's look at a simple example of stream programming:

```java
import java.util.Random;

public class Randoms {
    
    public static void main(String[] args) {
        // Randomly display unique integers between 5 and 20 and sort them
        new Random(47)
                .ints(5, 20)
                .distinct()             // Make integers in the stream unique
                .limit(7)       		// Get the first 7 elements
                .sorted()               // Sort
                .forEach(System.out::println);
    }
}
```

Output:

```sh
6
10
13
16
17
18
19
```

In fact, the functional programming style is declarative; it declares *what* to do rather than specifying (step-by-step) *how* to do it.

The same program, written in an imperative style (specifying every step), is harder to read and understand than the declarative version:

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

Output:

```sh
[7, 8, 9, 11, 13, 15, 18]
```

Reasons to use stream programming include:

1. High expressiveness and clear semantics.
2. Internal iteration (the iteration process is hidden), making it easier to handle concurrency.
3. Streams are lazily loaded; calculations are only performed when absolutely necessary.

Java 8 smoothly integrated the `Stream` methods into existing classes through default methods added using the `default` keyword in interfaces.

There are three types of stream operations:

1. **Creating the Stream**: Producing the stream.
2. **Intermediate Operations**: Modifying stream elements.
3. **Terminal Operations**: Consuming stream elements, often collecting them into a collection.

### Creating Streams

A group of elements can be easily converted into a stream using `Stream.of()`:

```java
import java.util.stream.Stream;

public class StreamOf {

    public static void main(String[] args) {
        // Create a stream
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

Output:

```sh
Bubble 1
Bubble 2
Bubble 3
It's a wonderful day for pie!
3.14159
2.718
1.618
```

Traditional collections can be easily converted into a Stream using the `stream()` method:

```java
public class CollectionToStream {

    public static void main(String[] args) {
        List<Bubble> bubbles = Arrays.asList(new Bubble(1), new Bubble(2), new Bubble(3));

        System.out.println(bubbles.stream()  // Convert collection to stream
                .mapToInt(b -> b.i)          // Intermediate operation: perform operation and produce new objects (IntStream here)
                .sum());                     // Total sum

        HashSet<String> w = new HashSet<>(Arrays.asList("It's a wonderful day for pie!".split(" ")));
        w.stream()
                .map(x -> x + " ")
                .forEach(System.out::print);        // Traverse and print Set elements via stream
        System.out.println();

        Map<String, Double> m = new HashMap<>();
        m.put("pi", 3.14159);
        m.put("e", 2.718);
        m.put("phi", 1.618);
        m.entrySet().stream()
                .map(e -> e.getKey() + ": " + e.getValue())
                .forEach(System.out::println);      // Traverse and print Map elements via stream
    }
}
```

Output:

```sh
6
a pie! It's for wonderful day 
phi: 1.618
e: 2.718
pi: 3.14159
```

#### Random Number Streams

Java 8's `Random` class has integrated stream methods, making it convenient to create random number streams:

```java
import java.util.Random;
import java.util.stream.Stream;

// Generate random number streams
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
        // Control upper and lower bounds
        show(rand.ints(10, 20).boxed());
        show(rand.longs(50, 100).boxed());
        show(rand.doubles(20, 30).boxed());
        // Control stream size
        show(rand.ints(2).boxed());
        show(rand.longs(2).boxed());
        show(rand.doubles(2).boxed());
        // Control size and upper/lower bounds
        show(rand.ints(3, 3, 9).boxed());
        show(rand.longs(3, 12, 22).boxed());
        show(rand.doubles(3, 11.5, 12.3).boxed());
    }
}
```

Output:

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
# ...
```

#### Integer Range

The Stream API provides convenient methods for generating streams of primitive data types. For example, summing an integer sequence:

```java
import java.util.stream.IntStream;

public class Ranges {

    public static void main(String[] args) {
        // Traditional method
        int result = 0;
        for (int i = 0; i < 20; i++) {
            result += i;
        }
        System.out.println(result);

        // Using Stream
        System.out.println(IntStream.range(0, 20).sum());
    }
}
```

Output:

```sh
190
190
```

#### generate()

The Stream API can also create streams using an implementation of the `Supplier<T>` functional interface. For example, creating a random number sequence:

```java
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class StreamGenerateExample {

    public static void main(String[] args) {
        Random random = new Random();
        Stream<Integer> randomNumbers = Stream.generate(random::nextInt);

        // Generate 10 random numbers and collect into a list
        List<Integer> integers = randomNumbers
                .limit(10)
                .collect(Collectors.toList());

        integers.forEach(System.out::println);
    }
}
```

Output:

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

`Stream.iterate`, introduced in Java 8, takes a seed value and a unary operator, generating an infinite sequential stream. Each element is generated by applying the unary operator to the previous element. Like `Stream.generate`, it's often used to generate sequences, such as the Fibonacci numbers:

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
                .skip(20)           // Discard first 20
                .limit(10)     // Take 10
                .forEach(System.out::println);
    }
}
```

Output:

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

`Stream.iterate` and `Stream.generate` are both used to generate infinite sequential streams. They can be distinguished as follows:

- **iterate**: Accepts a seed value and a unary operator. Each element depends on the previous one. Suitable for sequences like increments/decrements or Fibonacci.
- **generate**: Accepts a `Supplier<T>`. Each element is independent of the previous ones. Suitable for random number sequences or constant sequences.

#### Arrays

The `Arrays.stream()` method is used to convert an array to a `Stream`:

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

Output:

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

### Intermediate Operations

Intermediate operations are performed on a Stream but do not trigger processing. They return a new Stream that contains elements after the operation is applied.

Common intermediate operations:

1. `filter(Predicate<T> predicate)`: Filters elements based on a predicate.
2. `map(Function<T, R> mapper)`: Transforms elements to another type using a mapping function.
3. `flatMap(Function<T, Stream<R>> mapper)`: Transforms each element into another Stream and joins all generated streams into one.
4. `distinct()`: Returns a Stream with unique elements.
5. `sorted()`: Returns a Stream sorted by natural order.
6. `sorted(Comparator<T> comparator)`: Returns a Stream sorted according to a given comparator.
7. `peek(Consumer<T> action)`: Performs an action on each element without changing the Stream. Often used for debugging.

Note: Intermediate operations are lazy; they only execute when a terminal operation like `forEach`, `collect`, or `reduce` is called.

#### Tracking and Debugging

`Stream.peek()` is an intermediate operation that takes a `Consumer` and allows you to perform an action on each element while keeping the Stream unchanged. It's often used to view intermediate results during stream processing.

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

The logic is:
1. Filter names with length > 3.
2. Use `peek()` to print filtered names.
3. Use `map` to convert names to uppercase.
4. Use `peek()` to print converted names.
5. Collect and print result.

Output:

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

#### Sorting

`Stream.sorted()` can easily sort a collection using built-in or custom comparators:

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class SortingExample {

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

Output:

```sh
Result: [john, david, cindy, bob, alice]
```

#### Filtering

Commonly, Stream API provides these functions for filtering:

- `distinct()`: Eliminates duplicates with much lower cost than creating a Set.
- `filter(Predicate)`: Passes elements to the next stage only if they satisfy the predicate logic.

Example:

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class DistinctAndFilterExample {

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 2, 1, 4, 5, 4, 6, 7, 7, 8);
        List<Integer> result = numbers.stream()
                .distinct()     // 1: Eliminate duplicates
                .filter(e -> e % 2 == 0)        // 2: Filter even numbers
                .collect(Collectors.toList());      // 3: Collect into List

        System.out.println(result);
    }
}
```

Output:

```sh
[2, 4, 6, 8]
```

#### Manipulating Elements

Manipulation is mainly done via `map(Function)`, commonly seen in:

1. Type conversion.
2. Data transformation.
3. Object attribute extraction.

> Functions like `mapToInt`, `mapToLong`, and `mapToDouble` work the same but result in `IntStream`, `LongStream`, and `DoubleStream` respectively.

Example:

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class MapExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Square each number
        List<Integer> squaredNumbers = numbers.stream()
                                               .map(number -> number * number)
                                               .collect(Collectors.toList());

        System.out.println("Original list: " + numbers);
        System.out.println("Squared numbers: " + squaredNumbers);
    }
}
```

Output:

```sh
Original list: [1, 2, 3, 4, 5]
Squared numbers: [1, 4, 9, 16, 25]
```

#### Merging Streams

Sometimes the input source might be a complex multi-layered nested structure. If we want to flatten it into a single-layer structure while processing, `flatMap()` comes into play:

- `flatMap()`: Performs the same task as `map()` but merges generated Streams into a single Stream.

**What is it for?**

`flatMap()` is very useful in functional programming:

1. **Flattening nested structures**: Converts nested collections (e.g., list of lists) into a single stream, simplifying subsequent operations.
2. **Merging multiple streams**: Joins several streams into one to perform the same operation on all data.
3. **Dynamic stream generation**: Generates new streams based on each element and merges them. This is great for dynamic data processing pipelines.
4. **More efficient operation chains**: Can reduce the number of traversals by combining mapping and filtering operations.

Example of flattening:

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

Output:

```sh
Nested list: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
Flat list: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Example of merging multiple streams:

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MergeStreamsExample {

    public static void main(String[] args) {
        List<String> list1 = Arrays.asList("a", "b", "c");
        List<String> list2 = Arrays.asList("d", "e", "f");
        List<String> list3 = Arrays.asList("g", "h", "i");

        // Create stream containing multiple lists
        Stream<List<String>> listsStream = Stream.of(list1, list2, list3);

        // Merge into one stream
        List<String> mergedList = listsStream.flatMap(list -> list.stream())
                .collect(Collectors.toList());

        System.out.println("Merged list: " + mergedList);
    }
}
```

Output:

```sh
Merged list: [a, b, c, d, e, f, g, h, i]
```

**Difference from `map()`:**

- `map()` transforms elements while keeping the Stream structure unchanged.
- `flatMap()` flattens nested or multi-layered structures into a single Stream.

**How to choose?**

- If you only need to perform operations or calculations on elements without changing Stream structure, `map()` is the choice.
- If you need to merge multiple Streams or flatten nested data, `flatMap()` is more appropriate.

### The Optional Class

`Optional` is primarily used to handle null elements in streams, but it can be used elsewhere in code, offering benefits like:

- Avoiding `NullPointerException`.
- Improving code readability.
- Better API design (clearly expressing that a return value might be empty).

#### Optional in Streams

Many Stream operations return `Optional` objects:

- `findFirst()`: Returns the first object in the Stream, wrapped in `Optional`.
- `findAny()`: Returns any object from the Stream, wrapped in `Optional`.
- `max()`: Returns the largest object, wrapped in `Optional`.
- `min()`: Returns the smallest object, wrapped in `Optional`.
- `average()`: Returns the average of numeric elements, wrapped in `OptionalDouble`.

Example:

```java
import java.util.*;

public class OptionalExample {

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9);

        Optional<Integer> firstNumber = numbers.stream().filter(n -> n % 2 == 0).findFirst();
        System.out.println("findFirst() example: " + firstNumber.orElse(-1));

        Optional<Integer> anyNumber = numbers.stream().filter(n -> n > 2).findAny();
        System.out.println("findAny() example: " + anyNumber.orElse(-1));

        Optional<Integer> maxNumber = numbers.stream().max(Comparator.naturalOrder());
        System.out.println("max() example: " + maxNumber.orElse(-1));

        Optional<Integer> minNumber = numbers.stream().min(Comparator.naturalOrder());
        System.out.println("min() example: " + minNumber.orElse(-1));

        OptionalDouble average = numbers.stream().mapToInt(Integer::intValue).average();
        System.out.println("average() example: " + (average.isPresent() ? average.getAsDouble() : -1));
    }
}
```

Output:

```sh
findFirst() example: 2
findAny() example: 3
max() example: 9
min() example: 1
average() example: 5.0
```

Operations to unpack `Optional`:

- `ifPresent(Consumer)`: Calls the Consumer if a value exists.
- `orElse(otherObject)`: Returns the value if it exists, otherwise returns `otherObject`.
- `orElseGet(Supplier)`: Returns the value if it exists, otherwise uses the Supplier to generate an alternative.
- `orElseThrow(Supplier)`: Returns the value if it exists, otherwise throws an exception generated by the Supplier.

```java
public class OptionalUnpacking {

    public static void main(String[] args) {
        Optional<String> optionalValue = Optional.empty();

        // orElseGet() example
        String value1 = optionalValue.orElseGet(() -> "Default value");
        System.out.println("Value 1: " + value1);

        // orElseThrow() example
        try {
            String value2 = optionalValue.orElseThrow(() -> new IllegalStateException("Value not present"));
            System.out.println("Value 2: " + value2);
        } catch (RuntimeException e) {
            System.out.println("Exception caught: " + e.getMessage()); 
        }
    }
}
```

Output:

```sh
Value 1: Default value
Exception caught: Value not present
```

#### Creating Optional

You can create `Optional` objects in your code using these static methods:

- `Optional.empty()`: Creates an empty `Optional`.
- `Optional.of(value)`: Creates an `Optional` using a non-null value (throws exception if null).
- `Optional.ofNullable(value)`: Creates an `Optional` that might be null.

#### Operating on Optional

Common built-in functions for `Optional`:

- `filter(Predicate)`: Returns the `Optional` if the value satisfies the predicate.
- `map(Function)`: Returns a new `Optional` containing the result of applying the transformation.
- `flatMap(Function)`: Similar to `map()`, but for functions that themselves return an `Optional`.

```java
public class OptionalOperations {

    public static void main(String[] args) {
        Optional<Integer> optionalValue1 = Optional.of(10);
        Optional<Integer> optionalValue2 = Optional.empty();

        // filter()
        Optional<Integer> filteredValue1 = optionalValue1.filter(value -> value > 5);
        System.out.println("Filtered value 1: " + filteredValue1.orElse(-1));
        
        // map()
        Optional<String> mappedValue1 = optionalValue1.map(value -> "Value is: " + value);
        System.out.println("Mapped value 1: " + mappedValue1.orElse("Not present"));
        
        // flatMap()
        Optional<String> flatMappedValue1 = optionalValue2.flatMap(value -> Optional.of("Value is: " + value));
        System.out.println("FlatMapped value 1: " + flatMappedValue1.orElse("Not present"));
    }
}
```

Output:

```sh
Filtered value 1: 10
Mapped value 1: Value is: 10
FlatMapped value 1: Not present
```

Note: `flatMap()` in `Optional` changes the structure, while `map()` does not.

### Terminal Operations

Terminal operations are the last step in a stream pipeline, returning the final result.

#### Arrays

Collect a Stream and convert it to an array:

- `toArray()`: Convert to an array of Objects.
- `toArray(generator)`: Convert to an array of a specific type.

```java
import java.util.Arrays;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class StreamToArrayExample {

    public static void main(String[] args) {
        // To Object array
        Stream<String> s1 = Stream.of("apple", "banana", "cherry");
        System.out.println("Object array: " + Arrays.toString(s1.toArray()));

        // To specific type array
        Stream<String> s2 = Stream.of("apple", "banana", "cherry");
        String[] specificArray = s2.toArray(String[]::new);
        System.out.println("String array: " + Arrays.toString(specificArray));

        // For primitives
        int[] intArray = IntStream.range(1, 6).toArray();
        System.out.println("Int array: " + Arrays.toString(intArray));
    }
}
```

Output:

```sh
Object array: [apple, banana, cherry]
String array: [apple, banana, cherry]
Int array: [1, 2, 3, 4, 5]
```

#### Iteration

Stream provides two ways to consume elements:

- `forEach()`: Normal traversal; order is not guaranteed in parallel streams.
- `forEachOrdered()`: Traversal that guarantees element order even in parallel streams.

Example proof:

```java
import java.util.Arrays;
import java.util.List;

public class ForEachExample {

    public static void main(String[] args) {
        List<String> list = Arrays.asList("apple", "banana", "cherry", "date", "fig", "grape");

        // Sequential
        System.out.println("Sequential:");
        list.stream().forEachOrdered(System.out::println);

        // Parallel (unordered)
        System.out.println("\nParallel with forEach:");
        list.parallelStream().forEach(System.out::println);

        // Parallel (ordered)
        System.out.println("\nParallel with forEachOrdered:");
        list.parallelStream().forEachOrdered(System.out::println);
    }
}
```

#### Collections

Collect elements into containers like List, Set, Map, or String.

- `collect(Collector)`: Uses a Collector to gather elements.

```java
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.*;

public class CollectExample {

    public static void main(String[] args) {
        // Collect to List
        List<String> list = Stream.of("apple", "banana", "orange", "grape")
                .map(String::toUpperCase)
                .collect(Collectors.toList());
        System.out.println("List: " + list);

        // Collect to Set
        Set<String> set = Stream.of("apple", "banana", "orange", "grape")
                .map(String::toLowerCase)
                .collect(Collectors.toSet());
        System.out.println("Set: " + set);

        // Collect to Map
        Map<String, Integer> map = Stream.of("apple", "banana", "orange", "grape")
                .collect(Collectors.toMap(s -> s, String::length));
        System.out.println("Map: " + map);

        // Join to String
        String joined = Stream.of("apple", "banana", "orange", "grape")
                .collect(Collectors.joining(","));
        System.out.println("Joined String: " + joined);
    }
}
```

#### Reduction

Performs cumulative operations to reduce the Stream to a single value.

- `reduce(BinaryOperator)`: Returns an `Optional<T>`.
- `reduce(identity, BinaryOperator)`: Uses an initial value; returns type `T`.

Example:

```java
import java.util.stream.IntStream;
import java.util.OptionalInt;

public class ReduceExample {

    public static void main(String[] args) {
        // Sum
        OptionalInt sum = IntStream.range(0, 100).reduce(Integer::sum);
        sum.ifPresent(System.out::println);

        // Product
        OptionalInt product = IntStream.range(1, 10).reduce((a, b) -> a * b);
        product.ifPresent(System.out::println);

        // Maximum
        OptionalInt max = IntStream.range(0, 100).reduce(Integer::max);
        max.ifPresent(System.out::println);

        // Using identity (initial value)
        int reduced = IntStream.range(0, 100).reduce(10, Integer::sum);
        System.out.println(reduced); // Identiy 10 + sum 4950 = 4960
    }
}
```

#### Matching

Check if elements satisfy a condition (short-circuiting):

- `allMatch(Predicate)`: True if ALL satisfy.
- `anyMatch(Predicate)`: True if ANY satisfy.
- `noneMatch(Predicate)`: True if NONE satisfy.

Example:

```java
import java.util.stream.Stream;

public class MatchExample {

    public static void main(String[] args) {
        boolean allEven = Stream.of(1, 2, 3, 4, 5).allMatch(n -> n % 2 == 0);
        boolean anyEven = Stream.of(1, 2, 3, 4, 5).anyMatch(n -> n % 2 == 0);
        boolean noneMatch = Stream.of(1, 2, 3, 4, 5).noneMatch(n -> n > 10);
        System.out.println("allMatch: " + allEven);
        System.out.println("anyMatch: " + anyEven);
        System.out.println("noneMatch: " + noneMatch);
    }
}
```

#### Finding

Retrieve specific elements:

- `findFirst()`: Finds first satisfying element (best for sequential).
- `findAny()`: Finds any satisfying element (best for parallel).

#### Statistics

- `count()`: Count elements.
- `max(Comparator)` / `min(Comparator)`: Find max/min.

For numeric streams (IntStream, LongStream, DoubleStream):
- `average()`: Mean value.
- `sum()`: Sum of elements.
- `max()` / `min()` without Comparator.

Example:

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
numbers.stream().mapToInt(Integer::intValue).average().ifPresent(System.out::println);
System.out.println(numbers.stream().mapToInt(Integer::intValue).sum());
```

### Summary

Functional programming has profoundly influenced Java's paradigm. Before the Stream API, processing collections required verbose `for` loops, conditions, and auxiliary variables—code that was often complex and hard to maintain. Stream API enables data processing in a functional way, enhancing code conciseness, readability, and maintainability. As functional programming gains popularity, Java will likely continue to introduce more features in this direction to improve the developer experience. Its future remains full of potential.
