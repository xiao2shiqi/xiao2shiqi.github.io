+++
date = '2023-05-24T14:15:08+08:00'
draft = false
title = 'Understanding and Applying Java Generics'
tags = ["Java"]
+++


### Overview

Generics are a dynamic mechanism for parameterizing types. When used correctly, they can improve your program in the following ways:

1. **Safety**: Using generics makes code safer and more reliable because they provide compile-time type checking. This allows the compiler to catch type errors during the compilation phase. By checking type consistency at compile-time, you can avoid runtime type conversion errors and internal exceptions like `ClassCastException`, reducing bugs caused by type errors.
2. **Reusability and Flexibility**: Generics allow the use of placeholders like `<T>` to define abstract and general objects. You can decide the specific type at the time of use, making the code more versatile and reusable.
3. **Simplified Code and Enhanced Readability**: Generics reduce the need for explicit type casting, simplifying the code and making it clearer and easier to understand. By using descriptive generic type parameters, you can more accurately express the intent of the code. They also help avoid raw types or `Object` types, providing more type information and making the code more expressive.

This is the concept of Generics—one of the major changes introduced in later versions of Java. Generics implement parameterized types that can work across multiple types. While they provide an excellent supplement to Java's dynamic type mechanism, Java generics are essentially a high-level "syntax sugar." They also have several drawbacks, such as information loss due to type erasure, which we will explore and analyze in depth in this article.

### Simple Examples

The primary role of generics in Java is creating type-generic collection classes. Let's create a container class and use three examples to demonstrate the use of generics:

1. Without generics.
2. Using the `Object` type as the container object.
3. Using generics as the container object.

**Example 1: Without generics**

```java
public class IntList {

    private int[] arr;		// Can only store integer types
    private int size;

    public IntList() {
        arr = new int[10];
        size = 0;
    }

    public void add(int value) {
        arr[size++] = value;
    }

    public int get(int index) {
        return arr[index];
    }

    public int size() {
        return size;
    }

    public static void main(String[] args) {
        IntList list = new IntList();

        list.add(1);
        list.add(2);
        list.add(3);

        int value = list.get(1);  // No casting needed because type is fixed
        System.out.println(value);  // Output: 2
    }
}
```

In the above example, a list class `IntList` specifically for the `int` type is used, but this class can only store integers. To store other types, you would need to write similar classes, leading to low code reusability.

**Example 2: Using the `Object` type as a container for holding objects**

```java
public class ObjectList {
    private Object[] arr;
    private int size;

    public ObjectList() {
        arr = new Object[10];
        size = 0;
    }

    public void add(Object value) {
        arr[size++] = value;
    }

    public Object get(int index) {
        return arr[index];
    }

    public int size() {
        return size;
    }

    public static void main(String[] args) {
        // Example usage
        ObjectList list = new ObjectList();
        list.add(1);
        list.add("Hello");
        list.add(true);

        int intValue = (int) list.get(0);  // Requires explicit type casting
        String stringValue = (String) list.get(1);  // Requires explicit type casting
        boolean boolValue = (boolean) list.get(2);  // Requires explicit type casting
    }
}
```

In this example, a general `ObjectList` class is used, which uses the `Object` type as the container. When retrieving an object from the list, explicit type casting is required. Accidental casting errors will cause the program to throw exceptions, leading to code redundancy and reduced safety and readability.

**Example 3: Using generics to implement a general list class**

```java
public class GenericList<T> {

    private T[] arr;
    private int size;

    public GenericList() {
        arr = (T[]) new Object[10];  // Way to create a generic array
        size = 0;
    }

    public void add(T value) {
        arr[size++] = value;
    }

    public T get(int index) {
        return arr[index];
    }

    public int size() {
        return size;
    }

    public static void main(String[] args) {
        // List storing Integer type
        GenericList<Integer> intList = new GenericList<>();
        intList.add(1);
        intList.add(2);
        intList.add(3);

        int value = intList.get(1);  // No casting needed
        System.out.println(value);  // Output: 2

        // List storing String type
        GenericList<String> stringList = new GenericList<>();
        stringList.add("Hello");
        stringList.add("World");

        String str = stringList.get(0); // No casting needed
        System.out.println(str); // Output: Hello
    }
}
```

