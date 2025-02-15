+++
date = '2023-05-24T14:15:08+08:00'
draft = false
title = 'Java 泛型的理解和应用'
tags = ["Java"]

+++


### 概述

泛型是一种将类型参数化的动态机制，使用得到的话，可以从以下的方面提升的你的程序：

1. 安全性：使用泛型可以使代码更加安全可靠，因为泛型提供了编译时的类型检查，使得编译器能够在编译阶段捕捉到类型错误。通过在编译时检查类型一致性，可以避免在运行时出现类型转换错误和 `ClassCastException` 等异常。减少由于类型错误引发的bug。
2. 复用和灵活性：泛型可以使用占位符 `<T>` 定义抽象和通用的对象，你可以在使用的时候再来决定具体的类型是什么，从而使得代码更具通用性和可重用性。
3. 简化代码，增强可读性：可以减少类型转换的需求，简化代码，可以使代码更加清晰和易于理解。通过使用具有描述性的泛型类型参数，可以更准确地表达代码的意图，还可以避免使用原始类型或Object类型，从而提供更多的类型信息，使代码更加具有表达力

这就是泛型的概念，是 Java 后期的重大变化之一。泛型实现了参数化类型，可以适用于多种类型。泛型为 Java 的动态类型机制提供很好的补充，但是 Java 的泛型本质上是一种高级语法糖，也存在类型擦除导致的信息丢失等多种缺点，我们可以在本篇文章中深度探讨和分析。



### 简单的示例

泛型在 Java 的主要作用就是创建类型通用的集合类，我们创建一个容器类，然后通过三个示例来展示泛型的使用：

1. 没有使用泛型的情况
2. 使用 Object 类型作为容器对象
3. 使用泛型作为容器对象

示例1：没有使用泛型的情况

```java
public class IntList {

    private int[] arr;		// 只能存储整数类型的数据
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

        int value = list.get(1);  // 需要显式进行类型转换
        System.out.println(value);  // 输出: 2
    }
}
```

在上述示例中，使用了一个明确的 `int` 类型存储整数的列表类 `IntList`，但是该类只能存储整数类型的数据。如果想要存储其他类型的数据，就需要编写类似的类，导致类的复用度较低。

示例2：使用 Object 类型作为持有对象的容器

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
        // 示例使用
        ObjectList list = new ObjectList();
        list.add(1);
        list.add("Hello");
        list.add(true);

        int intValue = (int) list.get(0);  // 需要显式进行类型转换
        String stringValue = (String) list.get(1);  // 需要显式进行类型转换
        boolean boolValue = (boolean) list.get(2);  // 需要显式进行类型转换
    }
}
```

在上述示例中，使用了一个通用的列表类 `ObjectList`，它使用了 Object 类型作为持有对象的容器。当从列表中取出对象时，需要显式进行类型转换，而且不小心类型转换错误程序就会抛出异常，这会带来代码的冗余、安全和可读性的降低。

示例3：使用泛型实现通用列表类

```java
public class GenericList<T> {

    private T[] arr;
    private int size;

    public GenericList() {
        arr = (T[]) new Object[10];  // 创建泛型数组的方式
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
        // 存储 Integer 类型的 List
        GenericList<Integer> intList = new GenericList<>();
        intList.add(1);
        intList.add(2);
        intList.add(3);

        int value = intList.get(1);  // 不需要进行类型转换
        System.out.println(value);  // 输出: 2

        // 存储 String 类型的 List
        GenericList<String> stringList = new GenericList<>();
        stringList.add("Hello");
        stringList.add("World");

        String str = stringList.get(0); // 不需要进行类型转换
        System.out.println(str); // 输出: Hello
    }
}
```

在上述示例中，使用了一个通用的列表类 `GenericList`，通过使用泛型类型参数 `T`，可以在创建对象时指定具体的类型。这样就可以在存储和取出数据时，不需要进行类型转换，代码更加通用、简洁和类型安全。

通过上述三个示例，可以清楚地看到泛型在提高代码复用度、简化类型转换和提供类型安全方面的作用。使用泛型可以使代码更具通用性和可读性，减少类型错误的发生，并且提高代码的可维护性和可靠性。



### 组合类型：元组

在某些情况下需要组合多个不同类型的值的需求，而不希望为每种组合创建专门的类或数据结构。这就需要用到元组（Tuple）。

元组（Tuple）是指将一组不同类型的值组合在一起的数据结构。它可以包含多个元素，每个元素可以是不同的类型。元组提供了一种简单的方式来表示和操作多个值，而不需要创建专门的类或数据结构。

下面是一个使用元组的简单示例：

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

在上述示例中，定义了一个简单的元组类 `Tuple`，它有两个类型参数 `T1` 和 `T2`，以及相应的 `first` 和 `second` 字段。在 `main` 方法中，使用元组存储了不同类型的值，并通过调用 `getFirst` 和 `getSecond` 方法获取其中的值。

你也们可以利用继承机制实现长度更长的元组：

```java
public class Tuple2<T1, T2, T3> extends Tuple<T1, T2>{

