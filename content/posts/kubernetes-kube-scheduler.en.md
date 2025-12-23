+++
date = '2023-11-29T14:21:48+08:00'
draft = false
title = 'Understanding Kubernetes Scheduler'
tags = ["Cloud Native"]
+++

### 1. Overview

The **kube-scheduler** is the matchmaker of Kubernetes. Its job is to find the best Node for every newly created Pod. 

It considers:
- **Resource availability**: CPU/Memory/Storage.
- **Affinity and Anti-affinity**: Do Pods want to be together or apart?
- **Taints and Tolerations**: Should a Node repel certain Pods?
- **Priorities**: Which Pod is more important?

### 2. Resource Management

Inside the `resources` section of a PodSpec:
- **Requests**: What the container *needs*. The scheduler uses this value to find a node.
- **Limits**: What the container *is allowed to use*. Enforced at runtime by the Cgroup.

**LimitRange**: A cluster resource to enforce default, min, and max requests/limits for all Pods in a namespace.

### 3. Pre-startup Hooks: initContainers

**initContainers** run before any app containers start. They must exit successfully (with code 0).
- **Use cases**: Initializing files, waiting for database migrations, or checking for internal network ready.
- **Scheduler's role**: It ensures the Node has enough resources to run the init containers *and* the main containers.

### 4. Directing Placement

#### nodeSelector
The simplest constraint. Pods will only run on nodes with matching labels.
```yaml
nodeSelector:
  disktype: ssd
```

#### Node Affinity
More expressive than `nodeSelector`. Supporting logic like "NotIn" or "Exists".
- **RequiredDuringScheduling**: Strict requirement (Hard affinity).
- **PreferredDuringScheduling**: Weight-based preference (Soft affinity).

#### Pod Affinity and Anti-Affinity
Allows placement based on which Pods are *already* running on a node.
- **Affinity**: Together (e.g., placing Web and Cache together).
- **Anti-Affinity**: Apart (e.g., ensuring replicas of the same app are on different nodes for high availability).

### 5. Repelling Pods: Taints and Tolerations

Taints are applied to **Nodes**. Tolerations are applied to **Pods**.
- **NoSchedule**: New Pods won't start on this node unless they tolerate the taint.
- **NoExecute**: Existing Pods will be evicted if they don't tolerate the taint.

Useful for:
- Dedicated nodes (e.g., GPU only).
- Maintenance (Evicting all pods).
- Handling hardware failure.

### 6. PriorityClass

Defines the relative importance of Pods.
- Higher value = higher priority.
- If resources are scarce, the scheduler will evict lower-priority Pods to schedule a higher-priority one (**Preemption**).

### 7. Custom Schedulers

If you have highly specialized needs (e.g., batch scheduling for AI), you can run multiple schedulers in one cluster. Specify which one to use via `schedulerName` in your deployment YAML.

### Summary

The scheduler is a complex decision engine that ensures your workload is distributed fairly, efficiently, and according to your specific business rules.
