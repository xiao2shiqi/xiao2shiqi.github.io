+++
date = '2023-11-29T14:21:48+08:00'
draft = true
title = '理解 Kubernetes 的 Scheduler'
tags = ["云原生"]
+++

## 概述

kube-scheduler 是 Kubernetes 集群的核心组件之一，它负责为新创建的 Pods 分配节点。它根据多种因素进行决策，包括：

1. **资源需求和限制**：考虑每个 Pod 请求的资源量（如 CPU 和内存）以及节点上可用的资源。
2. **亲和性和反亲和性规则**：根据 Pod 的亲和性设置选择最适合的节点。
3. **健康检查**：确保选择的节点健康且能够运行 Pod。
4. **负载均衡**：尽量平衡集群中各个节点的负载。



## 使用

### limits 和 reuqests

在部署对象中的 spec 中常常会见到关于 `limits` 和 `requests` 的声明 ，例如：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          resources:
            limits:
              memory: 1Gi
              cpu: 1
            requests:
              memory: 256Mi
              cpu: 100m
```

这里的 limits 和 requests 是与 Pod 容器资源管理相关的两个关键概念：

-   Limits：指定容器运行时能够使用的最大资源量
-   Requests：指定容器启动时最低需要的资源量

**limits 和 requests 跟 scheduler 有什么关系 ？**

在集群中 kube-scheduler 一直是默默无闻的幕后工作者，它主要工作内容如下：

1. 当你创建一个 Deployment，如这个 `nginx`，是由 kube-scheduler 决策将其调度到哪个 Node 上运行的
2. kube-scheduler 会监听 apiserver 获取集群全局视图，然后根据 Pod 的资源请求（requests 和 limits）分析
3. 最终 kube-scheduler 会结合资源请求和集群的实际情况来调度 Pod

总之，kube-scheduler 会保证 Pod 会调度到满足其运行资源需求的 Node 节点上。



### LimitRange

**描述**

LimitRange 是资源描述对象，主要用于限制命名空间内资源的使用。它可以设置默认的资源请求和限制，以及资源使用的最大和最小值。它可以确保每个 Pod 或容器在资源使用上遵循特定的策略，从而避免单个 Pod 或容器占用过多资源。使用示例如下：创建一个 YAML 文件保存 LimitRange 内容。

例如：`mem-limit-range.yaml`：

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
    - default:
        memory: 512Mi
      defaultRequest:
        memory: 256Mi
      type: Container
```

应用到集群：

```sh
$ kubectl apply -f mem-limit-range.yaml
```

查看创建的 LimitRange 对象：

```sh
$ kubectl describe limitrange mem-limit-range
```

输出：

```sh
Name:       mem-limit-range
Namespace:  default
Type        Resource  Min  Max  Default Request  Default Limit  Max Limit/Request Ratio
----        --------  ---  ---  ---------------  -------------  -----------------------
Container   memory    -    -    256Mi            512Mi          -
```

说明：

-   Kind：设置为 LimitRange，用于限制命名空间内资源的使用。

-   Metadata：设置资源的名称

-   Spec：

    -   Limits：
    -   default：指定没有明确资源限制的容器的默认内存限制为 512Mi
    -   defaultRequest：指定没有明确资源请求的容器的默认内存请求。这里设置为 256Mi
    -   type：应用这些限制的资源类型，在这里是 `Container`

**验证**

定义一个没有声明资源请求的部署对象，文件命名为： `nginx-without-resource.yaml` ，如下：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
```

应用部署到集群：

```sh
$ kubectl apply -f nginx-without-resource.yaml
```

等 Pod 创建后，可以通过检查它们的配置来确认 `LimitRange` 是否生效。

```sh
$ kubectl describe pod [POD_NAME]
```

输出：

```yaml
Containers:
  #.. ignore
    Limits:
      memory:  512Mi
    Requests:
      memory:     256Mi