    private T3 t3;

    public Tuple2(T1 first, T2 second, T3 t3) {
        super(first, second);
        this.t3 = t3;
    }
}
```

继续扩展：

```java
public class Tuple3<T1, T2, T3, T4> extends Tuple2<T1, T2, T3> {

    private T4 t4;

    public Tuple3(T1 first, T2 second, T3 t3) {
        super(first, second, t3);
    }
}
```

如上所述，元组提供了一种简洁而灵活的方式来组合和操作多个值，适用于需要临时存储和传递多个相关值的场景。但需要注意的是，元组并不具备类型安全的特性，因为它允许不同类型的值的组合。



### 泛型接口

将泛型应用在接口，是在接口设计时常常需要考虑的，泛型可以提供接口的复用性和安全性。

下面是一个示例，展示泛型在接口上的使用：

```java
// 定义一个泛型接口
interface Container<T> {
    void add(T item);
    T get(int index);
}

// 实现泛型接口
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
		// 示例使用
        Container<String> container = new ListContainer<>();
        container.add("Apple");
        container.add("Banana");
        container.add("Orange");

        String fruit1 = container.get(0);
        String fruit2 = container.get(1);
        String fruit3 = container.get(2);

        System.out.println(fruit1);  // 输出: Apple
        System.out.println(fruit2);  // 输出: Banana
        System.out.println(fruit3);  // 输出: Orange
    }
}
```

在上述示例中，我们定义了一个泛型接口 `Container<T>`，它包含了两个方法：`add` 用于添加元素，`get` 用于获取指定位置的元素。然后，我们通过实现泛型接口的类 `ListContainer<T>`，实现了具体的容器类，这里使用了 `ArrayList` 来存储元素。在示例使用部分，我们创建了一个 `ListContainer<String>` 的实例，即容器中的元素类型为 `String`。我们可以使用 `add` 方法添加元素，使用 `get` 方法获取指定位置的元素。

通过在接口上使用泛型，我们可以定义出具有不同类型的容器类，提高代码的可复用性和类型安全性。泛型接口允许我们在编译时进行类型检查，并提供了更好的类型约束和编码规范。



### 泛型方法

泛型方法是一种在方法声明中使用泛型类型参数的特殊方法。它允许在方法中使用参数或返回值的类型参数化，从而实现方法在不同类型上的重用和类型安全性。

泛型方法具有以下特点：

1. 泛型方法可以在方法签名中声明一个或多个类型参数，使用尖括号 `<T>` 来表示
2. 类型参数可以在方法内部用作方法参数类型、方法返回值类型、局部变量类型

方法泛型化要比将整个类泛型化更清晰易懂，所以在日常使用中请尽可能的使用泛型方法。

以下展示泛型方法的示例：

```java
public class GenericMethodExample {
    // 带返回值的泛型方法
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

可以看到通过泛型方法，让 `getFirstElement()` 更具备通用性，无需为每个不同的类型编写单独的获取方法。

再来看一个带可变参数的泛型方法：

```java
public class GenericMethodExample {
    // 带返回值的泛型方法，接受变长参数列表
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

        System.out.println("String List: " + stringList);    // 输出: String List: [Apple, Banana, Orange]
        System.out.println("Integer List: " + intList);      // 输出: Integer List: [1, 2, 3, 4, 5]
    }
}
```



### 泛型信息的擦除

当你深入了解泛型的时候，你会发现它没有你想象的那么安全，它只是编译过程的语法糖，因为泛型并不是 Java 语言的特性，而是后期加入的功能特性，属于编译器层面的功能，而且由于要兼容旧版本的缘故，**所以 Java 无法实现真正的泛型。**

> 泛型擦除是指在编译时期，泛型类型参数会被擦除或替换为它们的上界或限定类型。这是由于Java中的泛型是通过类型擦除来实现的，编译器在生成字节码时会将泛型信息擦除，以确保与旧版本的Java代码兼容。

以下是一个代码示例，展示了泛型擦除的效果：

```java
public class GenericErasureExample {

    public static void main(String[] args) {
        // 定义一个 String 类型的集合
        List<String> stringList = new ArrayList<>();
        stringList.add("Hello");
        stringList.add("World");

        // 定义一个 Integer 类型的集合
        List<Integer> intList = new ArrayList<>();
        intList.add(10);
        intList.add(20);

        // 你无法通过反射获取泛型的类型参数，因为泛型信息会在编译时被擦除
        System.out.println(stringList.getClass());   // 输出: class java.util.ArrayList
        System.out.println(intList.getClass());      // 输出: class java.util.ArrayList

        // 原本不同的类型，输出结果却相等
        System.out.println(stringList.getClass() == intList.getClass());    // 输出: true

        // 使用原始类型List，可以绕过编译器的类型检查，但会导致类型转换错误
        List rawList = stringList;
        rawList.add(30); // 添加了一个整数，导致类型转换错误

        // 从rawList中取出元素时，会导致类型转换错误
        String str = stringList.get(0);  // 类型转换错误，尝试将整数转换为字符串
    }
}
```

通过上述代码，我们演示类的泛型信息是怎么被擦除的，并且演示由于泛型信息的擦除所导致的安全和转换错误。这也是为什么在泛型中无法直接使用基本类型（如 int、boolean 等），而只能使用其包装类的原因之一。



#### 为什么要擦除 ？

Java 在设计泛型时选择了擦除泛型信息的方式，主要是为了保持与现有的非泛型代码的兼容性，并且提供平滑的过渡。泛型是在 Java 5 中引入的，泛型类型参数被替换为它们的上界或限定类型，这样可以确保旧版本的 Java 虚拟机仍然可以加载和执行这些类。

尽管泛型擦除带来了一些限制，如无法在运行时获取泛型类型参数的具体类型等，但通过类型通配符、反射和其他技术，仍然可以在一定程度上处理泛型类型的信息。擦除泛型信息是 Java 泛型的设计妥协，为了在保持向后兼容性和类型安全性的同时，提供了一种灵活且高效的泛型机制。



#### 擦除会引发哪些问题 ？

设计的本质就是权衡，Java 设计者为了兼容性不得已选择的擦除泛型信息的方式，虽然完成了对历史版本的兼容，但付出的代价也是显著的，擦除泛型信息对于 Java 代码可能引发以下问题：

1. 无法在运行时获取泛型类型参数的具体类型：由于擦除泛型信息，无法在运行时获取泛型类型参数的具体类型。（如上所示）
2. 类型转换和类型安全性：擦除泛型信息可能导致类型转换错误和类型安全性问题。（如上所示）
3. 无法创建具体的泛型类型实例：由于擦除泛型信息，无法直接创建具体的泛型类型的实例。例如，无法使用 `new T()` 的方式
4. 与原始类型的混淆：擦除泛型信息可能导致与原始类型的混淆。并且泛型无法使用基本数据类型，只能依赖自动拆箱和装箱机制



#### Class 信息丢失

这是一段因为擦除导致没有任何意义的代码：

```java
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

输出结果：

```sh
[null, null, null, null, null, null, null, null, null, null]
```



### 泛型边界

泛型边界（bounds）是指对泛型类型参数进行限定，以指定其可以接受的类型范围。泛型边界可以通过指定上界（extends）或下界（super）来实现。泛型边界允许我们在泛型代码中对类型参数进行限制，它们有助于确保在使用泛型类或方法时，只能使用符合条件的类型。

泛型边界的使用场景包括：

1. 类型限定：当我们希望泛型类型参数只能是特定类型或特定类型的子类时，可以使用泛型边界。
2. 调用特定类型的方法：通过泛型边界，我们可以在泛型类或方法中调用特定类型的方法，访问其特定的属性。
3. 扩展泛型类型的功能：通过泛型边界，我们可以限制泛型类型参数的范围，以扩展泛型类型的功能。



#### 上界（extends）

用于设定泛型类型参数的上界，即，类型参数必须是特定类型或该类型的子类，示例

```java
public class MyExtendsClass<T extends Number> {
    
