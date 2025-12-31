+++
date = '2023-12-13T14:09:57+08:00'
draft = false
title = 'Understanding the Kubernetes Controller Manager'
tags = ["Cloud Native"]
+++

### Controller Manager

The Controller Manager is a vital component of the control plane, responsible for maintaining the overall state of the Kubernetes cluster.

Process:

![image-20231210114754993](https://s2.loli.net/2025/02/13/rSdl17DbLjKoaHB.png)

In the cluster, the Controller Manager primarily performs the following tasks:

- **Watch**: The Controller Manager watches for changes in resource states within the cluster via the API Server. It receives notifications whenever a resource state changes.
- **Decide**: Based on resource definitions and their current states, the Controller Manager makes decisions. For example, if the number of Pods for a Deployment falls below the expected count, it decides to create new Pods.
- **Act**: It executes necessary operations based on those decisions. For instance, to create a new Pod, the Controller Manager calls the API Server.

#### Common Controllers

Kubernetes includes many built-in controllers. When resource states change, the Controller Manager notifies these controllers to make decisions and act:

-   **Deployment Controller**: Responsible for deploying and managing Pod replicas.
-   **ReplicaSet Controller**: Manages the number of Pod replicas.
-   **DaemonSet Controller**: Ensures that a specified Pod runs on every node.
-   **Job Controller**: Manages one-time tasks.
-   **CronJob Controller**: Manages tasks that run at specified intervals.
-   **StatefulSet Controller**: Ensures the ordering and persistence of Pods.

**Cloud Controller Manager**

When deploying Kubernetes in the cloud, the cluster needs to connect with the cloud platform to use resources like virtual machines, load balancers, and storage volumes. The Cloud Controller Manager provides this connectivity, using cloud platform APIs to create and manage resources. It is mainly used in these scenarios:

-   Deploying Kubernetes clusters in a cloud environment.
-   Associating Kubernetes resources with cloud platform resources (e.g., linking Pods in a Deployment with VMs).
-   Monitoring cloud resource states and keeping them consistent with Kubernetes resource states.

#### kubelet

Kubelet is the node agent within a Kubernetes cluster, running on every node and responsible for running Pods on that node:

![image-20231210160441907](https://s2.loli.net/2025/02/13/JK2t89cCheBYod4.png)

Explanation:

In the diagram, the kubelet communicates with the cluster's control plane via the API Server. It retrieves Pod definitions from the API Server and creates/manages containers accordingly.

Additionally, the kubelet is responsible for:

-   Retrieving Pod definitions from the Kubernetes API Server.
-   Creating and managing containers using a Container Runtime.
-   Monitoring Pod health.
-   Periodically checking Pod status and taking appropriate actions.
-   Reporting Pod status to the Kubernetes API Server.

Detailed Pod Startup Flow:

![image-20231210162241039](https://s2.loli.net/2025/02/13/jEyON3roK7fg8n6.png)

Explanation:

1.  **Create Pod**: A user sends a request to the API Server to create a Pod.
2.  **API Server Updates etcd**: The API Server writes the new Pod information to etcd.
3.  **Scheduler Watches New Pod**: The Scheduler watches for new Pods in etcd via a watch mechanism.
4.  **Scheduler Binds Pod**: The Scheduler selects a suitable node and binds the Pod to it.
5.  **API Server Updates etcd**: The Scheduler writes the binding information back to etcd.
6.  **Kubelet Watches Bound Pod**: The Kubelet detects a new Pod bound to the node it manages.
7.  **Kubelet Runs Pod**: The Kubelet begins running the Pod on the node through these steps:
    -   **RunPodSandbox**: Creates the network and storage sandbox environment for the Pod.
    -   **PullImage**: Pulls the container image from the registry.
    -   **CreateContainer**: Creates the container.
    -   **StartContainer**: Starts the container.
8.  **Network Plugin Sets Up Pod Network**: The network plugin sets up the Pod's network, such as assigning IP addresses.
9.  **Update Pod Status**: The Kubelet updates the Pod status and notifies the API Server, which then updates the status in etcd.

The entire process is automated, completed through the coordination of various Kubernetes components.

### CRI

Before the CRI (Container Runtime Interface), Kubernetes was tightly coupled with the Docker runtime, meaning it could only use Docker to manage containers. The introduction of CRI changed this. CRI is a plugin interface for Kubernetes clusters, running on every node, which allows the kubelet to use various container runtimes without recompilation:

![image-20231210164710033](https://s2.loli.net/2025/02/13/nGLIyWca9d5XKUH.png)

Main reasons for using CRI include:

1.  **Runtime Standardization**: CRI provides a standard way for different runtimes (like Docker, containerd, CRI-O, etc.) to interact with Kubernetes. Users can choose the runtime that best fits their needs.
2.  **Decoupling**: Previously, runtime logic was hardcoded in Kubernetes. With CRI, the coupling is reduced, and runtimes can update and iterate independently of Kubernetes releases.
3.  **Extensibility**: CRI opens the door for innovation, as different teams can develop and optimize their own runtimes as long as they follow the CRI specification.

#### CRI Definition

CRI is a set of interface specifications defined by Kubernetes via the gRPC protocol.

![image-20231210165835899](https://s2.loli.net/2025/02/13/rntXBNOSoglGfw7.png)

Understanding CRI as gRPC services involves:

-   **gRPC and Protocol Buffers**:
    -   Uses Protocol Buffers as the Interface Definition Language (IDL) to define services and message formats.
    -   Protocol Buffers is a language-neutral, platform-neutral serialization framework.
-   CRI includes two main services:
    -   `RuntimeService`: Manages Pod and container lifecycles (create, start, stop containers, etc.).
    -   `ImageService`: Manages images (pulling, listing, deleting container images).

#### OCI Specification

In the early days of container technology, every runtime used its own format and interface, leading to a lack of interoperability. To solve this, Docker, CoreOS, and appc maintainers launched the OCI project in June 2015. OCI aims to define standards for container formats and runtimes.

OCI consists of two main parts:

-   **Image Specification**: Defines the format of the container image.
-   **Runtime Specification**: Defines the container runtime interface.

![image-20231210171626184](https://s2.loli.net/2025/02/13/i8H3PGE6bjAIcJ9.png)

**Image Specification**:
Describes the structure and content of a container image, defining the root filesystem, environment variables, startup commands, etc. It allows different runtimes to understand and use the same image.

**Runtime Specification**:
Defines how a container runtime creates, starts, stops, and deletes containers. It enables container orchestration systems like Kubernetes to interact with various runtimes.

Benefits of OCI:
-   Promotes container interoperability.
-   Reduces development and deployment costs.
-   Enhances security and reliability.

#### containerd

`containerd` is a core component of Docker. Since it adheres to OCI standards, it can be used independently of Docker in Kubernetes.

![image-20231210172835256](https://s2.loli.net/2025/02/13/UpqDkY7cm2KadXO.png)

##### Advantages

Why is it recommended to use containerd independently in Kubernetes?

-   **Lightweight and Efficient**: `containerd` provides the essential core features for running containers without Docker's extra bells and whistles, making it lightweight—ideal for edge computing or microservices.
-   **Lower Resource Consumption**: Compared to the full Docker engine, `containerd` uses fewer system resources (CPU, memory).
-   **Adheres to Standards**: It fully follows OCI standards and works seamlessly with OCI-compliant images and runtime interfaces like CRI.
-   **Simplification**: In Kubernetes, many Docker engine features are redundant. Using `containerd` simplifies the setup and reduces overhead.

Independently using `containerd` also helps with troubleshooting. Here are three ways container runtimes interact with the kubelet:

![image-20231210172944007](https://s2.loli.net/2025/02/13/lGhfu3vTCoWE4x2.png)

Due to OCI, Kubernetes no longer depends on Docker as the sole runtime and can support runtimes like containerd and CRI-O, increasing flexibility and reducing architectural complexity.

##### Differences

Differences between using Docker and containerd as runtimes in Kubernetes:

![image-20231210173721674](https://s2.loli.net/2025/02/13/GkpZQc98I4MnCSL.png)

Explanation: OCI standardizes the runtime layer, reducing extra abstraction layers.

##### Performance

containerd's performance consistently exceeds expectations:

![image-20231210174000326](https://s2.loli.net/2025/02/13/SWNAywqlD6vVJCa.png)

Comparison of runtimes:

![image-20231210174043727](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9cb8cead0fdc4c898187a5b45da4a45e~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2042&h=528&s=61291&e=png&b=ffffff)

### CNI

Before CNI (Container Network Interface), different runtimes (Docker, rkt) had their own network configuration methods, causing compatibility and portability issues. CNI provides a standard set of interfaces and plugins for configuring container networking across different environments. CNI solved:

1.  Standardization of container network configuration.
2.  Simplified cluster management.
3.  Pluggable network solutions.
4.  Dynamic networking for container orchestration.

#### CNI Plugins

To support complex scenarios in cloud-native environments, CNI uses a modular (plugin-based) design.

CNI plugins are categorized as:

-   **Main plugins**: Responsible for creating, configuring, and deleting network interfaces. Some also manage routing and firewalls.
-   **IPAM (IP Address Management)**: Assigns IP addresses to containers.
-   **Meta plugins**: Special plugins used alongside main plugins for additional features.

Common Main plugins:
-   **bridge**: Creates a network bridge and connects containers to it.
-   **ipvlan**: Similar to macvlan but based on IP rather than MAC.
-   **loopback**: Configures the container's loopback device.

Meta (Additional features):
-   **portmap**: Maps ports between host and container.
-   **bandwidth**: Limits container bandwidth using Linux tc.
-   **firewall**: Sets firewall rules for containers using iptables or firewalld.

#### Execution Mechanism

Plugins are designed to configure and clean up networking during container initialization and destruction:

![image-20231210194500175](https://s2.loli.net/2025/02/13/QajqO27IPpLxCiV.png)

Explanation:

1.  **Initialize container network (ADD operator)**:
    -   When a container is created, the runtime calls the CNI plugin with an ADD command.
    -   The kubelet builds a JSON configuration with container and network details and passes it to the plugin.
    -   The plugin reads it and performs the setup.
    -   If an IPAM plugin is specified, it is called to assign IP addresses, subnets, etc.
    -   The plugin connects the container to the network and applies isolation policies.
2.  **Clean up container network (DEL operator)**:
    -   When a container is destroyed, the runtime calls the plugin with a DEL command.
    -   The plugin cleans up based on the JSON config (removes interfaces, releases IPs, clears routes).
    -   If IPAM was used, it releases the IP.

The core of the mechanism is providing a standard way to manage networking across different runtimes and orchestrators while maintaining consistency.

#### Configuration Directories

In CNI context, `cni-bin-dir` and `cni-conf-dir` are crucial directories used by the kubelet.

**cni-bin-dir**:
Contains executable files for all CNI plugins. Kubelet calls these when initializing a network. Typical files include `bridge`, `loopback`, and `host-local`. Default is usually `/opt/cni/bin`.

**cni-conf-dir**:
Contains CNI configuration files ending in `.conf` or `.conflist`. These define parameters like network name, subnet, IP range, gateway, and plugins used. Default is usually `/etc/cni/net.d`.

The kubelet checks these at startup. You can specify them with `--cni-bin-dir` and `--cni-conf-dir` flags.

#### Flannel

Flannel is a simple overlay network solution that addresses:
1.  **Cross-host container communication**.
2.  **Simplified network configuration** (assigns subnets to nodes automatically).
3.  **Ease of deployment**.
4.  **Network isolation** via independent IP addresses for Pods.
5.  **Compatibility** with any CNI-compliant runtime.

**Best scenarios for Flannel**:
-   Rapidly deploying clusters across multiple hosts.
-   Needing simple Pod-to-Pod communication.
-   Needing automated network management without complex config.
-   Resource-constrained environments (edge computing).

#### Calico

Calico is a widely used high-performance network and security solution, using standard IP routing.

**Why Calico?**:
-   Efficient routing in large-scale environments.
-   Advanced network security policies between Pods and services.
-   Connectivity across multiple clusters.
-   Simplified operations using widely adopted protocols (BGP).

**Features**:
1.  **High Performance**: Uses native routing for near-bare-metal performance.
2.  **Scalability**: Scales to thousands of nodes.
3.  **Security Policies**: Fine-grained control over container communication.
4.  **Network Isolation**: Strict isolation via security policies.
5.  **Hybrid/Multi-cloud support**.
6.  **Standard Compliance**: Uses standard BGP for integration with traditional infrastructure.

**Best scenarios for Calico**:
-   Manage large scale clusters.
-   Enterprise apps requiring complex security policies.
-   Hybrid cloud or multi-datacenter management.
-   Performance-sensitive applications.

#### Plugin Comparison

Comparison of common CNI plugins:

![image-20231210202903172](https://s2.loli.net/2025/02/13/tM7g6Ius1p4cRqw.png)

### CSI

CSI (Container Storage Interface) is the specification responsible for storage management in Kubernetes, decoupling the Container Orchestrator (CO) from storage systems to make storage pluggable.

**Reasons for CSI**:
1.  **Standardization**: Previously, solutions were custom-built per CO; CSI provides a universal interface.
2.  **Independence**: Plugins can be developed and deployed independently of the CO core.
3.  **Decoupling**: Removing storage logic from core code reduces complexity and eases maintenance.

#### CSI Plugins

Kubernetes supports several types:

**In-tree Storage**:
-   Part of Kubernetes source code. No new in-tree plugins are accepted; new ones must be out-of-tree.

**Out-of-tree FlexVolume**:
-   Kubernetes calls executables on nodes to interact with storage.
-   Requires root access and host-level tools (attach, mount).

**Out-of-tree CSI**:
-   Interacts with storage drivers via RPC.

#### CSI Driver

A CSI Driver is a plugin following the CSI spec for volume lifecycle management.

![image-20231210205711631](https://s2.loli.net/2025/02/13/9DU5Fg78PYyhAtd.png)

Components:
-   **External-attacher**: Attaches volumes to nodes.
-   **External-provisioner**: Manages dynamic provisioning (creation/deletion).
-   **External-resizer**: Handles dynamic volume expansion.
-   **External-snapshotter**: Manages volume snapshots.
-   **Node-driver-register**: Registers the driver to the kubelet on each node.
-   **CSI Driver**: The actual component performing storage operations (create, delete, mount).

The driver executes operations called by the external components.

### Temporary Storage

##### emptyDir

Created when a Pod is assigned to a node; exists as long as the Pod runs on that node. It's initially empty and shared between containers in the Pod.

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

Explanation:
1.  Defines `cache-volume` as an `emptyDir` for local temporary storage.
2.  Mounts it to `/cache` in the `nginx` container.

##### hostPath

Mounts a file or directory from the host node's filesystem into the Pod. Persists after Pod deletion.

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

Notes on `hostPath`:
-   **Data Drift**: If the Pod moves to another node, data stays behind.
-   **Data Residue**: Files remain on the host after Pod deletion, wasting space.
-   **Portability**: Depends on specific host paths, reducing portability.
Recommended only for specific use cases, not general production.

### Persistent Storage

Kubernetes uses StorageClass, PV, and PVC to manage storage independently of the Pod lifecycle.

##### PV (PersistentVolume)

A cluster-level resource representing actual storage (NFS, Cloud volume, local disk). PVs are requested via PVCs.

Features:
-   Independent of Pod lifecycle.
-   Reusable across multiple Pods.
-   Static (pre-created) or Dynamic (auto-created via `StorageClass`).
-   Expandable capacity.

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

##### PVC (PersistentVolumeClaim)

A request for storage. Kubernetes finds a matching PV and binds it. Think of PV as the "product" and PVC as the "order".

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

##### Using PVC in a Pod

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

Content in the mounted directory will be persisted.

##### StorageClass

Allows defining storage types and dynamic provisioning properties. When a PVC requests a StorageClass, the PV is created automatically.

![image-20231211070828874](https://s2.loli.net/2025/02/13/BcI7JRymG3NVYsv.png)

**AWS EBS Example StorageClass**:

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

Detailed explanation:
-   `provisioner`: AWS EBS.
-   `gp2`: General Purpose SSD.
-   `reclaimPolicy: Retain`: PV won't be deleted when PVC is deleted.
-   `allowVolumeExpansion`: Allows resizing later.

##### Local Volume

A specific PV that uses storage directly on a node (disk, partition, directory). It is "exclusive" because it can only be used by Pods on that specific node.

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

##### Best Practices

1. Set up different `StorageClasses` for different disk/performance types.
2. For local PVs, try to create only one PV per physical disk to avoid I/O interference.
3. Use disk monitoring for local storage; disk failure is common at scale.
