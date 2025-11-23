+++
title = 'Spring Transactional 官方文档笔记'
date = 2025-11-19T00:00:00+08:00
draft = false
tags = ['Spring', 'Transaction', '笔记']
+++

> 信息来源：[Spring Transaction Management](https://docs.spring.io/spring-framework/reference/data-access/transaction.html)  
> 一句话总结：工作需要，了解事务，可以更好地处理业务问题  
> 评分：☆☆  
> 状态：已完成

为什么要使用 Spring 框架提供的事务模型？

Spring 解决了全局事务和本地事务的缺点，让应用程序开发者在任何环境中都能使用一致的编程模型。

### 目录

### 为什么研究？

### 有什么收益？

### 需要解决什么问题

### 摘抄

你只需编写一次代码，就可以在不同环境中受益于不同的事务管理策略。Spring 框架同时提供了声明式和编程式事务管理。大多数用户更喜欢声明式事务管理，我们在大多数情况下也推荐使用声明式事务管理。（大多数情况下，官方也推荐使用声明式事务）

在 Spring 事务中，正确的定义 TransactionManager 比较重要，它通常都是基于 JDBC DataSource 来创建，代码：

```java
@Configuration
// 假设你的配置文件名为 jdbc.properties，用于读取 ${jdbc.xxx}
@PropertySource("classpath:jdbc.properties")
public class DataSourceConfig {

    // 使用 @Value 注入配置文件中的属性，对应 XML 中的 ${...}
    @Value("${jdbc.driverClassName}")
    private String driverClassName;

    @Value("${jdbc.url}")
    private String url;

    @Value("${jdbc.username}")
    private String username;

    @Value("${jdbc.password}")
    private String password;

    // 1. 定义 DataSource Bean
    // 对应 XML: <bean id="dataSource" class="..." destroy-method="close">
    @Bean(destroyMethod = "close")
    public DataSource dataSource() {
        BasicDataSource dataSource = new BasicDataSource();
        dataSource.setDriverClassName(driverClassName);
        dataSource.setUrl(url);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return dataSource;
    }

    // 2. 定义 TransactionManager Bean
    // 对应 XML: <bean id="txManager" class="...">
    // 参数中的 dataSource 会自动由 Spring 注入上面定义的 Bean
    @Bean
    public PlatformTransactionManager txManager(DataSource dataSource) {
        DataSourceTransactionManager txManager = new DataSourceTransactionManager();
        txManager.setDataSource(dataSource); // 对应 <property name="dataSource" ref="dataSource"/>
        return txManager;
    }
}
```

上面的 PlatformTransactionManager 是 Spring 提供的命令式事务管理器的接口。

在事务方法中获取 Connection 搞点事情，不必采用传统的在 DataSource 上调用 getConnection() 方法的做法，而是可以使用 Spring 的 org.springframework.jdbc.datasource.DataSourceUtils 类，如下所示：

```java
// 这是包含事务的连接对象
Connection conn = DataSourceUtils.getConnection(dataSource);
```

## @Transactional 是怎么实现事务的？

它是通过 AOP 代理启用的，并且事务通知由元数据驱动（当前为基于 XML 或注解的元数据）。AOP 与事务元数据的结合产生了一个 AOP 代理，该代理在方法调用周围使用 TransactionInterceptor 并配合适当的 TransactionManager 实现来驱动事务。下图展示了在事务代理上调用方法的概念视图：

![AOP 事务代理示意图](/images/posts/spring-transactional-official-doc/transaction-aop-proxy.png)

## 默认情况下 Spring 事务是怎么回滚的？

在其默认配置下，Spring Framework 的事务基础设施代码仅在运行时的、未检查的异常情况下将事务标记为回滚。也就是说，当抛出的异常是 RuntimeException 的实例或子类时。（默认情况下，Error 实例也会导致回滚）。在默认配置中，从带事务的方法中抛出的已检查异常不会导致回滚。您可以通过指定回滚规则来精确配置哪些 Exception 类型会将事务标记为回滚，包括已检查异常。

因为默认情况下：`@Transactional` 只有 RuntimeException 和 Error 会触发事务回滚，Exception（普通异常）和 Checked Exception（受检异常，如 IOException、SQLException）不会回滚，这样其实挺危险。因此，在大多数企业项目中（包括你们 DragonPass 的 order / equity / member）我们通常会统一使用：

```java
// 所有异常都回滚
@Transactional(rollbackFor = Exception.class)
```

Spring 也提供手动回滚事务的方法，当然这是强烈不推荐使用的，这会让框架侵入代码，并且有违实现清晰的基于 POJO 的架构的初衷。

手动编程回滚事务的方式：

```java
public void resolvePosition() {
    try {
        // some business logic...
    } catch (NoProductInStockException ex) {
        // trigger rollback programmatically
        TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
    }
}
```

## 哪些方法可以被 Spring 事务代理？代理模式下的方法可见性和 @Transactional

`@Transactional` 注解通常用于具有 public 可见性的方法。从 6.0 起，protected 或包可见的方法默认情况下在基于类的代理中也可以被设为事务性的。请注意，在基于接口的代理中，事务性方法必须始终为 public，并且在被代理的接口中定义。对于这两种代理类型，只有通过代理进入的外部方法调用会被拦截。

## @Transactional 的推荐应用范围？

`@Transactional` 注解应用到接口定义、接口方法、类定义或类的方法上。Spring 团队建议你在具体类的方法上使用 `@Transactional` 注解，而不要依赖接口上声明的注解，即使在 5.0 之后，基于接口和目标类的代理对接口注解也能生效。

## @Transactional 的生效范围？

在代理模式（默认模式）下，只有通过代理进入的外部方法调用会被拦截。这意味着自我调用（即目标对象内的方法调用同一目标对象的另一个方法）不会在运行时产生实际事务，即使被调用的方法标注了 `@Transactional`。此外，代理必须完全初始化才能提供预期的行为，因此你不应在初始化代码中依赖此特性——例如，在 `@PostConstruct` 方法中。（类内部的 `self-invocation` 自调用和初始化调用的事务方法将失效，因为 AOP 无法代理自调用和初始化调用）

## 事务传播行为

什么是传播行为？如图所示：

![事务传播行为示意图](/images/posts/spring-transactional-official-doc/transaction-propagation.png)
