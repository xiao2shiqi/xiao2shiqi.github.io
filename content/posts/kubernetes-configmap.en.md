+++
date = '2023-11-16T14:35:01+08:00'
draft = false
title = 'Understanding Kubernetes ConfigMap'
tags = ["Cloud Native"]
+++

### Installation Instructions

You can install a single-node version of K8S suitable for local development through Docker Desktop. If Docker Desktop's Kubernetes fails to start, resolve it through the following methods:

**1. Add domestic image mirrors**

Add configuration to Docker's `daemon.json`:

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com"
  ]
}
```

**2. Download Kubernetes images via script**

Download the branch corresponding to your Kubernetes version from the [k8s-for-docker-desktop](https://github.com/AliyunContainerService/k8s-for-docker-desktop/tree/v1.27.2) project on GitHub, then execute the script. After startup is complete, verify the K8S cluster status:

```sh
$ kubectl cluster-info
$ kubectl get nodes
$ kubectl describe node
```

### Understanding Pod

First, understand Pods through a simple example. A Pod is the basic unit of deployment in Kubernetes. Here, we see how to create an `nginx` service using a Pod. Deploy an `nginx` service using the `kubectl` command:

```sh
$ kubectl create deployment nginx-arm --image=nginx
```

After creating the deployment, you can check the Pod status using the following command:

```sh
$ kubectl get pods
```

This will list all Pods, and you can see the status of the Pod created by the `nginx-arm` deployment.

If the Pod status is not `Running`, you can check the logs to help diagnose the problem:

```bash
$ kubectl logs [POD_NAME]
```

Replace `[POD_NAME]` with your Pod's name.

If you want the `nginx` service to be accessible from outside the cluster, you can create a Service to expose it:

```bash
$ kubectl expose deployment nginx-arm --port=80 --type=LoadBalancer
```

This will create a load balancer to forward traffic to port 80 of the `nginx` Pod.

Finally, request the service to verify:

```sh
$ curl 127.0.0.1:80
```

A response of `Welcome to nginx!` indicates the service is accessible.

### Understanding ConfigMap

ConfigMap is an API object in Kubernetes primarily used to store non-confidential key-value pair data. Since the Kubernetes philosophy promotes the separation of application programs and configurations, you can use ConfigMap to separate configuration information from application code, making the configuration of containerized applications more flexible and manageable.

#### Creation

You can create a ConfigMap from a specified `*.yaml` file using the following command:

```sh
$ kubectl create configmap envoy-config --from-file=envoy.yaml
```

The command above creates a ConfigMap object named `envoy-config`. Once created, it can be used to configure containerized applications in Kubernetes. You can mount this ConfigMap into a Pod so applications within the Pod can read and use the configurations defined in the `envoy.yaml` file.

#### Viewing

To list all ConfigMaps in the current namespace, use:

```sh
$ kubectl get configmap
```

This will display basic information for all ConfigMaps:

```sh
NAME               DATA   AGE
envoy-config       1      47h
```

To get detailed information about a specific ConfigMap, use:

```sh
$ kubectl describe configmap [CONFIGMAP_NAME]
```

#### Usage

Start an Envoy Deployment and use the ConfigMap object created earlier:

```sh
$ kubectl create -f envoy-deploy.yaml
$ kubectl expose deploy envoy --selector run=envoy --port=10000 --type=NodePort
```

In the `spec` of `envoy-deploy.yaml`, the external configuration file is referenced like this:

```yaml
spec:
  containers:
  - image: envoyproxy/envoy-dev
    name: envoy
    volumeMounts:
    - name: envoy-config
      mountPath: "/etc/envoy"
      readOnly: true
  volumes:
  - name: envoy-config
    configMap:
      name: envoy-config
