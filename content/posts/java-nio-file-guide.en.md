+++
date = '2023-05-09T14:10:56+08:00'
draft = false
title = 'Guide to java.nio.file Library in Java'
tags = ["Java"]
+++

### Introduction

Before Java 7, file handling was primarily done through `java.io.File`, which lacked support for symbolic links, modern file systems, and efficient recursive operations. The `java.nio.file` package (NIO.2) introduced in Java 7 solved these issues with a more comprehensive and powerful API.

### Core Components

#### 1. Path
The `Path` interface represents a hierarchical path to a file or directory. Unlike `File`, it is system-independent.
```java
Path path = Paths.get("data", "logs", "app.log");
// On Windows: data\logs\app.log
// On Linux: data/logs/app.log
```

#### 2. Files Utility
The `Files` class contains static methods for almost any file operation:
- **Existence**: `Files.exists(path)`
- **Creating**: `Files.createFile(path)`, `Files.createDirectory(path)`
- **Copying**: `Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING)`
- **Moving**: `Files.move(source, target)`
- **Deleting**: `Files.delete(path)` (throws exception if not empty)

#### 3. Reading and Writing Content
- **Small files**: `Files.readAllLines(path)` or `Files.write(path, bytes)`.
- **Large files (Streams)**: `Files.lines(path)` returns a Stream that processes lines lazily.
```java
try (Stream<String> lines = Files.lines(path)) {
    lines.filter(l -> l.contains("ERROR"))
         .forEach(System.out::println);
}
```

### Advanced Features

#### WatchService (File Monitoring)
You can monitor a directory for changes (create, edit, delete).
```java
WatchService watchService = FileSystems.getDefault().newWatchService();
path.register(watchService, StandardWatchEventKinds.ENTRY_CREATE);

WatchKey key;
while ((key = watchService.take()) != null) {
    for (WatchEvent<?> event : key.pollEvents()) {
        System.out.println("Modified: " + event.context());
    }
    key.reset();
}
```

#### PathMatcher (Globbing)
Easily find files matching patterns like `*.txt` or `log-????-??-??.log`.
```java
PathMatcher matcher = FileSystems.getDefault().getPathMatcher("glob:*.{java,class}");
```

#### File Walking
Recursively visit every file in a directory tree using `Files.walkFileTree`.
- Useful for complex searches, tree deletions, or batch processing.

### Summary

The `java.nio.file` package is the modern, robust standard for file I/O in Java. It provides better performance, better error handling, and a more intuitive API than the older `java.io.File`.