In this example, the `GenericList` class uses a generic type parameter `T`, allowing the specific type to be specified upon object creation. This eliminates the need for type casting when storing and retrieving data, making the code more versatile, concise, and type-safe.

These three examples clearly demonstrate the role of generics in increasing code reuse, simplifying type casting, and providing type safety. Using generics makes code more universal and readable, reduces type errors, and improves maintainability and reliability.

### Composite Type: Tuple

In some cases, you may need to combine multiple values of different types without creating dedicated classes or data structures for every combination. This is where Tuples come in.

A Tuple refers to a data structure that groups a set of values of different types together. It can contain multiple elements, each of a different type. Tuples provide a simple way to represent and operate on multiple values without creating specific classes.

Here is a simple example using a Tuple:

```java
class Tuple<T1, T2> {
    private T1 first;
    private T2 second;

    public Tuple(T1 first, T2 second) {
        this.first = first;
        this.second = second;
    }

    public T1 getFirst() {
        return first;
    }

    public T2 getSecond() {
        return second;
    }
}

public class TupleExample {

    public static void main(String[] args) {
        Tuple<String, Integer> person = new Tuple<>("Tom", 18);
        System.out.println("Name: " + person.getFirst());
        System.out.println("Age: " + person.getSecond());

        Tuple<String, Double> product = new Tuple<>("Apple", 2.99);
        System.out.println("Product: " + product.getFirst());
        System.out.println("Price: " + product.getSecond());
    }
}
```

In the above example, a simple `Tuple` class is defined with two type parameters `T1` and `T2`, along with corresponding `first` and `second` fields. In the `main` method, tuples are used to store values of different types, and values are retrieved using `getFirst` and `getSecond`.

You can also use inheritance to implement longer Tuples:

```java
public class Tuple2<T1, T2, T3> extends Tuple<T1, T2>{

    private T3 t3;

    public Tuple2(T1 first, T2 second, T3 t3) {
        super(first, second);
        this.t3 = t3;
    }
}
```

Continuing to expand:

```java
public class Tuple3<T1, T2, T3, T4> extends Tuple2<T1, T2, T3> {

    private T4 t4;

    public Tuple3(T1 first, T2 second, T3 t3, T4 t4) {
        super(first, second, t3);
        this.t4 = t4;
    }
}
```

As shown, tuples offer a concise and flexible way to group and operate on multiple values, suitable for scenarios requiring temporary storage and passing related values. Note, however, that tuples themselves don't provide inherent semantic type safety because they allow any combination of types.

### Generic Interfaces

Applying generics to interfaces is a common consideration in interface design, as generics can improve reusability and safety.

Here is an example showing the use of generics on an interface:

```java
// Define a generic interface
interface Container<T> {
    void add(T item);
    T get(int index);
}

// Implement the generic interface
public class ListContainer<T> implements Container<T> {

    private List<T> list;

    public ListContainer() {
        this.list = new ArrayList<>();
    }

    @Override
    public void add(T item) {
        list.add(item);
    }

    @Override
    public T get(int index) {
        return list.get(index);
    }

    public static void main(String[] args) {
		// Example usage
        Container<String> container = new ListContainer<>();
        container.add("Apple");
        container.add("Banana");
        container.add("Orange");

        String fruit1 = container.get(0);
        String fruit2 = container.get(1);
        String fruit3 = container.get(2);

        System.out.println(fruit1);  // Output: Apple
        System.out.println(fruit2);  // Output: Banana
        System.out.println(fruit3);  // Output: Orange
    }
}
```

In this example, we define a generic interface `Container<T>` with two methods: `add` for adding elements and `get` for retrieving an element at a specific index. Then, the `ListContainer<T>` class implements this generic interface using an `ArrayList` to store elements. In the usage part, we create a `ListContainer<String>` instance. We can then use `add` to add strings and `get` to retrieve them.