```



### initContainers

initContainers 用于在主应用容器启动之前执行一些预备任务。常见于以下场景：

1. **准备工作**：设置需要的配置文件、数据库迁移、等待其他服务就绪等。
2. **安全性**：权限提升操作，如改变文件权限或者执行特定的安全检查。
3. **服务依赖性**：等待其他服务或数据库可用。

initContainers 在执行完其任务后会停止，且必须成功完成才能启动主容器。非常适合用于启动前的初始化任务。

示例：在部署对象中声明 initContainers 属性：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      initContainers:
        - name: init-myservice
          image: busybox:1.28
          command: ['sh', '-c', 'echo The app is running! && sleep 10']
      containers:
        - name: nginx
          image: nginx
```

将部署对象应用到集群：

```sh
$ kubectl apply -f init-container.yaml
```

当 Pod 启动后，可以通过查看事件日志验证容器的加载顺序：

```sh
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  2m20s  default-scheduler  Successfully assigned default/nginx-deployment-6445f86ddc-fmmzw to docker-desktop
  Normal  Pulling    2m20s  kubelet            Pulling image "busybox:1.28"
  Normal  Pulled     116s   kubelet            Successfully pulled image "busybox:1.28" in 23.099396719s (23.099404677s including waiting)
  Normal  Created    116s   kubelet            Created container init-myservice
  Normal  Started    116s   kubelet            Started container init-myservice
  Normal  Pulling    106s   kubelet            Pulling image "nginx"
  Normal  Pulled     88s    kubelet            Successfully pulled image "nginx" in 18.382000675s (18.382006008s including waiting)
  Normal  Created    88s    kubelet            Created container nginx
  Normal  Started    88s    kubelet            Started container nginx
```

可以看到 initContainers 声明的容器已经加载，然后查看特定的日志，来检查 Pod 日志输出：

```sh
$ kubectl logs [POD_NAME] -c init-myservice
```

输出：

```sh
The app is running!
```

验证完成。

**initContainers 和 kube-scheduler 的关系 ？**

如果 initContainers 没有声明资源需求，默认也会使用 LimitRange 声明的默认资源，这也意味着，initContainers 也是由 kube-scheduler 来调度创建的。所以在 initContainers 中加上资源需求也会影响着 kube-scheduler 的调度决策。

### nodeSelector

在部署对象中，`nodeSelector` 属性的作用是用于把指定 Pod 调度到具有特定标签的节点上。如果没有满足要求的 Node 节点，则 Pod 会持续等待，示例：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
      nodeSelector:
        disktype: ssd
```

在这个例子中 nodeSelector 属性值为：`disktype: ssd` 。这表明这个 Pod 应该被调度到标签为 `disktype=ssd` 的 Node 节点上。kube-scheduler 在调度时，会选择合适的节点以运行这个 Pod 时。

先将部署对象应用到集群中：

```sh
$ kubectl apply -f node-selector.yaml
```

然后查看 Pod 状态：

```sh
$ kubectl get pod
```

输出：

```sh
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-f5bc98d57-pmq9v    0/1     Pending   0          2m17s
```

可以看到创建的 Pod 一直保持在 "Pending" 状态。通过事件日志查看具体原因：

```sh
$ kubectl describe pod [POD_NAME]
```

输出：

```sh
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  4m38s  default-scheduler  0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling..
```

从事件日志可以看出，这个 Pod 不能被调度，因为没有节点满足其设定的节点选择条件。因为我的集群中确实没有任何标记为 `disktype: ssd` 的节点在运行。



### Affinity 亲和性

NodeSelector 的演进版本，提供了更复杂的选择规则。除了简单的匹配，它们还支持更丰富的条件表达式，如 "存在"、"不等于"、"在集合中" 等，并且支持对 Pod 之间（Pod Affinity/Anti-Affinity）以及 Pod 与节点之间（Node Affinity）的亲和性/反亲和性设置。在 Kubernetes 后续版本中 Affinity 也逐渐替代了 NodeSelector。



#### **podAffinity**

podAffinity 用于定义 Pods 之间的亲和性。使得某个 Pod 被调度到与其他特定标签的 Pod 相同的节点上。

使用场景：当希望一组服务紧密地协同工作时，比如一个应用的不同组件需要低延迟通讯。

示例：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-anti
spec:
  replicas: 2
  selector:
    matchLabels:
      app: anti-nginx
  template:
    metadata:
      labels:
        app: anti-nginx
    spec:
      affinity:
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
                - key: a
                  operator: In
                  values:
                    - b
            topologyKey: kubernetes.io/hostname
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
                - key: app
                  operator: In
                  values:
                    - anti-nginx
            topologyKey: kubernetes.io/hostname
      containers:
        - name: with-pod-affinity
          image: nginx
```

