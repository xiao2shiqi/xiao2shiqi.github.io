+++
date = '2023-11-25T14:29:56+08:00'
draft = false
title = '理解 Kubernetes 的 Etcd'
+++

### 概述

etcd 是一个基于 Raft 协议实现。开源的、分布式的键值存储系统。主要用于在分布式系统中提供强一致性和高可用性的数据存储。etcd 在 Kubernetes 中的作用如下：

1. 集群状态数据存储：集群配置，集群状态信息等
2. 保证集群一致性和高可用：多实例的数据同步
3. 服务发现和配置共享
4. 集群数据备份和恢复

作为 Kubernetes 的核心组件，etcd 为集群的稳定性、可靠性和一致性提供了支撑。



### 安装

#### 命令行启动

安装参考官方文档 [etcd install](https://etcd.io/docs/v3.5/install/) 指引即可，安装后验证：

```sh
$ etcd --version
```

输出：

```sh
etcd Version: 3.5.10
Git SHA: 0223ca52b
Go Version: go1.21.3
Go OS/Arch: darwin/arm64
phoenix@xiaobindeMacBook-Pro ~ % etcd
```

在终端启动 etcd：

```sh
$ etcd
```

输出：

```sh
{"level":"warn","ts":"2023-11-23T06:59:49.265098+0800","caller":"embed/config.go:676","msg":"Running http and grpc server on single port. This is not recommended for production."}
{"level":"info","ts":"2023-11-23T06:59:49.265318+0800","caller":"etcdmain/etcd.go:73","msg":"Running: ","args":["etcd"]}
{"level":"info","ts":"2023-11-23T06:59:49.265352+0800","caller":"etcdmain/etcd.go:100","msg":"failed to detect default host","error":"default host not supported on darwin_arm64"}
{"level":"warn","ts":"2023-11-23T06:59:49.265361+0800","caller":"etcdmain/etcd.go:105","msg":"'data-dir' was empty; using default","data-dir":"default.etcd"}
#.....
```

#### 容器启动

在容器中启动 etcd 实例：

```sh
$ docker run -d registry.aliyuncs.com/google_containers/etcd:3.5.0-0 /usr/local/bin/etcd
```

进入 etcd 容器：

```sh
docker ps|grep etcd
docker exec –it <containerid> sh
```

### 使用

`etcd` 的使用较为简单，主要通过 `etcdctl` 来执行日常操作

#### 查看集群

查看 etcd 集群中的所有成员：

```sh
$ etcdctl member list --write-out=table
```

输出：

```sh
+------------------+---------+---------+-----------------------+-----------------------+------------+
|        ID        | STATUS  |  NAME   |      PEER ADDRS       |     CLIENT ADDRS      | IS LEARNER |
+------------------+---------+---------+-----------------------+-----------------------+------------+
| 8e9e05c52164694d | started | default | http://localhost:2380 | http://localhost:2379 |      false |
+------------------+---------+---------+-----------------------+-----------------------+------------+
```

#### 存储键值对

通过 `put` 命令用于将指定的值存储在指定的键下。使用方法如下：

```sh
$ etcdctl put [key] [value]
```

例如，要存储键为 `mykey` 和值为 `myvalue` 的键值对，你可以运行：

```sh
$ etcdctl put mykey myvalue
```

输出：

```sh
OK
```

这会在 `etcd` 中创建或更新键 `mykey` 的值为 `myvalue`。

#### 获取键值对

`get` 命令用于检索存储在指定键下的值。使用方法如下：

```sh
$ etcdctl get [key]
```

继续上面的例子，要获取 `mykey` 的值，你可以运行：

```sh
$ etcdctl get mykey
```

输出：

```sh
mykey
myvalue
```

#### 观察键值变化

通过 `watch` 命令可以观察键的变化。当指定的键发生变化（例如更新或删除）时，会输出通知。使用方法如下：

```sh
$ etcdctl watch [key]
```

例如，要观察 `mykey` 的变化，你可以运行：

```sh
$ etcdctl watch mykey
```

然后，在另一个终端更新 `mykey` 操作：

```sh
$ etcdctl put mykey newValue
$ etcdctl put mykey newValue2
$ etcdctl put mykey newValue3
```

然后执行 `watch` 命令的终端输出：

```sh
PUT
mykey
newValue
PUT
mykey
newValue2
PUT
mykey
newValue3
```

#### 租约机制

租约（Lease）是一种允许将键值对与一个有时间限制的租约关联的机制。租约到期后，与其关联的键值对会自动删除。

这个特性主要用于：保存临时配置，实现分布式锁，心跳机制，集群成员管理等场景。

##### 创建租约

使用 `lease grant` 命令可以创建一个租约：

```sh
$ etcdctl lease grant 60
```

输出：

```sh
lease 694d8c03cd2f520c granted with TTL(60s)
```

这个命令会创建一个持续 60 秒的租约，并且返回一个租约 ID，用于后续的操作。

##### 列出所有租约

使用 `lease list` 可以查看所有活跃的租约：

```sh
$ etcdctl lease list
```

输出：

```sh
found 1 leases
694d8c03cd2f520c
```

这里列出当前所有活跃的租约

##### 将键绑定到租约

使用 `--lease=<LEASE_ID>` 选项参数可以把键绑定在租约上：

```sh
$ etcdctl put mykey myvalue --lease=694d8c03cd2f520c
```

输出：

```sh
OK
```

这个键将在租约到期时自动删除。

##### 保持活跃

使用 `lease keep-alive` 可以对租约进行续租：

```sh
$ etcdctl lease keep-alive 694d8c03cd2f520c
```

输出：

```sh
lease 694d8c03cd2f5214 keepalived with TTL(60)
lease 694d8c03cd2f5214 keepalived with TTL(60)
lease 694d8c03cd2f5214 keepalived with TTL(60)
# ....
```

这条命令将保持租约活跃，防止其到期。

##### 撤销租约

使用 `lease revoke` 可以提前结束租约：

```sh
$ etcdctl lease revoke 694d8c03cd2f520c
```

输出：

```sh
lease 694d8c03cd2f520c revoked
```

这将撤销租约并删除所有与之相关联的键。

#### 备份和恢复

在 etcd 中，`snapshot` 功能是一种重要的数据保护和恢复机制。它允许你保存 `etcd` 数据库的当前状态，并在需要时从这些快照中恢复数据。

##### 创建快照

使用 `etcdctl snapshot save` 命令可以创建当前的数据快照：

```sh
$ etcdctl snapshot save snapshot.db
```

输出：

```sh
{"level":"info","ts":"2023-11-25T11:05:38.646873+0800","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"snapshot.db.part"}
{"level":"info","ts":"2023-11-25T11:05:38.652861+0800","logger":"client","caller":"v3@v3.5.10/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2023-11-25T11:05:38.653092+0800","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"127.0.0.1:2379"}
{"level":"info","ts":"2023-11-25T11:05:38.657127+0800","logger":"client","caller":"v3@v3.5.10/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2023-11-25T11:05:38.660291+0800","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"127.0.0.1:2379","size":"98 kB","took":"now"}
{"level":"info","ts":"2023-11-25T11:05:38.660394+0800","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"snapshot.db"}
```

这会将当前 etcd 数据库的状态保存到名为 `snapshot.db` 的文件中。

##### 恢复数据

使用 `etcdctl snapshot restore` 命令可以从快照文件中恢复数据：

```sh
$ etcdctl snapshot restore snapshot.db
```

输出：

```sh
2023-11-25T11:06:10+08:00 info  snapshot/v3_snapshot.go:260 restoring snapshot  {"path": "snapshot.db", "wal-dir": "default.etcd/member/wal", "data-dir": "default.etcd", "snap-dir": "default.etcd/member/snap"}
2023-11-25T11:06:10+08:00 info  membership/store.go:141 Trimming membership information from the backend...
2023-11-25T11:06:10+08:00 info  membership/cluster.go:421 added member  {"cluster-id": "cdf818194e3a8c32", "local-member-id": "0", "added-peer-id": "8e9e05c52164694d", "added-peer-peer-urls": ["http://localhost:2380"]}
2023-11-25T11:06:10+08:00 info  snapshot/v3_snapshot.go:287 restored snapshot {"path": "snapshot.db", "wal-dir": "default.etcd/member/wal", "data-dir": "default.etcd", "snap-dir": "default.etcd/member/snap"}
```

这会从 `snapshot.db` 中恢复数据，并且配置新的 etcd 实例。



#### 在 K8S 中创建 etcd

##### 安装 Helm

首先，安装 [Helm 包管理工具](https://github.com/helm/helm/releases)，它主要用于简化 Kubernetes 应用程序的部署和管理。

##### 添加 bitnami 仓库

然后将 Bitnami 仓库添加到你的 Helm 包中：

```sh
$ helm repo add bitnami https://charts.bitnami.com/bitnami
```

Bitnami 提供了许多预打包的 K8S 应用和服务，添加它你可以方便的搜索、配置和安装各种安全可靠的应用。

##### 下载 chart

从 Bitnami 仓库下载解压编辑 `etcd` 的 Helm chart：

```sh
$ helm pull bitnami/etcd
$ tar -xvf etcd-6.8.4.tgz
$ vi etcd/values.yaml
```

在本地环境为了避免产生不必要的数据文件，将数据持久化设置为 false：

```sh
persistence:
  ## @param persistence.enabled If true, use a Persistent Volume Claim. If false, use emptyDir.
  enabled: false
```

这意味着 etcd 数据不会被持久化存储，当 Pod 重启时数据会丢失。



##### 安装 chart

将 chart 部署到 Kubernetes 集群中：

```sh
$ helm install my-release ./etcd
```

执行这个命令，Helm 会根据位于 `/etcd` 目录中的 `values.yaml` 文件和其他 chart 文件，创建一组 Kubernetes 资源来部署 etcd 应用。

##### 启动 etcd 客户端

启动 etcd 客户端：

```sh
$ kubectl run my-release-etcd-client --restart='Never' --image docker.io/bitnami/etcd:3.5.0-debian-10-r94 --env ROOT_PASSWORD=$(kubectl get secret --namespace default my-release-etcd -o jsonpath="{.data.etcd-root-password}" | base64 --decode) --env ETCDCTL_ENDPOINTS="my-release-etcd.default.svc.cluster.local:2379" --namespace default --command -- sleep infinity
```

此命令创建一个 etcd 客户端 Pod，用于和 etcd 服务进行交互。

##### 验证

首先查看 Pod：

```sh
$ kubectl get pod
```

输出：

```sh
NAME                     READY   STATUS    RESTARTS   AGE
my-release-etcd-0        1/1     Running   0          7m28s
my-release-etcd-client   1/1     Running   0          74s
```

进入容器：

```sh
$ kubectl exec --namespace default -it my-release-etcd-client -- bash
```

存储键：

```sh
$ etcdctl --user root:$ROOT_PASSWORD put /message Hello
```

获取键：

```sh
$ etcdctl --user root:$ROOT_PASSWORD get /message
```

输出：

```sh
/message
Hello
```

到这里在 K8S 中创建 etcd，从设置环境、安装 etcd，到通过客户端验证的基本使用到这里就完成了。