By using generics on interfaces, we can define container classes of various types, improving code reusability and type safety. Generic interfaces allow for compile-time type checking and provide better type constraints and coding standards.

### Generic Methods

A generic method is a special method that uses generic type parameters in its declaration. It allows for parameterizing the types of arguments or return values, enabling the method to be reused across different types while maintaining type safety.

Generic methods have these characteristics:
1. They can declare one or more type parameters in the method signature using angle brackets `<T>`.
2. Type parameters can be used internally as parameter types, return types, or local variable types.

Generic methods are often clearer and more understandable than making the entire class generic. Therefore, you should use generic methods as much as possible in your daily development.

Here is an example of a generic method:

```java
public class GenericMethodExample {
    // Generic method with a return value
    public static <T> T getFirstElement(T[] array) {
        if (array != null && array.length > 0) {
            return array[0];
        }
        return null;
    }

    public static void main(String[] args) {
        Integer[] intArray = {1, 2, 3, 4, 5};
        String[] strings = {"Hello", "World"};

        System.out.println("First element in intArray: " + getFirstElement(intArray));
        System.out.println("First element in strings: " + getFirstElement(strings));
    }
}
```

The generic method makes `getFirstElement()` versatile, eliminating the need to write separate retrieval methods for every type.

Next, let's look at a generic method with variable arguments (varargs):

```java
public class GenericMethodExample {
    // Generic method with return value, accepting a variable argument list
    public static <T> List<T> createList(T... elements) {
        List<T> list = new ArrayList<>();
        for (T element : elements) {
            list.add(element);
        }
        return list;
    }

    public static void main(String[] args) {
        List<String> stringList = createList("Apple", "Banana", "Orange");
        List<Integer> intList = createList(1, 2, 3, 4, 5);

        System.out.println("String List: " + stringList);    // Output: String List: [Apple, Banana, Orange]
        System.out.println("Integer List: " + intList);      // Output: Integer List: [1, 2, 3, 4, 5]
    }
}
```

### Type Erasure

As you delve deeper into generics, you will find they are not as safe as you might imagine. They are essentially syntax sugar for the compilation process. This is because generics are not an inherent feature of the Java language itself but a feature added later at the compiler level. Because of the need for backward compatibility, **Java cannot implement true generics.**

> Type erasure refers to the process where generic type parameters are erased or replaced with their upper bounds or bound types during compilation. Java implements generics through type erasure; the compiler erases generic information when generating bytecode to ensure compatibility with older versions of Java code.

Here is a code example demonstrating the effect of type erasure:

```java
public class GenericErasureExample {

    public static void main(String[] args) {
        // Define a collection of String type
        List<String> stringList = new ArrayList<>();
        stringList.add("Hello");
        stringList.add("World");

        // Define a collection of Integer type
        List<Integer> intList = new ArrayList<>();
        intList.add(10);
        intList.add(20);

        // You cannot retrieve generic type parameters via reflection because they are erased during compilation
        System.out.println(stringList.getClass());   // Output: class java.util.ArrayList
        System.out.println(intList.getClass());      // Output: class java.util.ArrayList

        // Originally different types, yet the output shows they are equal
        System.out.println(stringList.getClass() == intList.getClass());    // Output: true

        // Using a raw List can bypass compiler type checks but will lead to type casting errors
        List rawList = stringList;
        rawList.add(30); // Adding an integer, which will cause a type casting error later

        // Retrieving an element from rawList can cause a type casting error
        // The following might throw ClassCastException at runtime depending on how it's used
        // String str = stringList.get(0);  
    }
}
```

The above code demonstrates how generic information is erased and shows the potential safety and casting errors caused by erasure. This is also one of the reasons why primitive types (like `int`, `boolean`, etc.) cannot be used directly in generics; only their wrapper classes can be used.

#### Why Erase?

Java chose to erase generic information primarily to maintain compatibility with existing non-generic code and to provide a smooth transition. Generics were introduced in Java 5. By replacing generic type parameters with their upper bounds or bounded types, Java ensured that older versions of the Java Virtual Machine could still load and execute these classes.

