+++
date = '2023-11-25T14:29:56+08:00'
draft = false
title = 'Understanding Kubernetes Etcd'
tags = ["Cloud Native"]
+++

### Overview

etcd is an open-source, distributed key-value storage system based on the Raft protocol. It is primarily used to provide strong consistency and high availability for data storage in distributed systems. Its roles in Kubernetes include:

1. **Cluster State Data Storage**: Cluster configurations, cluster state information, etc.
2. **Ensuring Cluster Consistency and High Availability**: Data synchronization across multiple instances.
3. **Service Discovery and Configuration Sharing**.
4. **Cluster Data Backup and Recovery**.

As a core component of Kubernetes, etcd provides the foundation for the cluster's stability, reliability, and consistency.

### Installation

#### Command-Line Startup

Refer to the official [etcd install](https://etcd.io/docs/v3.5/install/) guide for installation. Verify after installation:

```sh
$ etcd --version
```

Output:

```sh
etcd Version: 3.5.10
Git SHA: 0223ca52b
Go Version: go1.21.3
Go OS/Arch: darwin/arm64
```

Start etcd in the terminal:

```sh
$ etcd
```

Output:

```sh
{"level":"warn","ts":"2023-11-23T06:59:49.265098+0800","caller":"embed/config.go:676","msg":"Running http and grpc server on single port. This is not recommended for production."}
{"level":"info","ts":"2023-11-23T06:59:49.265318+0800","caller":"etcdmain/etcd.go:73","msg":"Running: ","args":["etcd"]}
{"level":"info","ts":"2023-11-23T06:59:49.265352+0800","caller":"etcdmain/etcd.go:100","msg":"failed to detect default host","error":"default host not supported on darwin_arm64"}
{"level":"warn","ts":"2023-11-23T06:59:49.265361+0800","caller":"etcdmain/etcd.go:105","msg":"'data-dir' was empty; using default","data-dir":"default.etcd"}
#.....
```

#### Container Startup

Start an etcd instance in a container:

```sh
$ docker run -d registry.aliyuncs.com/google_containers/etcd:3.5.0-0 /usr/local/bin/etcd
```

Enter the etcd container:

```sh
docker ps|grep etcd
docker exec –it <containerid> sh
```

### Usage

Using `etcd` is relatively straightforward, primarily through `etcdctl` for daily operations.

#### Viewing the Cluster

View all members of the etcd cluster:

```sh
$ etcdctl member list --write-out=table
```

Output:

```sh
+------------------+---------+---------+-----------------------+-----------------------+------------+
|        ID        | STATUS  |  NAME   |      PEER ADDRS       |      CLIENT ADDRS     | IS LEARNER |
+------------------+---------+---------+-----------------------+-----------------------+------------+
| 8e9e05c52164694d | started | default | http://localhost:2380 | http://localhost:2379 |      false |
+------------------+---------+---------+-----------------------+-----------------------+------------+
```

#### Storing Key-Value Pairs

The `put` command is used to store a specified value under a specified key. The usage is as follows:

```sh
$ etcdctl put [key] [value]
```

For example, to store a key-value pair of `mykey` and `myvalue`, you can run:

```sh
$ etcdctl put mykey myvalue
```

Output:

```sh
OK
```

This will create or update the value for the key `mykey` to `myvalue` in `etcd`.

#### Getting Key-Value Pairs

The `get` command is used to retrieve the value stored under a specified key. Usage:

```sh
$ etcdctl get [key]
```

Continuing with the example above, to get the value for `mykey`, run:

```sh
$ etcdctl get mykey
```

Output:

```sh
mykey
myvalue
```

#### Watching Key Changes

The `watch` command allows you to observe changes to a key. Notifications are output when the specified key changes (e.g., an update or deletion). Usage:

```sh
$ etcdctl watch [key]
```

For example, to observe changes to `mykey`, run:

```sh
$ etcdctl watch mykey
```

Then, in another terminal, update `mykey`:

```sh
$ etcdctl put mykey newValue
$ etcdctl put mykey newValue2
$ etcdctl put mykey newValue3
```

The terminal executing the `watch` command will output:

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

#### Lease Mechanism

A Lease is a mechanism that allows associating key-value pairs with a time-limited lease. Once the lease expires, the associated key-value pairs are automatically deleted.

This feature is primarily used for: saving temporary configurations, implementing distributed locks, heartbeat mechanisms, cluster member management, etc.

##### Creating a Lease

Use the `lease grant` command to create a lease:

```sh
$ etcdctl lease grant 60
```

Output:

```sh
lease 694d8c03cd2f520c granted with TTL(60s)
```

This command creates a lease for 60 seconds and returns a lease ID for subsequent operations.

##### Listing All Leases

Use `lease list` to view all active leases:

```sh
$ etcdctl lease list
```

Output:

```sh
found 1 leases
694d8c03cd2f520c
```

This lists all currently active leases.

##### Binding a Key to a Lease

Use the `--lease=<LEASE_ID>` option to bind a key to a lease:

```sh
$ etcdctl put mykey myvalue --lease=694d8c03cd2f520c
```

Output:

```sh
OK
```

This key will be automatically deleted when the lease expires.

##### Keeping Alive

Use `lease keep-alive` to renew the lease:

```sh
$ etcdctl lease keep-alive 694d8c03cd2f520c
```

Output:

```sh
lease 694d8c03cd2f5214 keepalived with TTL(60)
lease 694d8c03cd2f5214 keepalived with TTL(60)
lease 694d8c03cd2f5214 keepalived with TTL(60)
# ....
```

This command keeps the lease active, preventing it from expiring.

##### Revoking a Lease

Use `lease revoke` to end a lease early:

```sh
$ etcdctl lease revoke 694d8c03cd2f520c
```

Output:

```sh
lease 694d8c03cd2f520c revoked
```

This revokes the lease and deletes all keys associated with it.

#### Backup and Recovery

In etcd, the `snapshot` feature is an important mechanism for data protection and recovery. It allows you to save the current state of the `etcd` database and restore data from these snapshots when needed.

##### Creating a Snapshot

Use the `etcdctl snapshot save` command to create a snapshot of the current data:

```sh
$ etcdctl snapshot save snapshot.db
```

Output:

```sh
{"level":"info","ts":"2023-11-25T11:05:38.646873+0800","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"snapshot.db.part"}
{"level":"info","ts":"2023-11-25T11:05:38.652861+0800","logger":"client","caller":"v3@v3.5.10/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2023-11-25T11:05:38.653092+0800","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"127.0.0.1:2379"}
{"level":"info","ts":"2023-11-25T11:05:38.657127+0800","logger":"client","caller":"v3@v3.5.10/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2023-11-25T11:05:38.660291+0800","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"127.0.0.1:2379","size":"98 kB","took":"now"}
{"level":"info","ts":"2023-11-25T11:05:38.660394+0800","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"snapshot.db"}
```

This saves the current etcd database state to a file named `snapshot.db`.

##### Restoring Data

Use the `etcdctl snapshot restore` command to restore data from a snapshot file:

```sh
$ etcdctl snapshot restore snapshot.db
```

Output:

```sh
2023-11-25T11:06:10+08:00 info  snapshot/v3_snapshot.go:260 restoring snapshot  {"path": "snapshot.db", "wal-dir": "default.etcd/member/wal", "data-dir": "default.etcd", "snap-dir": "default.etcd/member/snap"}
2023-11-25T11:06:10+08:00 info  membership/store.go:141 Trimming membership information from the backend...
2023-11-25T11:06:10+08:00 info  membership/cluster.go:421 added member  {"cluster-id": "cdf818194e3a8c32", "local-member-id": "0", "added-peer-id": "8e9e05c52164694d", "added-peer-peer-urls": ["http://localhost:2380"]}
2023-11-25T11:06:10+08:00 info  snapshot/v3_snapshot.go:287 restored snapshot {"path": "snapshot.db", "wal-dir": "default.etcd/member/wal", "data-dir": "default.etcd", "snap-dir": "default.etcd/member/snap"}
```

This restores data from `snapshot.db` and configures a new etcd instance.

#### Creating etcd in K8S

##### Installing Helm

First, install the [Helm package management tool](https://github.com/helm/helm/releases). It's primarily used to simplify the deployment and management of Kubernetes applications.

##### Adding the bitnami Repository

Then, add the Bitnami repository to your Helm packages:

```sh
$ helm repo add bitnami https://charts.bitnami.com/bitnami
```

Bitnami provides many pre-packaged K8S applications and services. Adding it allows you to easily search, configure, and install various secure and reliable applications.

##### Downloading the Chart

Download, extract, and edit the `etcd` Helm chart from the Bitnami repository:

```sh
$ helm pull bitnami/etcd
$ tar -xvf etcd-6.8.4.tgz
$ vi etcd/values.yaml
```

To avoid generating unnecessary data files in a local environment, set data persistence to false:

```yaml
persistence:
  ## @param persistence.enabled If true, use a Persistent Volume Claim. If false, use emptyDir.
  enabled: false
```

This means etcd data will not be persistently stored, and data will be lost when the Pod restarts.

##### Installing the Chart

Deploy the chart into the Kubernetes cluster:

```sh
$ helm install my-release ./etcd
```

Executing this command causes Helm to create a set of Kubernetes resources to deploy the etcd application based on the `values.yaml` file in the `/etcd` directory and other chart files.

##### Starting the etcd Client

Start the etcd client:

```sh
$ kubectl run my-release-etcd-client --restart='Never' --image docker.io/bitnami/etcd:3.5.0-debian-10-r94 --env ROOT_PASSWORD=$(kubectl get secret --namespace default my-release-etcd -o jsonpath="{.data.etcd-root-password}" | base64 --decode) --env ETCDCTL_ENDPOINTS="my-release-etcd.default.svc.cluster.local:2379" --namespace default --command -- sleep infinity
```

This command creates an etcd client Pod used to interact with the etcd service.

##### Verification

First, check the Pod:

```sh
$ kubectl get pod
```

Output:

```sh
NAME                     READY   STATUS    RESTARTS   AGE
my-release-etcd-0         1/1     Running   0          7m28s
my-release-etcd-client    1/1     Running   0          74s
```

Enter the container:

```sh
$ kubectl exec --namespace default -it my-release-etcd-client -- bash
```

Store a key:

```sh
$ etcdctl --user root:$ROOT_PASSWORD put /message Hello
```

Get a key:

```sh
$ etcdctl --user root:$ROOT_PASSWORD get /message
```

Output:

```sh
/message
Hello
```

That's it for creating etcd in K8S—from setting up the environment and installing etcd to basic verification via the client.
