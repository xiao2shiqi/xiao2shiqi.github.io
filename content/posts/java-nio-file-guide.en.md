+++
date = '2023-05-09T14:10:56+08:00'
draft = false
title = 'Introduction and Usage of the Java.nio.file Library'
tags = ["Java"]
+++

### Overview

In early versions of Java, file I/O operations were relatively weak, primarily suffering from the following issues:

1.  **Lack of support for modern file systems**: Only basic file operations were provided, with no support for many features of modern file systems.
2.  **API not intuitive**: The file operation API design was relatively complex and verbose, leading to a poor user experience.
3.  **Insufficient performance for large files and concurrency**: The simple I/O model did not fully leverage the performance advantages of modern hardware and suffered from many synchronization issues.

To address these, later Java versions introduced the `java.nio.file` library to enhance Java's file operation capabilities. It also added stream functionalities, making file handling much more convenient. In this chapter, we will introduce the commonly used classes and modules in `java.nio.file`, roughly as follows:

1.  **Path**: Introduction to the `Paths` module and the `Path` interface.
2.  **Files**: Introduction to the `Files` and `FileSystems` utility classes.
3.  **File Management Services**: `WatchService`, `PathMatcher`, and other file services.

### Path

The `java.nio.file.Paths` and `java.nio.file.Path` classes are used in the Java NIO file I/O framework to handle file system paths. Here is a brief introduction:

-   **`Paths` Module**: The `Paths` module provides static methods to create `Path` objects, which represent paths in the file system. For example, `Paths.get()` can be used to create a `Path` object representing a file path.
-   **`Path` Interface**: The `Path` interface represents a path in a file system and provides a series of methods to manipulate paths. For example, `Path.toAbsolutePath()` gets an absolute path, and `Path.getParent()` gets the parent path.

> Regarding cross-platform compatibility: `Path` objects can work across different file systems on different operating systems, shielding developers from OS differences.

Here are some simple usage examples:

```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class PathExample {

    public static void main(String[] args) {
        // Create an absolute path
        Path absolutePath = Paths.get("C:\\Users\\phoenix\\file.txt");     // Passing "example\\file.txt" would create a relative path
        System.out.println("Absolute path: " + absolutePath);
        // Get parent path
        System.out.println("Parent path: " + absolutePath.getParent());
        // Get file name
        System.out.println("File name: " + absolutePath.getFileName());
        // Get root path
        System.out.println("Root path: " + absolutePath.getRoot());
        // Resolve (merge) paths
        Path resolvePath = Paths.get("C:\\Users\\phoenix").resolve("file.txt");
        System.out.println("Merged path:" + resolvePath);
    }
}
```

Output:

```sh
Absolute path: C:\Users\phoenix\file.txt
Parent path: C:\Users\phoenix
File name: file.txt
Root path: C:\
Merged path:C:\Users\phoenix\file.txt
```

From this, you can see not only the methods for manipulating file paths but also that I am using the `Windows` operating system. For more usage, you can refer to the official API documentation.

### Files

The `java.nio.file.Files` class is a utility class in the Java NIO file package. it provides a series of static methods for conveniently performing various file system operations such as creating, deleting, copying, moving, reading, and writing files. For example, `Files.exists()` checks if a file exists, and `Files.createDirectory()` creates a new directory.

Here are some simple usage examples:

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Arrays;
import java.util.List;

public class PathExample {