While type erasure introduces limitations—such as the inability to retrieve the specific type of generic parameters at runtime—it is still possible to handle generic information to some extent using type wildcards, reflection, and other techniques. Erasing generic information was a design compromise in Java generics to provide a flexible and efficient mechanism while maintaining backward compatibility and type safety.

#### What Problems Does Erasure Cause?

The essence of design is trade-off. To maintain compatibility, Java designers chose to erase generic information, but at a significant cost. Erasure can lead to the following issues in Java code:

1. **Inability to retrieve specific generic type parameters at runtime**: As shown above, you cannot know the specific type of a generic parameter during execution.
2. **Casting and Type Safety**: Erasing generic info can lead to casting errors and type safety concerns.
3. **Inability to create instances of generic types**: Because info is erased, you cannot directly instantiate a generic type. For example, `new T()` is not allowed.
4. **Confusion with raw types**: Erasure can lead to confusion with raw types. Furthermore, generics cannot use primitive data types, relying instead on auto-boxing and unboxing mechanisms.

#### Loss of Class Information

Here is a piece of code that demonstrates how erasure makes certain logic meaningless:

```java
import java.util.Arrays;

public class ArrayMaker<T> {

    private Class<T> kind;

    public ArrayMaker(Class<T> kind) {
        this.kind = kind;
    }

    @SuppressWarnings("unchecked")
    T[] create(int size) {
        return (T[]) java.lang.reflect.Array.newInstance(kind, size);
    }

    public static void main(String[] args) {
        ArrayMaker<String> stringMaker = new ArrayMaker<>(String.class);
        String[] stringArray = stringMaker.create(10);
        System.out.println(Arrays.toString(stringArray));
    }
}
```

Output:

```sh
[null, null, null, null, null, null, null, null, null, null]
```

### Generic Bounds

Generic bounds refer to the limits placed on generic type parameters to specify the range of acceptable types. Bounds can be set using upper bounds (`extends`) or lower bounds (`super`). They allow us to restrict type parameters in generic code, ensuring that only compliant types are used with generic classes or methods.

Scenarios for using generic bounds include:
1. **Type Constraints**: When you want a generic type parameter to be a specific type or a subclass of that type.
2. **Calling methods of a specific type**: Through bounds, you can call methods or access attributes of a specific type within generic classes or methods.
3. **Extending generic functionality**: Bounds allow you to limit the scope of type parameters to extend the capabilities of the generic type.

#### Upper Bound (extends)

Used to set the upper limit for a generic type parameter, meaning the type must be the specified type or its subclass.

```java
public class MyExtendsClass<T extends Number> {
    
    public static void main(String[] args) {
        MyExtendsClass<Integer> integerClass = new MyExtendsClass<>();  // OK, Integer is a subclass of Number
        MyExtendsClass<Double> doubleClass = new MyExtendsClass<>();    // OK, Double is a subclass of Number
        // MyClass<String> stringClass = new MyClass<>(); // Compile error, String is not a subclass of Number
    }
}
```

In generic methods, the `extends` keyword is commonly used in the reading pattern (Producer Extends, PE). For instance, if a method returns `List<? extends Number>`, you are certain that every element in the list is a `Number` or its subclass. You can safely read them as `Number`, but you cannot add any elements (except `null`) to it.

```java
public void doSomething(List<? extends Number> list) {
    Number number = list.get(0); // Can read
    // list.add(3); // Compile error, cannot write
}
```

#### Lower Bound (super)

Used to set the lower limit for a type parameter, meaning the type must be the specified type or its superclass.

```java
    public void addToMyList(List<? super Number> list) {
        list.add(3);      // OK, Integer is a subclass of Number
        list.add(3.14);   // OK, Double is a subclass of Number
        // list.add("String"); // Compile error, String is not a superclass or a subclass of Number
    }
```

In generic methods, the `super` keyword is often used in the writing pattern (Consumer Super, CS). For instance, with a method parameter like `List<? super Integer>`, you can add `Integer` or its subclasses to the list, but you cannot retrieve elements as a specific type (only as `Object`).

