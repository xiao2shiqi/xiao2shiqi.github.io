+++
date = '2023-05-09T14:10:56+08:00'
draft = false
title = 'Java.nio.file 文件库的介绍和使用'
tags = ["Java"]
+++

### 概述

在早期的 Java 版本中，文件 IO 操作功能一直相对较弱，主要存在以下问题：

1.  缺乏对现代文件系统的支持：只提供的基础的文件操作，不支持很多现代的文件系统
1.  API 不够直观：文件操作的 API 设计相对较为复杂和冗长，使用体验感很差
1.  对于大文件处理和并发性能不够：简单的 I/O 模型，没有充分利用现代硬件的性能优势，而且还有很多同步的问题

但 Java 在后期版本中引入了 `java.nio.file` 库来提高 Java 对文件操作的能力。还增加的流的功能，似乎使得文件变成更好用了。所以本章，我们就来主要介绍 `java.nio.file` 中常用的类和模块，大致如下：

1.  Path 路径：Paths 模块和 Path 工具类介绍
1.  Files 文件：File 和 FileSystems 工具类介绍
1.  文件管理服务：WatchService 、PathMatcher 等等文件服务

### Path 路径

`java.nio.file.Paths` 和 `java.nio.file.Path` 类在 Java NIO 文件 I/O 框架中用于处理文件系统路径。以下是对它们的简单介绍：

-   `Paths` 模块：`Paths` 模块提供了一些静态方法来创建 `Path` 对象，`Path` 对象表示文件系统中的路径。例如，可以使用 `Paths.get()` 方法创建一个 `Path` 对象，这个对象表示一个文件路径。
-   `Path` 类：`Path` 类代表一个文件系统中的路径，它提供了一系列的方法来操作文件路径。例如，可以使用 `Path.toAbsolutePath()` 方法获取一个绝对路径，或者使用 `Path.getParent()` 方法获取路径的父路径。

> 关于跨平台：Path 对象可以工作在不同操作系统的不同文件系统之上，它帮我们屏蔽了操作系统之间的差异

以下是一些简单使用场景示例：

```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class PathExample {

    public static void main(String[] args) {
        // 创建一个绝对路径
        Path absolutePath = Paths.get("C:\Users\phoenix\file.txt");     // 这里传入 "example\file.txt" 创建的相对路径
        System.out.println("Absolute path: " + absolutePath);
        // 获取父路径
        System.out.println("Parent path: " + absolutePath.getParent());
        // 获取文件名
        System.out.println("File name: " + absolutePath.getFileName());
        // 获取根路径
        System.out.println("Root path: " + absolutePath.getRoot());
        // 合并路径
        Path resolvePath = Paths.get("C:\Users\phoenix").resolve("file.txt");
        System.out.println("Merged path:" + resolvePath);
    }
}
```

输出结果：

```sh
Absolute path: C:\Users\phoenix\file.txt
Parent path: C:\Users\phoenix
File name: file.txt
Root path: C:\
Merged path:C:\Users\phoenix\file.txt
```

从这里你不仅可以看出关于 `Paths` 和 `Path` 类对于文件路径的一些操作方法的使用，还能看得出我使用的是 `Windows` 操作系统。还有更多的用法可以查看官方的 API 文档，这里就不过多赘述了。

### Files 文件

`java.nio.file.Files` 类是 Java NIO 文件包中的一个实用工具类，它提供了一系列静态方法，可以让你方便地执行文件系统中的各种操作，例如文件的创建、删除、复制、移动、读取和写入等。例如，可以使用 `Files.exists()` 方法检查一个文件是否存在，或者使用 `Files.createDirectory()` 方法创建一个新目录。

以下是一些简单使用场景示例：

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Arrays;
import java.util.List;

public class PathExample {