部署文件展示亲和性（Affinity）设置：

-   PodAffinity：要求调度的 Pod 必须与具有特定标签（键 `a`，值 `b`）的 Pod 在相同的节点上。
-   PodAntiAffinity：要求调度的 Pod 不能与具有相同标签（键 `app`，值 `anti-nginx`）的 Pod 在相同的节点上。

将上面部署文件应用到集群后，查看 Pods 的分布情况：

```sh
NAME                          READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
nginx-anti-5656fcbb98-62mds   0/1     Pending   0          5s    <none>   <none>   <none>           <none>
nginx-anti-5656fcbb98-wxphs   0/1     Pending   0          5s    <none>   <none>   <none>           <none>
```

可以 Pod 因为亲和性规则无法调度一直处于等待状态，查看特定 Pod 的事件日志可以验证：

```sh
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  27s   default-scheduler  0/1 nodes are available: 1 node(s) didn't match pod affinity rules. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling..
```

利用 Pod 亲和性和反亲和性规则来控制 Pod 的调度位置，以实现特定的调度需求和负载分布。

#### **nodeAffinity**

用于定义 Pod 与节点之间的亲和性。控制 Pod 被调度到具有特定标签或属性的节点上。

适用场景：当您需要根据硬件特性（如 GPU、高性能存储）或其他自定义标签（如环境标签）调度 Pod 时。

示例：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: disktype
                    operator: In
                    values:
                      - ssd
      containers:
        - name: nginx
          image: nginx
```

部署文件的亲和性（Affinity）设置：

-   `nodeAffinity` 被设置为要求 Pod 被调度到具有 `disktype: ssd` 标签的节点上。

将上面部署文件应用到集群后，查看 Pod 的运行情况：

```sh
NAME                                READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
nginx-deployment-565d7797dc-jf5nk   0/1     Pending   0          14s   <none>   <none>   <none>           <none>
```

可以 Pod 因为亲和性规则无法调度一直处于等待状态，查看特定 Pod 的事件日志可以验证：

```sh
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  89s   default-scheduler  0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling..
```



**preferredDuringSchedulingIgnoredDuringExecution**

和之前的 requiredDuringScheduling 调度类型不同，preferredDuringScheduling 表明其是一个偏好性的调度，调度器会根据偏好优先选择满足对应规则的节点来调度Pod。但如果找不到满足规则的节点，调度器则会选择其他节点来调度Pod。

示例：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 1
            preference:
              matchExpressions:
                - key: disktype
                  operator: In
                  values:
                    - ssd
      containers:
        - name: nginx
          image: nginx
```

配置说明：这里使用的是 `preferredDuringSchedulingIgnoredDuringExecution` 类型，这意味着调度器会尽量但不强制将 Pod 调度到具有 `disktype: ssd` 标签的节点上。

将上面部署文件应用到集群后，查看 Pod 的运行情况：

```sh
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-69c654d896-7qh8t   1/1     Running   0          28s
```

可以看到虽然我本地没有满足亲和性规则的 Node 节点，但是 Pod 依然可以调度起来了。

总结：

-   `podAffinity` 关注的是 Pod 之间的关系不同

