+++
date = '2023-11-29T14:21:48+08:00'
draft = false
title = 'Understanding the Kubernetes Scheduler'
tags = ["Cloud Native"]
+++

## Overview

The `kube-scheduler` is one of the core components of the Kubernetes cluster, responsible for assigning nodes to newly created Pods. It makes decisions based on various factors, including:

1.  **Resource requirements and constraints**: Considers the amount of resources (such as CPU and memory) requested by each Pod and the available resources on the nodes.
2.  **Affinity and anti-affinity rules**: Selects the most suitable node based on the Pod's affinity settings.
3.  **Health checks**: Ensures the selected node is healthy and capable of running the Pod.
4.  **Load balancing**: Attempts to balance the load across all nodes in the cluster.

## Usage

### limits and requests

In the `spec` of deployment objects, you often see declarations of `limits` and `requests`, for example:

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

Here, `limits` and `requests` are two key concepts related to Pod container resource management:

-   **Limits**: Specifies the maximum amount of resources the container can use at runtime.
-   **Requests**: Specifies the minimum amount of resources required for the container to start.

**What is the relationship between limits/requests and the scheduler?**

Kube-scheduler is the unsung hero working behind the scenes. Its main tasks include:

1. When you create a Deployment like this `nginx`, kube-scheduler decides which Node it should run on.
2. kube-scheduler watches the API Server to get a global view of the cluster and analyzes it based on the Pod's resource requests (`requests` and `limits`).
3. Ultimately, kube-scheduler schedules the Pod by combining resource requests with the actual state of the cluster.

In short, kube-scheduler ensures that a Pod is scheduled to a Node that satisfies its resource requirements.

### LimitRange

**Description**

`LimitRange` is a resource object used to restrict resource usage within a namespace. It can set default resource requests and limits, as well as minimum and maximum values for resource usage. This ensures that every Pod or container follows specific policies, preventing a single Pod from consuming excessive resources. Here is an example: create a YAML file named `mem-limit-range.yaml`.

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

Apply it to the cluster:

```sh
$ kubectl apply -f mem-limit-range.yaml
```

Check the created `LimitRange` object:

```sh
$ kubectl describe limitrange mem-limit-range
```

Output:

```sh
Name:       mem-limit-range
Namespace:  default
Type        Resource  Min  Max  Default Request  Default Limit  Max Limit/Request Ratio
----        --------  ---  ---  ---------------  -------------  -----------------------
Container   memory    -    -    256Mi            512Mi          -
```

Explanation:

-   **Kind**: Set to `LimitRange` to restrict resource usage within the namespace.
-   **Metadata**: Sets the name of the resource.
-   **Spec**:
    -   **Limits**:
    -   **default**: Specifies a default memory limit of 512Mi for containers without explicit resource limits.
    -   **defaultRequest**: Specifies a default memory request of 256Mi for containers without explicit resource requests.
    -   **type**: The type of resource these limits apply to, which is `Container` here.

**Verification**

Define a deployment without resource requests named `nginx-without-resource.yaml`:

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

Apply it:

```sh
$ kubectl apply -f nginx-without-resource.yaml
```

Once the Pod is created, you can confirm if the `LimitRange` is in effect by checking its configuration:

```sh
$ kubectl describe pod [POD_NAME]
```

Output:

```yaml
Containers:
  # ... ignore
    Limits:
      memory:  512Mi
    Requests:
      memory:  256Mi
```

### initContainers

`initContainers` are used to perform preparatory tasks before the main application container starts. They are common in the following scenarios:

1. **Preparation**: Setting up configuration files, database migrations, waiting for other services to be ready, etc.
2. **Security**: Privilege escalation tasks, such as changing file permissions or performing specific security checks.
3. **Service Dependencies**: Waiting for other services or databases to become available.

`initContainers` stop after completing their tasks and must finish successfully before the main container starts. They are perfect for initialization tasks.

Example: Declaring `initContainers` in a deployment:

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

Apply the deployment:

```sh
$ kubectl apply -f init-container.yaml
```

Once the Pod starts, verify the loading order via event logs:

```sh
Events:
  Type    Reason    Age    From                Message
  ----    ------    ----   ----                -------
  Normal  Scheduled  2m20s  default-scheduler  Successfully assigned default/nginx-deployment-6445f86ddc-fmmzw to docker-desktop
  Normal  Pulling    2m20s  kubelet            Pulling image "busybox:1.28"
  Normal  Pulled     116s   kubelet            Successfully pulled image "busybox:1.28" in 23.099396719s
  Normal  Created    116s   kubelet            Created container init-myservice
  Normal  Started    116s   kubelet            Started container init-myservice
  Normal  Pulling    106s   kubelet            Pulling image "nginx"
  Normal  Pulled     88s    kubelet            Successfully pulled image "nginx" in 18.382000675s
  Normal  Created    88s    kubelet            Created container nginx
  Normal  Started    88s    kubelet            Started container nginx
```

You can see the `initContainers` have loaded. Check the specific logs for the Pod output:

```sh
$ kubectl logs [POD_NAME] -c init-myservice
```

Output:

```sh
The app is running!
```

**Relationship between initContainers and kube-scheduler?**

If `initContainers` don't declare resource requests, they will use the defaults from `LimitRange` by default. This means they are also scheduled and created by kube-scheduler. Adding resource requirements to `initContainers` will also influence kube-scheduler's scheduling decisions.

### nodeSelector

