+++
date = '2023-12-13T14:09:57+08:00'
draft = true
title = '理解 Kubernetes 的 Controller Manager'
+++

### Controller Manager

Controller Manager 是控制平面的一个重要组件，负责维护 Kubernetes 集群的整体状态。

流程：

![image-20231210114754993](https://s2.loli.net/2025/02/13/rSdl17DbLjKoaHB.png)

在集群中 Controller Manager 主要做以下几件事情：

- **监听：** Controller Manager 通过 API Server 监听集群中的资源状态变化。当资源状态发生变化时，Controller Manager 会收到通知。
- **决策：** Controller Manager 会根据资源的定义和状态做出决策。如果一个 Deployment 的 Pod 数量低于预期，Controller Manager 会创建新的 Pod。
- **执行：** Controller Manager 会根据决策，执行相应的操作。例如，如果要创建新的 Pod，Controller Manager 会调用 API Server 来创建 Pod。

#### 常见的 Controller

Kubernetes 中内置了许多 Controller，当资源状态发生变化时，Controller Manager 会通知这些 Controller 做出决策和执行操作。

-   **Deployment Controller**：负责部署和管理 Pod 副本。
-   **ReplicaSet Controller**：负责管理 Pod 副本的数量。
-   **DaemonSet Controller**：确保每个节点都运行指定的 Pod。
-   **Job Controller**：负责执行一次性任务。
-   **CronJob Controller**：负责按照指定的频率执行任务。
-   **StatefulSet Controller**：确保 Pod 的顺序性和持久性。

**Cloud Controller Manager**

在云端部署 Kubernetes 时，需要将 Kubernetes 集群与云平台连接起来，以便 Kubernetes 集群可以使用云平台提供的资源，如虚拟机、负载均衡器、存储卷等。Cloud Controller Manager 提供了将 Kubernetes 集群与云平台连接起来的功能。它可以使用云平台的 API 创建和管理云资源 Cloud Controller Manager 主要用于以下场景：

-   在云端部署 Kubernetes 集群。
-   将 Kubernetes 集群与云平台的资源进行关联，如将 Deployment 资源中的 Pod 与虚拟机进行关联。
-   监控云资源的状态，并将其与 Kubernetes 资源的状态保持一致。

#### kubelet

Kubelet 是 Kubernetes 集群中的节点代理，kubelet 组件运行在每个节点上，负责在节点上运行 Pod：

![image-20231210160441907](https://s2.loli.net/2025/02/13/JK2t89cCheBYod4.png)

说明：

图片中 kubelet 组件通过 API Server 与集群的控制平面进行通信。从 API Server 获取 Pod 的定义信息，并根据 Pod 的定义信息创建和管理容器。

除此之外，kubelet 还负责以下任务：

-   从 Kubernetes API Server 获取 Pod 的定义信息。
-   使用容器运行时（Container Runtime）创建和管理容器。
-   监控 Pod 的健康状态。
-   定期检查 Pod 的状态，并根据 Pod 的状态做出相应的操作。
-   向 Kubernetes API Server 报告 Pod 的状态。

Pod 的详细启动流程：

![image-20231210162241039](https://s2.loli.net/2025/02/13/jEyON3roK7fg8n6.png)

说明

0.  **创建 Pod**: 用户向 API Server 发送创建 Pod 的请求。

0.  **API Server 更新 etcd**: API Server 将新 Pod 的信息写入 etcd。

0.  **Scheduler 监听新 Pod**: Scheduler 通过 watch 机制监听 etcd 中新的 Pod。

0.  **Scheduler 绑定 Pod**: Scheduler 选择一个合适的节点并将 Pod 与之绑定。

0.  **API Server 更新 etcd**: Scheduler 将绑定信息写回 etcd。

0.  **Kubelet 监听绑定的 Pod**: Kubelet 监听到有新的 Pod 绑定到其管理的节点。

0.  Kubelet 运行 Pod：Kubelet 开始在节点上运行 Pod，包括以下步骤：

    -   **RunPodSandbox**: 创建 Pod 的网络和存储沙盒环境。
    -   **PullImage**: 从镜像仓库拉取容器镜像。
    -   **CreateContainer**: 创建容器。
    -   **StartContainer**: 启动容器。

0.  **网络插件设置 Pod 网络**: 网络插件负责设置 Pod 的网络，如分配 IP 地址。

0.  **更新 Pod 状态**: Kubelet 将 Pod 的状态更新，通知 API Server，API Server 再次更新 etcd 中的状态信息。

整个创建 Pod 的过程是自动化的，由 Kubernetes 各组件协同工作完成。



### CRI

在没有 CRI（Container Runtime Interface） 之前，Kubernetes 与 Docker 容器运行时是紧密耦合的。这意味着 Kubernetes 只能使用 Docker 来创建和管理容器。但 CRI 的引入，改变了这一点。CRI 是 K8s 集群的一个插件接口，运行于集群的每个节点中，它使 kubelet 能够使用各种容器运行时而不需要重新编译：

![image-20231210164710033](https://s2.loli.net/2025/02/13/nGLIyWca9d5XKUH.png)

使用 CRI 的主要原因包含：

1. **容器运行时标准化**：CRI 提供了一种标准方式，使得不同的容器运行时（如 Docker、containerd、CRI-O 等）能够与 Kubernetes 进行交互。这意味着开发者和用户可以选择适合他们需求的容器运行时。
2. **解耦**：在 CRI 之前，容器运行时逻辑是硬编码在 Kubernetes 代码中的。通过 CRI，Kubernetes 和容器运行时之间的耦合度降低，容器运行时的更新和迭代可以独立于 Kubernetes 发布。
3. **可扩展**：CRI 为容器运行时的创新打开了大门，不同的团队可以独立开发和优化自己的运行时，只要它们遵循 CRI 规范。



#### CRI 定义

CRI（Container Runtime Interface）是 Kubernetes 通过 gRPC 协议定义的一系列接口规范。

![image-20231210165835899](https://s2.loli.net/2025/02/13/rntXBNOSoglGfw7.png)

理解 CRI 作为一组 gRPC 服务涉及以下几个方面：

-   **gRPC 与 Protocol Buffers**：

    -   使用 Protocol Buffers 作为接口定义语言（IDL）来定义服务和消息格式。
    -   Protocol Buffers 是一种语言中立、平台中立的序列化框架。

-   CRI 包括两个主要服务：

    -   `RuntimeService` 负责 Pod 和容器的生命周期管理，例如创建、启动、停止容器等。
    -   `ImageService` 负责镜像管理，例如拉取、列出和删除容器镜像。



#### OCI 规范

在容器技术刚刚兴起时，每个容器运行时都使用自己的容器格式和接口。这导致不同容器运行时之间无法互操作，给容器的开发、部署和管理带来了困难。为了解决容器互操作性的问题，Docker、CoreOS 和 appc 维护者于 2015 年 6 月启动了 OCI 项目。OCI 项目旨在定义容器格式和运行时的标准，以促进容器的互操作性。

OCI 由两个主要部分组成：

-   **Image Specification**：定义了容器镜像的格式。
-   **Runtime Specification**：定义了容器运行时的接口。

![image-20231210171626184](https://s2.loli.net/2025/02/13/i8H3PGE6bjAIcJ9.png)

**Image Specification**：

描述了容器镜像的结构和内容。它定义了容器镜像的根文件系统、环境变量、启动命令等。Image Specification 使不同容器运行时能够理解和使用容器镜像。

**Runtime Specification**：

定义了容器运行时的接口。它定义了容器运行时如何创建、启动、停止和删除容器。Runtime Specification 使 Kubernetes 等容器编排系统能够与不同容器运行时进行交互。

总结 OCI 的一些主要优势：

-   促进容器的互操作性。
-   降低容器的开发和部署成本。
-   提高容器的安全性和可靠性。

#### containerd

`containerd` 是 Docker 的一个核心组件，因为`containerd` 符合 OCI 标准，所以它也可以不依赖 Docker 单独在 Kubernetes 中使用。

![image-20231210172835256](https://s2.loli.net/2025/02/13/UpqDkY7cm2KadXO.png)

##### 优势

为什么更建议在 Kubernetes 单独使用 containerd ？

-   **轻量级和高效**：`containerd` 提供了容器运行所必需的核心功能，而不包括 Docker 的一些附加功能，这使得它更加轻量和高效。对于需要最小化资源占用的环境，如边缘计算或微服务架构。
-   **更少的资源消耗**：相比于完整的 Docker 引擎，`containerd` 占用更少的系统资源（CPU、内存），这对于资源受限的环境非常重要。
-   **遵循行业标准**：`containerd` 完全遵循 OCI 标准，可以无缝地与任何遵循 OCI 规范的容器镜像和运行时接口（如 CRI）一起工作。这种兼容性是在多种云环境和操作系统中部署容器的关键。
-   **简化和去除冗余**：在 Kubernetes 中，Docker 引擎的额外功能出现重复和冗余。在这些情况下，使用 `containerd` 可以简化设置并减少冗余。

单独使用 containerd 在问题定位上也有优势，这里展示三种不同的容器运行时配置方式与 Kubernetes kubelet 组件的交互：

![image-20231210172944007](https://s2.loli.net/2025/02/13/lGhfu3vTCoWE4x2.png)

这里说明因为 OCI 规范，Kubernetes 它已经不再依赖 Docker 作为唯一的容器运行时，并且可以支持多种运行时如 containerd 和 CRI-O。这种解耦提高了 Kubernetes 的灵活性和效率，同时也降低了架构的复杂性。

##### 差异

在 Kubernetes 中使用 Docker 和 containerd 作为容器运行时的差异对比：

![image-20231210173721674](https://s2.loli.net/2025/02/13/GkpZQc98I4MnCSL.png)

说明：因为 OCI 使 Kubernetes 的运行时层更加标准化，减少了额外的抽象层。

##### 性能

containerd 在各个场合中的性能表达都好过预期：

![image-20231210174000326](https://s2.loli.net/2025/02/13/SWNAywqlD6vVJCa.png)

各个运行时的对比：

![image-20231210174043727](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9cb8cead0fdc4c898187a5b45da4a45e~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2042&h=528&s=61291&e=png&b=ffffff)

### CNI

在 CNI（Container Network Interface） 之前，不同的容器运行时（如 Docker, rkt）有自己的网络配置方法，这导致了兼容性和移植性问题。CNI 为配置容器网络提供了一组标准的接口和插件。CNI 的目的是为容器运行时提供网络配置，以支持在不同环境下的容器网络操作。CNI 的出现解决了以下问题：

0.  **标准化容器网络配置**
0.  **简化集群管理**
0.  **插件化网络解决方案**
0.  **支持容器编排的动态网络需求**

CNI 为容器化环境中的网络配置提供了标准化和一致性，并且能够满足容器和容器编排工具的各种网络需求。

#### CNI 插件

CNI 为了能够支持云原生环境中对复杂的网络场景，应对不断演变的技术和应用场景的能力。所以使用模块化设计（插件）实现。

CNI 的插件主要分为以下几类：

-   主插件（Main plugins）：负责创建、配置和删除网络接口。一些主插件还可以管理路由规则和防火墙规则。
-   IPAM（IP 地址管理）：负责分配 IP 地址给容器。
-   Meta 插件： 一种特殊类型的插件，可以与主插件一起使用来提供额外的网络相关功能

常见的主插件包括：

-   **bridge**：创建一个网络桥接，并将容器连接到它。
-   **ipvlan**：类似于 macvlan，但基于 IP 而非 MAC 地址。
-   **loopback**：配置容器的 loopback 设备。

Meta：附加功能：

-   **portmap**：用于在主机和容器之间进行端口映射，使得外部可以通过主机上的端口访问容器内部的服务。
-   **bandwidth**：利用 Linux Traffic Control（tc）工具来限制容器的网络带宽。
-   **firewall**：使用 iptables 或 firewalld 来为容器设置防火墙规则，增强网络安全性。

这些插件可以独立使用或者组合使用，以支持各种网络配置需求。

#### 运行机制

插件的运行机制设计用于在容器初始化和销毁的时候配置和清理网络。以下是详细的运行机制：

![image-20231210194500175](https://s2.loli.net/2025/02/13/QajqO27IPpLxCiV.png)

说明：

0.  **初始化容器网络（ADD 操作）** ：

    -   当容器被创建时，容器运行时会调用 CNI 插件并执行 ADD 操作。
    -   kubelet 构建一个包含容器和网络配置信息的 JSON 格式的配置文件，并将这个配置传递给 CNI 插件。
    -   CNI 插件读取配置文件，执行必要的网络设置。
    -   如果配置中指定了 IPAM 插件，CNI 插件会调用 IPAM 插件分配 IP 地址、子网和其他网络参数。
    -   网络设置完成后，CNI 插件将容器连接到指定的网络，可能还会配置网络隔离和安全策略。

0.  **清理容器网络（DEL 操作）** ：

    -   当容器被销毁时，容器运行时会调用 CNI 插件执行 DEL 操作。
    -   CNI 插件再次接收到含有网络配置的 JSON 配置文件，并根据这些信息清理容器的网络设置。
    -   这包括删除网络接口、释放 IP 地址、清除路由规则等。
    -   如果使用了 IPAM 插件，CNI 插件会调用它来释放分配给容器的 IP 地址。

CNI 插件的运行机制的核心在于提供了一个标准化的方式来设置和管理容器网络，这样不同的容器运行时和编排系统就可以使用各种不同的网络技术，同时保持网络配置的一致性和可移植性。

#### 配置目录

在使用 CNI 的上下文中，`cni-bin-dir` 和 `cni-conf-dir` 是两个重要的目录，它们在 Kubernetes 集群中被 kubelet 用来配置网络。

**cni-bin-dir**：

这个目录包含了所有 CNI 插件的可执行文件。当 CNI 需要初始化一个容器的网络时，kubelet 会调用这个目录下的对应插件。例如，您可能会在这个目录下找到如 `bridge`、`loopback` 和 `host-local` 等网络插件的二进制文件。默认情况下，CNI 的二进制文件目录通常是 `/opt/cni/bin`。

**cni-conf-dir**：

这个目录包含了 CNI 配置文件，这些文件以 `.conf` 或 `.conflist` 结尾。这些配置文件定义了网络的具体参数，如网络名称、子网、IP 范围、网关、使用的 CNI 插件及其特定的配置选项。默认情况下，CNI 的配置文件目录通常是 `/etc/cni/net.d`。

kubelet 在启动时会检查这些目录，并使用这些目录下的插件和配置文件来为容器设置网络。

在 Kubernetes 集群上运行 `kubelet`，可以通过传递 `--cni-bin-dir` 和 `--cni-conf-dir` 参数来指定这些目录，如果不指定，则会使用默认值。

#### Flannel

作为一个 CNI 插件，Flannel 是一个简单的覆盖网络解决方案，Flannel 解决了一系列与容器网络相关的问题：

0.  **跨主机容器通信**： Flannel 允许分布在不同节点上的容器互相通信。
0.  **简化网络配置**： Flannel 自动为每个节点分配一个子网，并管理跨节点的路由，从而简化了网络配置。
0.  **易于部署**： 只需简单的几个步骤就可以部署。
0.  **网络隔离**： Flannel 提供了基本的网络隔离，通过为 Pod 分配独立的 IP 地址，确保 Pod 间网络的逻辑隔离。
0.  **兼容性**： Flannel 可以与任何遵循 CNI 规范的容器运行时一起工作。

**适合 Flannel 的场景**：

-   需要在多宿主机上快速部署一个 Kubernetes 集群。
-   需要一种简单的网络解决方案来支持 Pods 间的通信。
-   需要一个无需复杂配置的网络解决方案，它可以自动化地处理网络分配和管理。
-   在资源受限的环境中，比如在边缘计算场景，Flannel 的轻量级特性非常适合。

#### Calico

Calico 是一个广泛使用的网络和网络安全解决方案，特别是在 Kubernetes 环境中。它使用标准的 IP 路由，提供高性能和高可扩展性的网络解决方案。

**为什么会有 Calico ？** ：

-   在大规模环境中提供高效的网络路由。
-   实现 Pod 之间以及 Pod 和外部服务之间的高级网络安全策略。
-   提供跨多个 Kubernetes 集群的网络连通性。
-   简化网络运维，因为它使用的是数据中心中已经广泛采用的技术和协议。

**Calico 特点**：

0.  **高性能**：Calico 使用主机上的原生路由功能，可以提供接近裸机的网络性能。
0.  **可扩展性**：它可以无缝地扩展到非常大的部署，处理数以千计的节点。
0.  **网络安全策略**：Calico 提供了细粒度的网络安全策略，允许用户控制哪些容器可以通信。
0.  **网络隔离**：通过定义安全策略，Calico 能够为 Pod 间提供严格的网络隔离。
0.  **跨云和混合环境**：Calico 支持多种类型的环境，包括私有云、公有云和混合云。
0.  **遵守标准**：Calico 使用标准的 BGP（边界网关协议），易于与传统的网络架构集成。

**适合使用 Calico 的场景**：

-   **大规模部署**：需要管理大量节点的 Kubernetes 集群。
-   **安全要求高的应用**：需要复杂网络策略来保护敏感数据的企业级应用。
-   **混合云环境**：需要在不同的云环境或者数据中心间进行网络配置和管理。
-   **性能敏感型应用**：需要高吞吐量和低延迟网络的应用。

Calico 为需要高性能、高安全性和可扩展性的网络环境提供了一个强大而灵活的解决方案，适合各种规模和复杂度的网络配置。

#### 插件对比

CNI 常见插件对比：

![image-20231210202903172](https://s2.loli.net/2025/02/13/tM7g6Ius1p4cRqw.png)

### CSI

容器运行时 CSI（Container Storage Interface）是 Kubernetes 中负责容器存储管理的接口规范。CSI 将容器编排系统（CO）和存储系统解耦，使容器存储管理成为可插拔的插件。

**CSI 产生的原因**：

0.  **标准化**：在 CSI 出现之前，存储解决方案通常需要为每个容器编排系统定制开发，CSI 提供了一个通用的接口来标准化这一过程。
0.  **独立性**：CSI 允许存储插件独立于容器编排系统的核心进行开发和部署，这样就不需要每次容器编排系统更新时都要更新存储插件。
0.  **解耦存储**：通过将存储功能从容器编排系统核心代码中解耦出来，降低了系统的复杂性，并使得编排系统更易于维护和升级。

#### CSI 插件

Kubernetes 支持多种存储插件，这些插件提供了不同的存储功能和特性。主要有以下几种：

**In-tree Storage** ：

-   这些插件是 Kubernetes 源代码的一部分，也就是说，它们与 Kubernetes 核心代码一起维护和发布。
-   社区已不再接受新的 in-tree 插件，新的插件需要通过 out-of-tree 插件进行支持

**Out-of-tree FlexVolume**：

-   FlexVolume 指 Kubernetes 调用计算节点的执行文件与存储插件进行交互
-   FlexVolume 依赖宿主机的 root 权限和 attach, mount 工具

**Out-of-tree CSI (Container Storage Interface)** ：

-   CSI 插件shi 通过 RPC 与存储驱动进行交互

#### CSI 驱动

CSI 驱动（Container Storage Interface Driver）是遵循 CSI 规范的一种存储插件，用于容器编排系统（如 Kubernetes）中，实现存储卷的生命周期管理。

![image-20231210205711631](https://s2.loli.net/2025/02/13/9DU5Fg78PYyhAtd.png)

CSI 驱动一般包含：

External-attacher、External-provisioner、External-resizer、external-snapshotter、node-driver-register、CSI Driver

-   External-attacher：负责处理卷的“附加”操作，即将存储卷附加到相应的 Kubernetes 节点
-   External-provisioner：管理卷的动态供应（即创建和删除卷）
-   External-resizer：负责处理存储卷的动态扩展
-   external-snapshotter：管理存储卷快照的创建、删除和恢复
-   node-driver-register：在每个节点上运行，负责将 CSI 驱动注册到 kubelet。
-   CSI Driver：是实际执行存储操作的组件，例如创建卷、删除卷、附加卷、挂载卷等。

CSI 驱动与存储系统进行交互，根据 external-attacher、external-provisioner、external-resizer 和 external-snapshotter 的调用执行具体的存储操作。

#### 临时存储

##### emptyDir

emptyDir 是一种常见的临时存储卷，它在 Pod 被创建时创建，在 Pod 被删除时删除。emptyDir 卷最初是空的，可以由 Pod 中的容器使用。要使用 emptyDir，需要在 Pod 的 spec 中定义一个 volume 对象。volume 对象的类型为 emptyDir。示例：

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
          volumeMounts:
          - mountPath: /cache
            name: cache-volume
      volumes:
      - name: cache-volume
        emptyDir: {}
```

部署文件说明：

0.  首先在 `volumes` 中定义一个名为 `cache-volume` 的 emptyDir 临时存储卷，代表 Pod 使用本地临时存储
0.  然后在 `spec.containers` 中指定 `nginx` 挂载 `cache-volume` 的卷到容器的 `/cache` 目录使用

emptyDir 易于使用且数据在容器之间共享，适合存储临时文件且需要容器间共享数据的场景。

##### hostPath

hostPath 卷是将 Pod 挂载到宿主机上的目录。它是一种本地存储，在 Pod 被删除时不会被删除。示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: nginx
    volumeMounts:
    - mountPath: /etc/nginx/conf.d
      name: config-volume
  volumes:
  - name: config-volume
    hostPath:
      path: /etc/nginx/conf.d
```

部署文件说明：

0.  首先在 `volumes` 中定义一个 `config-volume` 的 hostPath 卷，指定路径为宿主机的 `/etc/nginx/conf.d` 目录。
0.  然后在 `spec.containers` 中的 `volumeMounts` 属性中引用 `cache-volume` 卷挂载到容器内 `//etc/nginx/conf.d` 目录使用

为 `hostPath` 卷指定类型可以提供额外的信息（或者强制性的校验）关于期望的 `hostPath` 应该如何存在或者创建。

```yaml
volumes:
- name: my-host-path
  hostPath:
    path: /some/path/on/host
    type: DirectoryOrCreate
```

在上面的示例中，`type: DirectoryOrCreate` 指定了如果在宿主机上 `/some/path/on/host` 路径不存在，Kubernetes 应该创建一个目录。

使用 hostPath 的注意事项：

0.  **数据漂移**：`hostPath` 卷绑定到特定节点上，如果 Pod 被调度到其他节点，数据不会随之迁移。
0.  **数据遗留：** Pod 被删除后，如果没有特解处理，那么 hostPath 上写的数据会遗留到节点上，占用空间。
0.  **可移植性**：因为 `hostPath` 依赖于宿主机上的特定路径，这可能影响到 Pod 的可移植性。

总结：`hostPath` 卷通常只会用于特定的用例，不推荐在生产环境使用。

#### 持久化存储

针对持久化存储，Kubernetes 引入 StorageClass，Volume，PVC，PVC 等概念，并且将存储独立于 Pod 的生命周期进行管理。

##### PV

PersistentVolume 是用于存储持久化数据的资源，代表一个集群级别的资源，它代表了一块实际的存储空间，例如一个 NFS 、一个云存储卷或一个本地磁盘。PV 可以被集群中的任何用户通过 PersistentVolumeClaim (PVC) 来请求和使用。

PersistentVolume 具有以下特性：

-   独立于 Pod 的生命周期：PersistentVolume 在 Pod 被删除后仍然存在。
-   可重复使用：PersistentVolume 可以被多个 Pod 使用。
-   PV 可以是静态供应的（由管理员预先创建）或动态供应的（由 `StorageClass` 自动创建）。
-   可扩展：PersistentVolume 的容量可以根据需要进行扩展。

示例：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

这个 `PersistentVolume` 对象表示了一块在宿主机上、位于 `/mnt/data` 目录的存储，其大小为 100 MB，并且可以被 Kubernetes 集群中的 Pods 使用。但它仅限于部署在同一节点上的 Pod，因为它使用了宿主机的本地路径。

##### PVC

**PersistentVolumeClaim** (PVC) 是 Pod 对 PersistentVolume 的请求。指定了需要的 PersistentVolume 类型和大小。Kubernetes 将使用该信息来查找可用的 PersistentVolume，并将其分配给 Pod。

**PersistentVolume 和 PersistentVolumeClaim 之间的关系**

PersistentVolume 和 PersistentVolumeClaim 之间的关系类似于订单和商品的关系。PersistentVolume 是商品，PersistentVolumeClaim 是订单。Pod 使用 PersistentVolumeClaim 来订购 PersistentVolume。

示例：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
```

在这个配置中，PersistentVolumeClaim 请求一个容量为 100MB 的存储，并且使用名为 manual 的 StorageClass（绑定到现有的 PersistentVolume）。一旦这个 PVC 被提交到 Kubernetes 集群（通过 `kubectl apply -f <filename>.yaml`），集群将尝试找到或动态创建一个符合这些要求的 PersistentVolume（PV）并与之绑定。

**在 Pod 中使用 PVC**

PVC 创建的目的是提供给 Pod 使用。示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
```

此配置的关键点在于，它创建了一个 Pod，并且通过上面创建的 PVC `task-pv-claim` 挂载了一个持久化卷到 Nginx 的内容目录中。这意味着任何存储在该目录中的内容（如网页文件）将被持久化。

##### StorageClass

StorageClass 是一种资源类型，它允许管理员定义不同类型的存储方案和特性，以及如何在集群中供应这些存储。通过使用 `StorageClass`，可以实现动态存储卷的供应，这意味着当有新的 `PersistentVolumeClaim` (PVC) 请求时，相应的 `PersistentVolume` (PV) 会被自动创建和配置，而无需管理员手动预先创建。

StorageClass 和 PVC，PV 之间的关系：

![image-20231211070828874](https://s2.loli.net/2025/02/13/BcI7JRymG3NVYsv.png)

**示例 StorageClass 配置**：

假设使用 AWS 的 Elastic Block Store (EBS) 作为存储后端：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: my-storage-class
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Retain
allowVolumeExpansion: true
```

说明：

-   `my-storage-class` 是这个 `StorageClass` 的名称。
-   使用的存储供应器是 AWS EBS (`kubernetes.io/aws-ebs`)。
-   参数 `type: gp2` 指定了使用 AWS 的通用型 SSD 卷。
-   `reclaimPolicy: Retain` 表示当 PVC 被删除时，相应的 PV 不会被自动删除。
-   `allowVolumeExpansion: true` 允许以后扩展由这个类创建的存储卷。

通过定义 StorageClass，集群的用户可以在创建 PVC 时指定所需的存储类型和配置，而无需关心具体的存储实现细节。

**示例 PVC 使用 StorageClass：**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  storageClassName: my-storage-class
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
```

在这个示例中：

-   `PersistentVolumeClaim` 的名称是 `my-pvc`。
-   `storageClassName` 设置为 `my-storage-class`，这将使用之前定义的 `StorageClass` 来动态创建 PV。
-   `accessModes` 是 `ReadWriteOnce`，意味着这个存储卷可以被单个节点以读写模式挂载。
-   请求的存储容量是 `100Mi`（100兆字节）。

当这个 PVC 被提交到集群时，Kubernetes 会自动根据 `my-storage-class` `StorageClass` 的定义来动态创建一个相应的 PV，并将其与这个 PVC 绑定。然后，这个 PVC 可以被 Pod 使用，以访问所供应的持久存储资源。

##### Local Volume

独占的 Local Volume 是指一种特定类型的持久卷（Persistent Volume，PV），它直接使用节点（Node）上的存储资源，如磁盘、分区或目录。这种类型的卷被称为“独占”因为它们只能被同一节点上的 Pod 使用，而无法跨节点共享或访问。

示例：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-local-volume
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  local:
    path: /mnt/data
```

在这种情况下，`my-local-volume` 是一个独占的 Local Volume，它具有 1Gi 的容量，`ReadWriteOnce` 的访问模式，以及 `/mnt/data` 的本地路径。

##### 最佳实践

关于持久化存储的最佳实践：

0.  不同解释类型的磁盘，需要设置不同的 StorageClass，以便区分。
0.  StorageClass 需要设置磁盘类型，以便区分。
0.  本地 PV 静态部署下，每个物理磁盘尽量只创建一个 PV，避免分区之间的 I/O 干扰。
0.  本地存储需要配合磁盘检测来使用。当集群部署规模化后，磁盘损坏是频发的事情。