-   `nodeAffinity` 更关注 Pod 与节点特性之间的关系

    -   requiredDuringScheduling：硬亲和，强制型调度规则，必须满足亲和性设置，否则不能调度
    -   preferredDuringScheduling：软亲和，偏好型调度规则，首先找到满足设置的节点，没有则会调度到其他节点



### Taints 污点

Taints 和 Tolerations 是 Kubernetes 中用于控制 Pod 调度到特定节点的一种机制，相比 Affinity 亲和性 **相似性** 的机制，Taints 的规则是属于 **排斥性** 的机制，用来“排斥”不满足特定条件的 Pod。

Taints 有三种效果：

-   `NoSchedule`（不会调度新 Pod）
-   `PreferNoSchedule`（尽量避免调度新 Pod）
-   `NoExecute`（新 Pod 不会调度且已存在 Pod 可能会被迁移）

Taints 常见的应用场景：

-   对于集群中不想共享的 Node，可以加上 Taints 标签表示独享
-   用于多租户 Kubernetes 计算资源隔离
-   Kubernetes 本身使用 Taints 机制驱除不可用的 Node

使用示例：

给节点添加 Taint，防止所有 Pod 自动调度到该节点，除非它们具有匹配的 Tolerations：

```sh
$ kubectl taint nodes docker-desktop for-special-user=cadmin:NoSchedule
```

先定义一个没有任何 Tolerations 的 Pod 来验证：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
```

将它应用到集群，查看 Pod 状态会一直处于 Pending：

```sh
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-77b4fdf86c-wm5f9   0/1     Pending   0          23s
```

从事件日志可以看到是 Taints 在发挥作用：

```sh
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  56s   default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {for-special-user: cadmin}. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling..
```

然后再 Pod 定义中添加 Tolerations，允许它被调度到带有特定 Taint 的节点上：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
      tolerations:
        - key: "for-special-user"
          operator: "Equal"
          value: "docker-desktop"
          effect: "NoSchedule"
```

这个部署文件设置了一个 **容忍度 (Tolerations)** 规则：允许 Pod 被调度到标记为 `for-special-user=docker-desktop` 并且具有 `NoSchedule` 效果的节点上。

将它应用到集群，查看 Pod 状态：

```sh
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-dd7d69c9c-77qlf   1/1     Running   0          31s
```

Pod 已经正常调度，这也是 Taints 发挥作用。

如果节点不在需要 Tanints 作为排除，可以移除 ：

```sh
$ kubectl taint nodes docker-desktop for-special-user=cadmin:NoSchedule-
```

输出：

```sh
node/docker-desktop untainted
```

### PriorityClass

`PriorityClass` 用于定义 Pod 的调度优先级。常见的场景包括：

1. **确保关键服务优先调度**：对于关键组件，如数据库、核心应用服务，可以设置更高的优先级。
2. **管理资源争用**：在资源有限的环境中，通过设置不同的优先级，管理不同 Pod 的调度顺序。

使用 `PriorityClass` 的步骤：

1. **创建 PriorityClass**：

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
```

说明：

-   **value**：这是一个整数，表示该 PriorityClass 的优先级。较高的数值表示更高的优先级。
-   **globalDefault**：表示为集群中所有没有指定优先级的 Pod 的默认优先级。

2.  **在 Pod 中指定 PriorityClass**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  priorityClassName: high-priority
  containers:
  - name: mycontainer
    image: myimage
```

通过 `priorityClassName` 应用刚才创建的 PriorityClass，从而确保该 Pod 具有更高的调度优先级。



### 自定义 scheduler

默认的调度器是面向通用的使用场景设计的，如果默认的 Kubernetes 调度器无法满足需求，也可以通过自定义的调度器来满足更加个性化的需求，示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  schedulerName: my-custom-scheduler
  containers:
  - name: mycontainer
    image: myimage
```

社区也有很多成熟开源的自定义调度器，例如：

-   腾讯 TKE 的调度器
-   华为 volcano 调度器

另外也可以参考 `kube-scheduler` 源码实现一个自己的调度器。