    public static void main(String[] args) throws IOException {
        Path path = Paths.get("example.txt");
        // 1: Check if file exists
        boolean exists = Files.exists(path);
        System.out.println("File exists: " + exists);
        if (!exists) {
            // 2: Create file if it doesn't exist
            Files.createFile(path);
        }
        // 3: Copy a file
        Path target = Paths.get("example2.txt");
        Files.copy(path, target, StandardCopyOption.REPLACE_EXISTING);
        // 4: Create directory
        Path newDirectory = Paths.get("example");
        Files.createDirectories(newDirectory);
        // 5: Move file: move example2.txt into the example directory
        Files.move(target, newDirectory.resolve("example2.txt"), StandardCopyOption.REPLACE_EXISTING);
        // 6: Delete file and directory
        Files.delete(newDirectory.resolve("example2.txt"));
        Files.delete(newDirectory);    // Only empty directories can be deleted
        // 7: Write byte array to file
        Files.write(path, "Hello World".getBytes());
        // 8: Write sequence of text lines to file
        List<String> lines = Arrays.asList("Line 1", "Line 2", "Line 3");
        Files.write(path, lines, StandardCharsets.UTF_8, StandardOpenOption.CREATE);
        // 9: Read file and print all lines
        Files.readAllLines(path, StandardCharsets.UTF_8).forEach(System.out::println);
    }
}
```

Output:

```sh
File exists: true
Line 1
Line 2
Line 3
```

You can also view logs or files in the project root:

![image-20230508234504230](https://s2.loli.net/2025/02/15/snRvXz21cLbtyN9.png)

The above code demonstrates how to use the `Files` class for common operations. In actual projects, you can combine these methods to suit your needs.

**Supplements:**

The `Files.delete` function can only delete empty directories. This design is intentional because recursively deleting files and directories can be a very dangerous operation, especially if you accidentally delete a directory containing critical data. If you want to delete a directory containing subdirectories and files, you need to first recursively delete everything within it before deleting the directory itself. This can be achieved by traversing the file tree using `Files.walkFileTree` and calling `Files.delete`.

### FileSystems

The `FileSystems` class provides static methods to access and manipulate the default file system (usually the local file system of the OS) as well as other file system implementations. Here is a simple example:

```java
public class FileSystemsExample {

    public static void main(String[] args) {
        // Get the default file system
        FileSystem fileSystem = FileSystems.getDefault();
        // Get the path separator
        String pathSeparator = fileSystem.getSeparator();
        System.out.println("Path separator: " + pathSeparator);
        // Get the root directories of the file system
        for (Path root : fileSystem.getRootDirectories()) {
            System.out.println("Root directory: " + root);
        }
        // Create a Path object using the file system
        Path path = fileSystem.getPath("path", "to", "file.txt");
        System.out.println(path);
        // Check if read-only
        System.out.println("is read only ?: " + fileSystem.isReadOnly());
        // Get the file system provider
        System.out.println("provider: " + fileSystem.provider());
    }
}
```

Output:

```sh
Path separator: \
Root directory: C:\
path\to\file.txt
is read only ?: false
provider: sun.nio.fs.WindowsFileSystemProvider@5b480cf9
```

While `FileSystem` has relatively few methods, it is essential for creating `WatchService` and `PathMatcher`.

#### WatchService (File Monitoring)

`WatchService` is a file system observer created based on `FileSystem`. It is primarily used to monitor file system events (such as creation, modification, or deletion of files or directories) in real-time. This is useful for scenarios such as:

-   File uploads
-   Real-time backups
-   Hot reloading configurations

Here is a simple example:

```java
import java.io.IOException;
import java.nio.file.*;

public class WatchServiceExample {

