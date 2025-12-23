+++
date = '2023-12-13T14:09:57+08:00'
draft = false
title = 'Understanding Kubernetes Controller Manager'
tags = ["Cloud Native"]
+++

### The Control Loop

The **Controller Manager** is the "brain" of the control plane. It runs various controllers that watch the state of the cluster and make changes to move the **actual state** toward the **desired state**.

**Workflow:**
1. **Watch**: Observe current state via the API Server.
2. **Reconcile**: Compare actual state (e.g., 2 Pods running) with desired state (e.g., 3 Pods requested).
3. **Action**: Issue commands to the API Server to reach the target (e.g., create 1 Pod).

### Key Controllers

- **Deployment Controller**: Manages ReplicaSets and ensures the correct number of Pods are running.
- **Node Controller**: Monitors node health and handles evictions.
- **Job/CronJob Controllers**: Manage one-time or scheduled tasks.
- **Cloud Controller Manager**: Integrates with cloud provider APIs to manage storage, load balancers, and network routes.

### Kubelet and Runtimes

**Kubelet** is the agent running on every node. It receives PodSpecs from the API Server and ensures they are running.

- **CRI (Container Runtime Interface)**: A plugin interface that allows K8s to use different runtimes like `containerd`, `CRI-O`, or `Docker`.
- **OCI (Open Container Initiative)**: Standards for container images and runtimes.
- **containerd**: A lightweight industry-standard runtime that K8s uses directly to improve performance and stability.

### Networking (CNI)

**CNI (Container Network Interface)** handles networking for Pods.
- **Overlay Networks**: Like **Flannel**, which creates a simple virtual network across nodes.
- **BGP-based Networks**: Like **Calico**, which uses standard routing protocols for higher performance and sophisticated security policies.

### Storage (CSI)

**CSI (Container Storage Interface)** standardizes how K8s talks to external storage (AWS EBS, NFS, Ceph).

**Concepts:**
- **PersistentVolume (PV)**: A piece of storage in the cluster.
- **PersistentVolumeClaim (PVC)**: A request for storage by a user.
- **StorageClass**: Automates the creation of PVs (Dynamic Provisioning).

### Summary

The stability of a Kubernetes cluster relies on these distributed control loops. By decoupling storage (CSI), networking (CNI), and runtimes (CRI), Kubernetes maintains a highly extensible and vendor-neutral architecture.