    public static void main(String[] args) throws IOException {
        Path path = Paths.get("example.txt");
        // 1：检查文件是否存在
        boolean exists = Files.exists(path);
        System.out.println("File exists: " + exists);
        if (!exists) {
            // 2：不存在则创建文件
            Files.createFile(path);
        }
        // 3：复制一个文件
        Path target = Paths.get("example2.txt");
        Files.copy(path, target, StandardCopyOption.REPLACE_EXISTING);
        // 4：创建目录
        Path newDirectory = Paths.get("example");
        Files.createDirectories(newDirectory);
        // 4：移动文件：将 example2.txt 移动到 example 目录下
        Files.move(target, newDirectory.resolve("example2.txt"), StandardCopyOption.REPLACE_EXISTING);
        // 5：删除文件和目录
        Files.delete(newDirectory.resolve("example2.txt"));
        Files.delete(newDirectory);    // 只能删除空目录
        // 6：将字节数组写入文件
        Files.write(path, "Hello World".getBytes());
        // 7：将文本行序列写入文件
        List<String> lines = Arrays.asList("Line 1", "Line 2", "Line 3");
        Files.write(path, lines, StandardCharsets.UTF_8, StandardOpenOption.CREATE);
        // 8：读取文件，并且打印所有行
        Files.readAllLines(path, StandardCharsets.UTF_8).forEach(System.out::println);
    }
}
```

输出结果：

```sh
File exists: true
Line 1
Line 2
Line 3
```

也可以在项目根目录下查看文件：

![image-20230508234504230](https://s2.loli.net/2025/02/15/snRvXz21cLbtyN9.png)

以上代码示例展示了如何使用 `Files` 类进行常见的文件操作。在实际项目中，您可以根据需要组合使用这些方法来满足您的需求。

补充：

Files.delete 函数只能删除空目录，这个设计是有意为之的，因为递归地删除文件和目录可能是一个非常危险的操作，尤其是当您不小心删除了一个包含重要数据的目录时。如果您想删除一个包含子目录和文件的目录，您需要先递归地删除目录中的所有子目录和文件，然后再删除目录本身。可以借助 `Files.walkFileTree` 遍历文件目录，然后调用 `Files.delete` 即可。

### FileSystems 文件系统

`FileSystems` 类提供了一组静态方法来访问和操作默认文件系统（通常是操作系统的本地文件系统）以及其他文件系统实现。以下是一个简单的示例：

```java
public class FileSystemsExample {

    public static void main(String[] args) {
        // 获取默认文件系统
        FileSystem fileSystem = FileSystems.getDefault();
        // 获取文件系统的路径分隔符
        String pathSeparator = fileSystem.getSeparator();
        System.out.println("Path separator: " + pathSeparator);
        // 获取文件系统的根目录
        for (Path root : fileSystem.getRootDirectories()) {
            System.out.println("Root directory: " + root);
        }
        // 使用文件系统创建一个 path 路径对象
        Path path = fileSystem.getPath("path", "to", "file.txt");
        System.out.println(path);
        // 是否只读
        System.out.println("is read only ?: " + fileSystem.isReadOnly());
        // 文件系统的提供者
        System.out.println("provider: " + fileSystem.provider());
    }
}
```

输出结果：

```sh
Path separator: \
Root directory: C:\
path\to\file.txt
is read only ?: false
provider: sun.nio.fs.WindowsFileSystemProvider@5b480cf9
```

`FileSystem` 工具类的方法并不多，可以参考它的 API，但通过 `FileSystem` 可以创建 WatchService 和 PathMatcher 子类

#### WatchService 文件监控

WatchService 是一个文件系统观察者，基于 `FileSystem` 创建，主要用于监控文件系统事件（如创建、修改、删除文件或目录）。它可以帮助我们实时地检测和处理文件系统中的变化。如果你的业务中有需要监控文件变化的场景，你可能会需要用到它，例如：

-   文件上传
-   实时备份
-   热加载配置

以下是一个简单的示例：

```java
import java.io.IOException;
import java.nio.file.*;

public class WatchServiceExample {

    public static void main(String[] args) throws IOException, InterruptedException {
        // 创建 WatchService
        WatchService watchService = FileSystems.getDefault().newWatchService();

        // 注册监听指定的目录
        Path dir = Paths.get("C:\Users\phoenix");
        dir.register(watchService, StandardWatchEventKinds.ENTRY_CREATE, StandardWatchEventKinds.ENTRY_MODIFY, StandardWatchEventKinds.ENTRY_DELETE);

        while (true) {
            // 获取并处理事件
            WatchKey key = watchService.take();
            for (WatchEvent<?> event : key.pollEvents()) {
                System.out.println("Event: " + event.kind() + " - " + event.context());
            }

            // 重置 key，继续监听
            if (!key.reset()) {
                break;
            }
        }
        watchService.close();
    }
}
```

启动以上程序，程序就会监控我当前系统的用户目录，当我在用户目录创建文件并且编辑，删除，程序会输出以下内容：

```sh
Event: ENTRY_CREATE - 新建 文本文档.txt
Event: ENTRY_DELETE - 新建 文本文档.txt
Event: ENTRY_CREATE - helloWorld.txt
Event: ENTRY_MODIFY - helloWorld.txt
Event: ENTRY_MODIFY - helloWorld.txt
Event: ENTRY_MODIFY - helloWorld.txt
Event: ENTRY_DELETE - helloWorld.txt
```

#### PathMatcher 文件匹配

PathMatcher 是一个文件路径匹配接口，它可以帮助我们在遍历文件系统时，根据特定规则过滤出符合条件的文件或目录。它可以使用多种匹配语法（如 glob 和 regex），使得处理文件名或目录名的模式变得更加灵活和高效。PathMatcher 的使用场景包括：

-   文件过滤：在搜索文件时，我们可能需要根据文件名或目录名的模式来过滤结果
-   批量操作：当我们需要对文件系统中的一组文件或目录执行批量操作时，PathMatcher 可以帮助我们找到符合特定规则的文件或目录
-   目录监控：可以结合 WatchService 对目录监控，然后通过 PathMatcher 过滤找出我们想要文件，如：.log 文件的创建，修改等

以下是一个简单示例代码：

```java
import java.io.IOException;
import java.nio.file.*;
import java.util.stream.Stream;