In a deployment object, the `nodeSelector` attribute is used to schedule specific Pods to nodes with specific labels. If no node satisfies the requirements, the Pod will remain pending. Example:

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

In this example, the `nodeSelector` is set to `disktype: ssd`. This indicates that the Pod should be scheduled to a Node with the label `disktype=ssd`. Kube-scheduler will look for a suitable node to run this Pod.

Apply it:

```sh
$ kubectl apply -f node-selector.yaml
```

Check the Pod status:

```sh
$ kubectl get pod
```

Output:

```sh
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-f5bc98d57-pmq9v    0/1     Pending   0          2m17s
```

The Pod stays in "Pending". Check the detailed reasons in the event logs:

```sh
$ kubectl describe pod [POD_NAME]
```

Output:

```sh
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  4m38s  default-scheduler  0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector.
```

The log shows that no nodes meet the criteria. In my case, no node is labeled with `disktype: ssd`.

### Affinity

An evolution of `nodeSelector`, Affinity provides more complex selection rules. Beyond simple matching, it supports rich expressions (e.g., "Exists", "Does Not Equal", "In a set"). It supports settings for relationships between Pods (`podAffinity`/`podAntiAffinity`) and between Pods and nodes (`nodeAffinity`). In newer versions of Kubernetes, Affinity has largely replaced `nodeSelector`.

#### **podAffinity**

`podAffinity` defines relationships between Pods, allowing a Pod to be scheduled on the same node as other Pods with specific labels.

**Scenario**: When you want groups of services to work closely together, such as components requiring low-latency communication.

Example:

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

Affinity settings in this file:
- **PodAffinity**: Requires the Pod to reside on the same node as Pods labeled `a=b`.
- **PodAntiAffinity**: Requires the Pod *not* to reside on the same node as other Pods labeled `app=anti-nginx`.

After applying, check the Pod distribution:

```sh
NAME                          READY   STATUS    RESTARTS   AGE   IP      NODE
nginx-anti-5656fcbb98-62mds   0/1     Pending   0          5s    <none>  <none>
nginx-anti-5656fcbb98-wxphs   0/1     Pending   0          5s    <none>  <none>
```

Pods are pending due to affinity rules. Verification in logs:

```sh
Events:
  Warning  FailedScheduling  27s   default-scheduler  0/1 nodes are available: 1 node(s) didn't match pod affinity rules.
```

#### **nodeAffinity**

Defines the relationship between Pods and nodes, controlling placement based on node labels or attributes.

**Scenario**: Scheduling based on hardware features (GPU, SSD) or custom labels (environment tags).

Example:

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

As expected, without the `ssd` tag, the Pod will remain Pending.

**preferredDuringSchedulingIgnoredDuringExecution**

Unlike `requiredDuringScheduling`, this is a preference. The scheduler tries to find a match but will choose another node if no match is found.

Example:

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

Even without an SSD node, this Pod will run:

```sh
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-69c654d896-7qh8t   1/1     Running   0          28s
```

**Summary**:
-   **podAffinity**: Focuses on relationships between Pods.
-   **nodeAffinity**: Focuses on relationships between Pods and node attributes.
    -   **requiredDuringScheduling**: Hard requirement; mandatory rules.
    -   **preferredDuringScheduling**: Soft requirement; preference-based.

### Taints

Taints and Tolerations control which Pods can be scheduled on specific nodes. Unlike Affinity, which is attractive, Taints are **repulsive**—they repel Pods that don't satisfy certain conditions.

Taint effects:
-   `NoSchedule`: No new Pods allowed.
-   `PreferNoSchedule`: Scheduler tries to avoid placing new Pods.
-   `NoExecute`: No new Pods allowed, and existing Pods may be evicted.

Scenarios:
-   Marking nodes as "Exclusive".
-   Multi-tenant resource isolation.
-   Kubernetes using taints to evict Pods from unhealthy nodes.

Example:

Add a taint to a node to prevent normal Pods from scheduling:

```sh
$ kubectl taint nodes docker-desktop for-special-user=cadmin:NoSchedule
```

A normal Pod without tolerations will stay Pending:

```sh
Events:
  Warning  FailedScheduling  56s   default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {for-special-user: cadmin}.
```

Add **Tolerations** to the Pod to allow it on that node:

```yaml
# ... spec
    spec:
      containers:
        - name: nginx
          image: nginx
      tolerations:
        - key: "for-special-user"
          operator: "Equal"
          value: "cadmin"
          effect: "NoSchedule"
```

Now it runs:

```sh
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-dd7d69c9c-77qlf   1/1     Running   0          31s
```

To remove a taint:

```sh
$ kubectl taint nodes docker-desktop for-special-user=cadmin:NoSchedule-
```

### PriorityClass

`PriorityClass` defines scheduling priority. Scenarios:

1. **Prioritize critical services**: Database or core app pods get higher priority.
2. **Managing resource contention**: In tight-resource envs, manage order of scheduling.

Steps:

1. **Create PriorityClass**:

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "High priority for XYZ services."
```

2. **Specify in Pod**:

```yaml
# ... spec
    spec:
      priorityClassName: high-priority
# ... 
```

### Custom Scheduler

The default scheduler is for general use. For specialized needs, you can use custom ones by setting `schedulerName` in your PodSpec.

Popular community custom schedulers:
-   Tencent TKE Scheduler
-   Huawei Volcano Scheduler

Alternatively, you can implement your own by referencing `kube-scheduler` source code.
