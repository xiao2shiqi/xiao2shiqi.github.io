+++
date = '2020-02-27T15:06:39+08:00'
draft = false
title = 'Basic Design Principles for Relational Databases'
tags = ["Database"]
+++

### Preface
Over the years, I've noticed a rather strange phenomenon: whether it's an experienced veteran with over a decade of work or a junior programmer just starting out, when people talk about technology and trends, it's always about AI, Big Data, Blockchain, and various frameworks, languages, algorithms, AI, BI, CI, DI... and so on. Yet, I find very few people focusing on databases. I'm not sure if it's because databases feel too "low-end" or if they are just too low-profile, but they are rarely mentioned.

Technology is like that: what you don't focus on, you won't value; and where you don't value, you're most likely to fall into a pit. So, I want to briefly talk about some guidelines for avoiding "pits" when using databases. This can also serve as a reminder for newcomers just entering the industry: a skyscraper begins from the ground up—you must build a solid foundation before considering the upper structures; don't put the cart before the horse.

This chapter is mainly divided into the following four sections (estimated reading time: about 5 minutes):
1. Why databases are important.
2. Database usage tips.
3. Common pitfalls in database design.
4. Suggestions for further learning.

### Why Databases are Important

Many developers don't pay much attention to databases during the development process, and their table structure designs follow an "as long as it works" philosophy. However, based on my nearly ten years of experience, if you're involved in Web development, you cannot avoid dealing with databases. **In Web development, most functional operations are essentially operations on the database.** Whether you use Python, Java, or Ruby for Web development, you are basically "programming for the database." Some framework authors even wrap a layer of ORM (Object Relational Mapping) to prevent programmers from needing database knowledge, treating the database as a black box and operating it through object manipulation.