```java
public void doSomething(List<? super Integer> list) {
    list.add(3);        // Matches type, can write
    // Integer number = list.get(0);     // Compile error, cannot read as specific type
    Object o = list.get(0);     // Can read as Object
}
```

By proficiently applying the `PECS` principle (Producer Extends, Consumer Super), we can easily implement a general `copy` method for collections, similar to one in the `Collections` utility class:

```java
public static <T> void copy(List<? super T> dest, List<? extends T> src) {
    for (T t : src) {
        dest.add(t);
    }
}

public static void main(String[] args) {
    List<Object> objectList = new ArrayList<>();
    List<Integer> integerList = Arrays.asList(1, 2, 3);

    copy(objectList, integerList);

    System.out.println(objectList);     // [1, 2, 3]
}
```

Remember, both `extends` and `super` are constraints for compile-time types; actual runtime type information is removed during type erasure.

#### Unbounded (?)

The unbounded wildcard `<?>` is a special type parameter that can accept any type. it is often used when code works across different types of objects and you either don't know or don't care what the specific type is.

```java
public static void printList(List<?> list) {
    for (Object elem : list)
        System.out.println(elem + " ");
    System.out.println();
}

public static void main(String[] args) {
    List<Integer> li = Arrays.asList(1, 2, 3, 4, 5);
    List<String> ls = Arrays.asList("one", "two", "three");
    printList(li);
    printList(ls);
}
```

You might ask: why not just use `Object` instead of the `<?>` wildcard?

Both can seemingly hold any type, but `List<Object>` and `List<?>` behave very differently regarding type safety.

`List<Object>` is a concrete type. You can add any type of object to a `List<Object>`, but it CANNOT accept other types of lists like `List<String>` or `List<Integer>`.

In contrast, `List<?>` is a wildcard type representing a list of any type. You cannot add any elements to a `List<?>` (except `null`) because you don't know the specific type, but you can accept any type of list, including `List<Object>`, `List<String>`, `List<Integer>`, etc.

```java
public static void printListObject(List<Object> list) {
    for (Object obj : list)
        System.out.println(obj);
}

public static void printListWildcard(List<?> list) {
    for (Object obj : list)
        System.out.println(obj);
}

public static void main(String[] args) {
    List<String> stringList = Arrays.asList("Hello", "World");

    printListWildcard(stringList); // Valid
    // printListObject(stringList); // Compile error
}
```

Therefore, when you need to write code that can accept any type of `List`, you should use `List<?>` rather than `List<Object>`.

### Current Issues

Before generics were introduced, a massive amount of Java code was already running in production. To allow this code to continue running in newer versions, Java designers chose **"type erasure"** to implement generics, avoiding changes to the `JVM` and existing non-generic code.

While this solved backward compatibility, it introduced issues that most Java programmers must now deal with:

1. **Type Erasure**: The primary limitation. You cannot query the real type of a generic object at runtime.
2. **Cannot Instantiate Generic Classes**: You cannot use syntax like `new T()` or `new E()` due to erasure.
3. **Cannot Use Primitives as Type Parameters**: Since generics are compiler syntax sugar, only wrapper types like `Integer` or `Double` can be used.
4. **Complexity of Wildcards**: Using `? extends T` and `? super T` requires careful understanding and application.
5. **Inheritance Restrictions**: Due to erasure, a generic class cannot inherit from or implement different parameterized versions of the same generic interface.

Despite these drawbacks, Java generics remain a powerful tool helping us write safer, more readable code.

### Summary

Before generics, collection libraries couldn't check the type of objects being inserted at compile time—checks only happened at runtime, leading to type conversion exceptions that were neither user-friendly nor easy to debug. Generics allowed compile-time type checking, increasing security and enabling the creation of more versatile code, thus improving reusability.

However, the design isn't perfect, mainly due to type erasure—a compromise made for backward compatibility. Because of erasure, Java generics lost some powerful features like runtime type querying and generic array creation.

Despite these limitations, the Java language continues to evolve. For example, Java 10 introduced local variable type inference, making the use of generics more convenient. In the future, Java may continue with deeper improvements to its generics system.