public class PathMatcherExample {

    public static void main(String[] args) throws IOException {
        // 创建 PathMatcher，使用 glob 语法：匹配所有以 .tmp 结尾的文件（临时文件）
        FileSystem fileSystem = FileSystems.getDefault();
        PathMatcher matcher = fileSystem.getPathMatcher("glob:*.tmp");
        // 在指定目录，找到匹配的文件，然后进行删除
        try (Stream<Path> walk = Files.walk(Paths.get("path/to/directory"))) {
            walk.filter(path -> matcher.matches(path.getFileName())).forEach(path -> {
                System.out.println(path.getFileName());
                try {
                    Files.delete(path);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
        }
    }
}
```

上面的示例程序是通过 PathMatcher 匹配 .tmp 结尾的临时文件，然后进行删除的示例，结合 PathMatcher 可以轻松的完成一个清理临时文件的小程序。

### 读文件内容

上面的示例都是操作文件和目录，这里介绍一下如何读文件的内容，为了方便演示读取文件，先在 `path/to/file.txt` 相对目录下创建一个示例文本：

```sh
Java is a high-level programming language.
Python is an interpreted, high-level programming language.
JavaScript is a scripting language for Web development.
C++ is a general-purpose programming language.
Rust is a systems programming language.
```

读文件主要用到 Files 类的两个方法：

1.  `readAllLines()` 方法：一次性加载，主要用于读取小到中等的文件
1.  `lines()` 方法：逐行读取，适用于大文件

#### 小文件

`readAllLines()` 适用于读取小到中等大小的文件，因为它会将整个文件内容加载到内存中，这个方法适用于在读取文件内容后立即处理整个文件的情况。使用示例：

```java
public class LinesExample {

    public static void main(String[] args) throws IOException {
        // 读取全部文件
        List<String> lines = Files.readAllLines(Paths.get("path/to/file.txt"), StandardCharsets.UTF_8);

        // 对文件内容进行处理
        Map<String, Long> wordFrequency = lines.stream()
                .flatMap(line -> Arrays.stream(line.split("\s+")))
                .map(String::toLowerCase)
                .collect(Collectors.groupingBy(word -> word, Collectors.counting()));

        System.out.println("Word Frequency:");
        wordFrequency.forEach((word, count) -> System.out.printf("%s: %d%n", word, count));
    }
}
```

#### 大文件

`lines()` 方法： 使用场景：适用于读取大型文件，因为它不会一次性将整个文件内容加载到内存中。通过使用 Java 8 的 Stream API，可以在读取文件内容时同时处理每一行，从而提高处理效率。使用示例：

```java
public class LinesExample {

    public static void main(String[] args) throws IOException {
        Path filePath = Paths.get("path/to/file.txt");

        // 逐行读取，并且在内容进行处理
        Stream<String> lines = Files.lines(filePath);
        Map<String, Long> wordFrequency = lines
                .skip(3)            // 跳过前 3 行
                .flatMap(line -> Arrays.stream(line.split("\s+")))
                .map(String::toLowerCase)
                .collect(Collectors.groupingBy(word -> word, Collectors.counting()));

        System.out.println("Word Frequency:");
        wordFrequency.forEach((word, count) -> System.out.printf("%s: %d%n", word, count));
        lines.close();
    }
}
```

输出结果：

```sh
Word Frequency:
rust: 1
a: 2
c++: 1
systems: 1
language.: 2
is: 2
programming: 2
general-purpose: 1
```

### 总结

在过去，`java.io` 包主要负责处理文件 I/O。但是它存在一些问题，例如性能不佳、API 不直观、文件元数据操作困难等。为了解决这些问题，后期的 Java 版本引入了新的 `java.nio.file` 库。现在 `java.nio.file` 已经成为处理文件 I/O 的首选库。 `Path`、`Files`、`FileSystem` 等工具类，可以更方便快捷的访问和操作文件系统。目前大多数的开发人员普遍认为 `java.nio.file` 比传统的 `java.io` 包更直观且易于使用。虽然 `java.nio.file` 库已经非常成熟，但是随着操作系统和文件系统的发展，我们仍然可以期待在未来的 Java 版本中看到它的一些扩展和改进。