    public static void main(String[] args) {
        MyExtendsClass<Integer> integerMyExtendsClass = new MyExtendsClass<>();  // 可以，因为 Integer 是 Number 的子类
        MyExtendsClass<Double> doubleMyExtendsClass = new MyExtendsClass<>();   // 可以，因为 Double 是 Number 的子类
//        MyClass<String> myStringClass = new MyClass<>(); // 编译错误，因为 String 不是 Number 的子类
    }
}
```

在泛型方法中，`extends` 关键字在泛型的读取模式（Producer Extends，PE）中常用到。比如，一个方法返回的是 `List<? extends Number>`，你可以确定这个 List 中的元素都是 Number 或其子类，可以安全地读取为 Number，但不能向其中添加任何元素（除了 null），示例：

```java
public void doSomething(List<? extends Number> list) {
    Number number = list.get(0); // 可以读取
//        list.add(3); // 编译错误，不能写入
}
```



#### 下界（super）

用于设定类型参数的下界，即，类型参数必须是特定类型或该类型的子类。示例：

```java
    public void addToMyList(List<? super Number> list) {
        Object o1 = new Object();
        list.add(3);  // 可以，因为 Integer 是 Number 的子类
        list.add(3.14); // 可以，因为 Double 是 Number 的子类
//      list.add("String");     // 编译错误，因为 String 不是 Number 的子类
    }
```

在泛型方法中，`super` 关键字在泛型的写入模式（Consumer Super，CS）中常用到。比如，一个方法参数的类型是 `List<? super Integer>`，你可以向这个 List 中添加 Integer 或其子类的对象，但不能从中读取具体类型的元素（只能读取为 Object），示例：

```java
public void doSomething(List<? super Integer> list) {
    list.add(3);        // 类型符合，可以写入
//  Integer number = list.get(0);     // 编译错误，不能读取具体类型
    Object o = list.get(0);     // 可以读取 Object
}
```

熟练和灵活的运用 `PECS` 原则（Producer Extends, Consumer Super）我们也可以轻松实现 Collection 里面的通用类型集合的 Copy 方法，示例：

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

记住，无论是 `extends` 还是 `super`，它们都只是对编译时类型的约束，实际的运行时类型信息在类型擦除过程中已经被删除了。



#### 无界（?）

无界通配符 `<?>` 是一种特殊的类型参数，可以接受任何类型。它常被用在泛型代码中，当代码可以工作在不同类型的对象上，并且你可能不知道或者不关心具体的类型是什么。你可以使用它，示例：

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

那么，问题来了。

那我为什么不直接使用  Object ？ 而要使用 <?> 无界通配符 ？

它们好像都可以容纳任何类型的对象。但实际上，`List<Object>` 和 `List<?>` 在类型安全性上有很大的不同。

例如，`List<Object>` 是一个具体类型，你可以向 `List<Object>` 中添加任何类型的对象。但是，`List<Object>` 不能接受其他类型的 `List`，例如 `List<String>` 或 `List<Integer>`。

相比之下，`List<?>` 是一个通配符类型，表示可以是任何类型的 `List`。你不能向 `List<?>` 中添加任何元素（除了 `null`），因为你并不知道具体的类型，但你可以接受任何类型的 `List`，包括 `List<Object>`、`List<String>`、`List<Integer>` 等等。

示例代码：

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

    printListWildcard(stringList); // 有效
    // printListObject(stringList); // 编译错误
}
```

因此，当你需要编写能接受任何类型 `List` 的代码时，应该使用 `List<?>` 而不是 `List<Object>`



### 目前存在的问题

在 Java 引入泛型之前，已经有大量的 Java 代码在生产环境中运行。为了让这些代码在新版本的 Java 中仍然可以运行，Java 的设计者选择了一种叫做 **“类型擦除”** 的方式来实现泛型，这样就不需要改变 `JVM` 和已存在的非泛型代码。

但这样的设计解决了向后兼容的问题，但也引入很多问题需要大多数的 Java 程序员来承担，例如：

1. **类型擦除**：这是Java泛型中最主要的限制。这意味着在运行时你不能查询一个泛型对象的真实类型
2. **不能实例化泛型类型的类**：你不能使用 `new T()`，`new E()`这样的语法来创建泛型类型的对象，还是因为类型被擦除
3. **不能使用基本类型作为类型参数**：因为是编译器的语法糖，所以只能使用包装类型如 `Integer`，`Double` 等作为泛型类型参数
4. **通配符的使用可能会导致代码复杂**：如 `? extends T` 和 `? super T` 在理解和应用时需要小心
5. **因为类型擦除，泛型类不能继承自或者实现同一泛型接口的不同参数化形式**

尽管 Java 的泛型有这些缺点，但是它仍然是一个强大和有用的工具，可以帮助我们编写更安全、更易读的代码。



### 总结

在泛型出现之前，集合类库并不能在编译时期检查插入集合的对象类型是否正确，只能在运行时期进行检查，这种情况下一旦出错就会在运行时抛出一个类型转换异常。这种运行时错误的出现对于开发者而言，既不友好，也难以定位问题。泛型的引入，让开发者可以在编译时期检查类型，增加了代码的安全性。并且可以编写更为通用的代码，提高了代码的复用性。

然而，泛型设计并非完美，主要的问题出在类型擦除上，为了保持与老版本的兼容性所做的妥协。因为类型擦除，Java 的泛型丧失了一些强大的功能，例如运行时类型查询，创建泛型数组等。

尽管 Java 泛型存在一些限制，但是 Java 语言仍然在不断的发展中，例如在 Java 10 中，引入了局部变量类型推断的特性，使得在使用泛型时可以更加方便。对于未来，Java 可能会在泛型方面进行更深入的改进。