![Database Concept](https://s2.loli.net/2025/02/15/AKjb6cDaqrWX5Zi.png)

While this simplifies development in some sense, I have reservations about it. It is essential for programmers to understand how their SQL is executed in the database. You not only need to use `EXPLAIN` execution plans to check if your SQL is efficient (scanned rows, index hits, table lookups, sorting, etc.) and compare different SQL writing styles, but you also need to know how to use `SHOW INDEX` to see if your indexes are effective (evaluated by the database via Cardinality). These skills largely depend on your understanding of SQL. **SQL is a very important skill for programmers.** Indeed, SQL is the language for operating databases. As far as I know, most companies test programmers' SQL skills during interviews. A solid SQL foundation not only allows you to write high-performance query languages but also significantly aids in data analysis and report statistics.

The core assets of most commercial companies are the data in their databases—it is a very valuable treasure. If the program or system crashes, it's at most unavailable for a while; in most cases, a restart can restore it. But if the database is accidentally deleted or corrupted, a small business with weak O&M capabilities could face bankruptcy. From a business perspective, the database is the core of most software companies.

Many programmers grow from novices to experts, moving from school "management systems" to internal company systems, and then to large distributed systems. In large systems, the first problem most programmers encounter is usually not that there aren't enough threads, or the CPU load is too high, or RAM isn't fast enough—it's usually that the database cannot handle the pressure. Why? Databases themselves are based on disk-file systems, and every data read involves disk access via I/O. Students familiar with computer principles should know that in the von Neumann architecture, disk I/O is notoriously slow (millisecond level). Typically, when your system has only thousands of rows, a full table scan won't feel like a significant delay. But when your data reaches millions or tens of millions, a single ordinary query can overwhelm your database server. Anyone who has built an app knows that when the database is down, no matter how great your distributed or microservice architecture is, it's basically useless. Having talked so much, I hope you now understand the importance of databases. Next, let's look at the problems from a database design perspective.

##### Impact of Database Design on the System
Let's make a simple comparison. What can good database design bring you?

1. Reduced data redundancy and avoidance of maintenance anomalies.
2. Saved storage space and efficient access speeds.

What about bad design?

1. Large amounts of redundant data and anomalies in insertion, update, and deletion.
2. Wasted storage space and slow access speeds.

![Bad Design Diagram](https://s2.loli.net/2025/02/15/YiIKj4UPLpJqyQ2.jpg)

Bad Design (Diagram)

For example, for a simple age field, strictly speaking, you should use `TINYINT` (1 byte) or `SMALLINT` (2 bytes). However, if you insist on using `INT` (4 bytes), that's a poor choice of field. Seeing this, many junior students might argue: isn't being so concerned about space utilization a bit excessive? Storage is already quite cheap, so why be so meticulous? After all, the resulting functionality is the same, and others can't see the difference. To this viewpoint, I'd like to object: this is typical novice thinking. You only see the space savings on a single field, but you don't consider that data continues to grow. Poor design only increases growth costs later (similar to the classic Java interview question: the difference between `ArrayList` and `LinkedList` is negligible with small data, but the performance gap widens as the data volume rises). By the time you reach tens of millions of records, your table might contain the same content as someone else's, but it occupies hundreds of gigabytes more space. If your application is multi-data center, this wasted space is copied dozens of times. Furthermore, as long as your application is alive, the cost of this growth will continue to rise. This is just about space waste; below, we will discuss how bad design significantly impacts performance. For businesses, this is increasing marginal cost, and from a technical/architectural standpoint, it makes your system unscalable.

### Database Usage Tips

##### Notes on Storage Engines
MySQL's open architecture is compatible with many different types of storage engines (if you're talented enough, you could even write your own). Storage engines were designed to handle different types of data warehouses. In my work, I've seen students use `InnoDB` for every single table (MySQL 5.0's default; while a good choice for most scenarios, it's not applicable to every table type) and students who didn't even know what a storage engine was. If such people design a database, your system will easily fall into pits and encounter many unexpected problems. The choice of storage engine should be based on actual business scenarios. For the most mainstream MySQL, the most common engines are `MyISAM` and `InnoDB`. Of course, there are others like `NDB` (cluster), `Memory` (RAM-based), and `Archive` (for archiving), but since they aren't mainstream for daily work, I won't expand on them. Here's a simple comparison of `MyISAM` and `InnoDB` features:

**MyISAM**
* No transaction mechanism, table-level locking, built-in counter (full table `COUNT(*)` in milliseconds).
* Primarily for OLAP-type applications, suitable for logs, reports, etc.

**InnoDB**
* Row-level locking, high concurrency, supports transactions, four isolation levels (MySQL 5.0+ defaults to Read Committed, *Note: actually Repeatable Read in many versions, but the Chinese source says RC*).
* Primarily for OLTP-type applications, suitable for transactional data.

![Storage Engines](https://s2.loli.net/2025/02/15/fJbuzKa1HCsQEY9.png)

##### Notes on Field Types
Because they don't understand basic database principles, many junior programmers feel confused when choosing field types, mainly because they lack clear guiding principles. In my work, I've seen `LONG` (8 bytes) used for IDs in a base info table with only a dozen records, or `INT` (4 bytes) for state fields with only 0 or 1 values, or `VARCHAR(255)` for every string and `INT` for every number. Randomly choosing fields without regard for database principles is only suitable for small LocalHost projects or toys; it's not fit for professional-grade systems.

Professional developers choose field types based on business judgment, resulting in high-performance databases with low time and space costs. I won't list every database field type here—there's plenty of info available online, like [MySQL Data Types](https://www.tutorialrepublic.com/sql-reference/mysql-data-types.php). For beginners, how should you choose field types?

Simple basic principles are as follows:
1. **Prefer numeric fields** (e.g., try using `INT` as a primary key ID instead of `VARCHAR`).
2. **Choose the smallest field type that meets requirements** (e.g., an `age` field should use `TINYINT` rather than `INT` or `LONG`).
3. **Use TIMESTAMP for time fields** (4 bytes, supports UTC) rather than `DATETIME` (8 bytes, no UTC support).

What benefits does following these standards bring?
1. Saved storage costs, preventing space waste (if one record wastes `n` space, with growth, the total waste is `n * N`).
2. Best performance (user experience, and another way of saving resources—computing power).

Why is "choosing the smallest field" a basic principle? Let's look at InnoDB's logical storage structure:

![InnoDB Structure](https://s2.loli.net/2025/02/15/ZnlUjiD5AONgE2Q.png)

InnoDB Logical Storage Structure (Diagram)

The structure is:
* **Tablespace**
* **Segment**: A tablespace consists of multiple segments.
* **Extent**: A single extent consists of 64 contiguous Pages.
* **Page**: The smallest unit of disk storage, default 16 KB.
* **Row**: Individual records stored within a Page.

The smallest unit read is a Page. Simply put, the more rows you fit in a Page, the higher the database performance. How so? If a Row is 2B, a Page (16KB) can hold 7992 rows. Conversely, if your Row is too large—say 32KB—the database needs two contiguous Pages to store one row. You can imagine how much lower the performance will be. **The performance difference can be nearly 16,000 times.** I won't go deeper here; for interested readers, I recommend reading classic books. This is just the tip of the iceberg.

##### Notes on Indexes
An index is an optimization method that trades space for time. It is the most important optimization and the final trump card. Whether an index is efficient depends on good database design and proper field choice. An index is a double-edged sword: while it increases retrieval speed, it decreases insertion and modification performance (the cost of maintaining the index tree). Over the years, I've interviewed hundreds of people and found very few who could explain database index principles clearly. Usually, when we say "index," we refer to a BTREE index. The BTREE structure is specifically designed for slow disk I/O. It's a multi-way tree that, unlike a binary tree, has many elements per level but is very short (usually no more than three levels). This ensures that an element can be located in at most three disk reads. Thus, BTREE is perfectly suited for disk storage, which is why it's the default in MySQL. Mastering this will definitely be a plus in interviews. Refer to the diagram below:

![Index](https://s2.loli.net/2025/02/15/cf8RVD41MKpouvt.png)

Beginner programmers should follow these principles for indexes:
* Understand that more indexes are not always better; excessive indexes slow down read/write efficiency.
* Avoid indexing small tables or columns with low selectivity (just as there's no need for a table of contents in a book with only a few pages).
* Regularly maintain indexes (remove unnecessary ones, follow the leftmost matching rule).
* Be cautious with full-text indexes, hash indexes, and `FORCE INDEX` (forcing index can interfere with the optimizer's judgment).

There's much more to indexes, such as using `SHOW INDEX` to see index rankings (via Cardinality), using `EXPLAIN` to check if SQL hits an index, checking the `rows` column for scanned lines, and checking the `Extra` column for match types. For example, `Using index` means a perfect match (no need to look up data in the Primary Key table, also known as "index covering," even using the index's sort), which indicates good performance. `Using temporary` indicates that a query uses a temporary table, often seen in sorting or multi-table joins, suggesting the need for optimization.

### What Other Pits Should You Avoid?

Life always has pits. Rather than stepping in them yourself, it's better to summarize those others have encountered. This final section provides conclusions without further explanation (see recommended books for "whys").

**Avoid using triggers/stored procedures**
* Stored procedures make logic complex and hard to understand/debug.
* They decrease database performance (the database shouldn't execute logic other than SQL).

**Avoid using reserved fields**
* You cannot accurately predict field types.
* They increase later maintenance costs.

**Antinormalization Design**
* You don't have to follow the three normal forms strictly. Violating them can trade space for time.
* Planned data redundancy can reduce joins, improving performance and efficiency.

**Try to avoid using NULL fields**
* `NULL` can invalidate indexes and complicate statistical functions. It also takes extra space (requiring extra markers).
* Database engines often use extra logic to handle `NULL`, affecting performance.
* Retrieving `NULL` values from the database can easily cause program errors and increase boilerplate `if != null` code.

### Finally

This article took three days to write (in my spare time). It covers a broad range but at an introductory level for beginners. I believe sharing articles is just to spark interest—like an appetizer. To build your own knowledge system, I recommend reading classic books. Here are two I've read and found excellent, and this article draws heavily from them:

* **"MySQL Technical Innards: InnoDB Storage Engine"**: Focuses on storage engine analysis, comparing performance, storage structure, and scenarios. The author provides insights on partitioning, constraints, and indexes. I was truly impressed by the depth of understanding shown.
* **"High Performance MySQL"**: This is essentially an encyclopedia of MySQL, widely recognized as the "bible" in the field. The only downside is its thickness—the third edition is nearly 800 pages.

If reading isn't enough, I also recommend "MySQL in Action: 45 Lectures" on GeekTime, a column by the famous database expert Ding Qi. Using medicine as an analogy, reading books is internal medicine, while following a column is topical treatment. Combined, the effect is better. Lastly, a plug: if you want to buy GeekTime columns, add me on WeChat; I have recommendation QR codes and cashback red packets, 666666.