```

The configuration above defines the volume mount name and mount directory in `volumeMounts`, set to read-only. In `volumes`, you can see the source of the volume is the ConfigMap named `envoy-config`, which is the object we just created.

Then, use the following command to adjust the number of Pods created:

```bash
kubectl scale deploy envoy --replicas=3
```

Confirm via `kubectl get pods`:

```sh
NAME                     READY   STATUS    RESTARTS   AGE
envoy-747c876c74-lss78   1/1     Running   1          13h
envoy-747c876c74-tmklv   1/1     Running   0          8h
envoy-747c876c74-vdh99   1/1     Running   0          8h
```

#### **Environment Variables**

Using the `--from-env-file` option, you can create ConfigMaps specifically for environment variable configurations:

```bash
$ kubectl create configmap game-env-config --from-env-file=game.properties
```

The `-o yaml` parameter can be used to specify the ConfigMap object's output format as YAML:

```bash
$ kubectl get configmap -oyaml [CONFIGMAP_NAME]
```

#### **Command-Line Key-Value Pairs**

Use the `--from-literal` parameter to define key-value pair ConfigMaps directly in the command line:

```sh
$ kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```

This ConfigMap creates two key-value pairs: `special.how=very` and `special.type=charm`. You can print it using the command above.

**Referencing Configuration**

Like other ConfigMap objects, you can reference and assign Pod environment variables in a deployment object:

```yaml
# ......
spec:
  containers:
    - name: test-container
      image: nginx
      #command: [ "/bin/sh", "-c", "env" ]
      env:
        # Define the environment variable
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              # The ConfigMap containing the value you want to assign to SPECIAL_LEVEL_KEY
              name: special-config
              # Specify the key associated with the value
              key: special.how
```

Note: The Pod above references the value for the key `special.how` from `special-config` via `configMapKeyRef` and assigns it to the environment variable named `SPECIAL_LEVEL_KEY`.

Verification: Create the deployment, then check the Pod loading by printing environment variables using the `env` command:

```sh
# create deployment
$ kubectl create -f downward-api-pod.yaml
# check pod
$ kubectl exec downward-api-pod -- env | grep "SPECIAL_LEVEL_KEY"
```

Output results:

```sh
# output
SPECIAL_LEVEL_KEY=very
```

**Mounting**

You can also declare a `volume` in the Deployment configuration to access a ConfigMap object via mounting:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-volume-pod
spec:
  containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "/bin/sh", "-c", "ls /etc/config/" ]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        # Provide the name of the ConfigMap containing the files you want
        # to add to the container
        name: special-config
```

Note:

* `volumeMounts` defines the volume mount point inside the container; the referenced volume name is `config-volume`, and the specified path is `/etc/config`.
* `volumes` defines the name of the volume. It specifies that this volume comes from a ConfigMap, and the content of `special-config` will be mapped into the volume via `name`.

Verification: Following the method above, check the Pod environment variables using the `env` command after creating the deployment.

### Readiness Probe

A Readiness Probe is a mechanism used to detect whether a container has started and is ready to be used. It is primarily used to improve system reliability and stability.

Basic definition of probe configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: centos
  name: centos
spec:
  replicas: 1
  selector:
    matchLabels:
      run: centos
  template:
    metadata:
      labels:
        run: centos
    spec:
      containers:
      - command:
        - tail
        - -f
        - /dev/null
        image: centos
        name: centos
        readinessProbe:
          exec:
            command:
            - cat
            - /tmp/healthy
          initialDelaySeconds: 5
          periodSeconds: 5
```

Note: This Deployment configures a readiness probe that executes the command `cat /tmp/healthy`. If the command executes successfully (returns status code 0), the container is considered ready.

* `readinessProbe`: Defines the Readiness Probe.
* `exec`: Defines checking the ready state by executing a specified command; `command` is the actual command executed.
* `initialDelaySeconds`: Execution of the readiness probe starts 5 seconds after the container starts.
* `periodSeconds`: The readiness probe executes every 5 seconds.

Start Pod verification:

```bash
$ kubectl create -f centos-readiness.yaml
```

After starting, you'll find that the Pod takes a long time to reach `READY` status:

```bash
NAME                      READY   STATUS             RESTARTS   AGE
centos-54bc4f8766-m54hd   0/1     Running            0          4m21s
```

The reason lies in the readiness probe. To make the Pod enter the ready state, you can enter the container to perform operations:

```bash
# Enter Pod
$ kubectl exec -it [POD_NAME] -- /bin/bash
# Create a file
$ echo "0" > /tmp/healthy
$ cat /tmp/healthy		# # output 0
```

Add the file checked by the probe, which returns a normal status code, and then check the Pod again:

```sh
$ kubectl get po
```

Output:

```sh
NAME                      READY   STATUS             RESTARTS   AGE
centos-54bc4f8766-m54hd   1/1     Running            0          5m24s
```

You can see that the Pod has now reached READY status.