    public static void main(String[] args) throws IOException, InterruptedException {
        // Create WatchService
        WatchService watchService = FileSystems.getDefault().newWatchService();

        // Register listener for a specific directory
        Path dir = Paths.get("C:\\Users\\phoenix");
        dir.register(watchService, StandardWatchEventKinds.ENTRY_CREATE, StandardWatchEventKinds.ENTRY_MODIFY, StandardWatchEventKinds.ENTRY_DELETE);

        while (true) {
            // Get and process events
            WatchKey key = watchService.take();
            for (WatchEvent<?> event : key.pollEvents()) {
                System.out.println("Event: " + event.kind() + " - " + event.context());
            }

            // Reset key to continue monitoring
            if (!key.reset()) {
                break;
            }
        }
        watchService.close();
    }
}
```

Running this program will monitor my system's user directory. When I create, edit, or delete a file there, the program outputs:

```sh
Event: ENTRY_CREATE - New Text Document.txt
Event: ENTRY_DELETE - New Text Document.txt
Event: ENTRY_CREATE - helloWorld.txt
Event: ENTRY_MODIFY - helloWorld.txt
Event: ENTRY_MODIFY - helloWorld.txt
Event: ENTRY_MODIFY - helloWorld.txt
Event: ENTRY_DELETE - helloWorld.txt
```

#### PathMatcher (File Matching)

`PathMatcher` is an interface for file path matching. It helps filter files or directories based on specific rules (using glob or regex syntax) while traversing the file system. Usage scenarios include:

-   **File filtering**: Filtering results based on pattern while searching.
-   **Batch operations**: Finding a group of files for batch processing.
-   **Directory monitoring**: Combining with `WatchService` to filter for specific files (e.g., `.log` files).

Example code:

```java
import java.io.IOException;
import java.nio.file.*;
import java.util.stream.Stream;

public class PathMatcherExample {

    public static void main(String[] args) throws IOException {
        // Create PathMatcher with glob syntax: matches all files ending in .tmp
        FileSystem fileSystem = FileSystems.getDefault();
        PathMatcher matcher = fileSystem.getPathMatcher("glob:*.tmp");
        // Find and delete matching files in a specified directory
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

The example uses `PathMatcher` to find and delete `.tmp` files, which could be part of a utility for cleaning temporary files.

### Reading File Content

To demonstrate reading file content, let's assume a sample file at `path/to/file.txt`:

```sh
Java is a high-level programming language.
Python is an interpreted, high-level programming language.
JavaScript is a scripting language for Web development.
C++ is a general-purpose programming language.
Rust is a systems programming language.
```

`Files` provides two primary methods for reading:

1.  **`readAllLines()`**: Loads everything into memory; used for small to medium files.
2.  **`lines()`**: Reads line by line; suitable for large files.

#### Small Files

`readAllLines()` loads the entire content into memory, making it suitable when you need to process the whole content immediately.

```java
public class ReadAllLinesExample {

    public static void main(String[] args) throws IOException {
        // Read all lines
        List<String> lines = Files.readAllLines(Paths.get("path/to/file.txt"), StandardCharsets.UTF_8);

        // Process content (e.g., word frequency)
        Map<String, Long> wordFrequency = lines.stream()
                .flatMap(line -> Arrays.stream(line.split("\\s+")))
                .map(String::toLowerCase)
                .collect(Collectors.groupingBy(word -> word, Collectors.counting()));

        System.out.println("Word Frequency:");
        wordFrequency.forEach((word, count) -> System.out.printf("%s: %d%n", word, count));
    }
}
```

#### Large Files

The `lines()` method is efficient for large files as it doesn't load everything at once. Using Java 8's Stream API, you can process lines as they are read.

```java
public class LinesExample {

    public static void main(String[] args) throws IOException {
        Path filePath = Paths.get("path/to/file.txt");

        // Read line by line and process
        try (Stream<String> lines = Files.lines(filePath)) {
            Map<String, Long> wordFrequency = lines
                    .skip(3)            // Skip first 3 lines
                    .flatMap(line -> Arrays.stream(line.split("\\s+")))
                    .map(String::toLowerCase)
                    .collect(Collectors.groupingBy(word -> word, Collectors.counting()));

            System.out.println("Word Frequency:");
            wordFrequency.forEach((word, count) -> System.out.printf("%s: %d%n", word, count));
        }
    }
}
```

Output:

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

### Summary

In the past, the `java.io` package handled file I/O but had issues with performance, API intuitiveness, and metadata operations. To solve these, Java introduced the `java.nio.file` library, which is now the preferred choice. Utility classes like `Path`, `Files`, and `FileSystem` provide faster and more convenient access to the file system. Most developers find `java.nio.file` more intuitive and easier to use than traditional `java.io`. While the library is very mature, we can still expect future improvements as OS and file systems evolve.
