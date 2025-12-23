+++
date = '2023-11-16T14:35:01+08:00'
draft = false
title = '理解 Kubernetes 的 Configmap'
tags = ["云原生"]
+++

### 安装说明

通过 docker desktop 可以安装适用于单机和开发环境单机版的 K8S，如果 docker desktop 无法启动 Kubernates 通过以下方式解决：

一：添加国内镜像源

为 Docker 的 `daemon.json` 添加配置：

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com"
  ]
}
```



二：通过脚本下载 Kubernetrs 所需要的镜像

在 GitHub 中的 [k8s-for-docker-desktop](https://github.com/AliyunContainerService/k8s-for-docker-desktop/tree/v1.27.2) 项目中下载 Kubernetes 版本对应的分支，然后执行脚本即可，启动完成后，验证 K8S 集群状态：

```sh
$ kubectl cluster-info
$ kubectl get nodes
$ kubectl describe node
```



### 理解 Pod

先通过一个简单的示例理解 Pod，Pod 是 Kubernetes 中的基本部署单元，这里看看如何用 Pod 创建一个 `nginx` 服务。使用 `kubectl` 命令部署一个 `nginx` 的服务：

```sh
$ kubectl create deployment nginx-arm --image=nginx
```

创建部署后，您可以使用以下命令检查 Pod 的状态：

```sh
$ kubectl get pods
```

这将列出所有 Pod，您可以查看 `nginx-arm` 部署创建的 Pod 的状态。

如果 Pod 状态不是 `Running`，您可以使用以下命令查看日志，以帮助诊断问题：

```bash
$ kubectl logs [POD_NAME]
```

将 `[POD_NAME]` 替换为您的 Pod 名称。

如果您想让 `nginx` 服务可以从集群外部访问，您可以创建一个服务来暴露它：

```bash
$ kubectl expose deployment nginx-arm --port=80 --type=LoadBalancer
```

这将创建一个负载均衡器，将流量转发到 `nginx` Pod 的 80 端口。

最后请求服务，进行验证：

```sh
$ curl 127.0.0.1:80
```

响应 `Welcome to nginx!` 代表服务访问完成。



### 理解 ConfigMap

ConfigMap 是 Kubernetes 中的一个 API 对象，主要用于存储非机密性的键值对数据。因为 Kubernetes 的理念是推崇应用程序和配置分离，所以你可以使用 ConfigMap 将配置信息从应用程序代码中分离出来，使得容器化应用程序的配置更加灵活和可管理。



#### 创建

你可以通过一下命令从指定的 `*.yaml`  文件里面创建一个 ConfigMap，示例：

```sh
$ kubectl create configmap envoy-config --from-file=envoy.yaml
```

以上命令创建一个名称为 `envoy-config` 的 ConfigMap 对象，创建后，它可以用于配置 Kubernetes 中的容器化应用，可以将这个 ConfigMap 挂载到 Pod 中，使得 Pod 内的应用能够读取并使用 `envoy.yaml` 文件中定义的配置。



#### 查看

在当前命名空间中列出所有 ConfigMap，您可以使用：

```sh
$ kubectl get configmap
```

这将显示所有 ConfigMap 的基本信息：

```sh
NAME               DATA   AGE
envoy-config       1      47h
```

要获取特定 ConfigMap 的详细信息，可以使用：

```sh
$ kubectl describe configmap [CONFIGMAP_NAME]
```



#### 使用

启动一个 Envoy Deployment 并且使用刚才创建的 ConfigMap 对象：

```sh
$ kubectl create -f envoy-deploy.yaml
$ kubectl expose deploy envoy --selector run=envoy --port=10000 --type=NodePort
```

在 `envoy-deploy.yaml` 的 `spec` 中是这样引用外部的配置文件的

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

以上配置在 `volumeMounts` 中定义了卷的挂载名称和挂载目录，并且设置为只读。在 `volumes` 中可以看到卷的来源是名称为 `envoy-config` 的  ConfigMap ，就是我们刚才创建的对象。

然后，可以使用以下命令，调整刚才创建 Pod 的数量：

```bash
kubectl scale deploy envoy --replicas=3
```

通过 `kubectl get pods`  可以确认：

```sh
NAME                     READY   STATUS    RESTARTS   AGE
envoy-747c876c74-lss78   1/1     Running   1          13h
envoy-747c876c74-tmklv   1/1     Running   0          8h
envoy-747c876c74-vdh99   1/1     Running   0          8h
```



#### **环境变量**

使用 `--from-env-file` 选项参数，可以创建特别用于环境变量配置示例：

```bash
$ kubectl create configmap game-env-config --from-env-file=game.properties
```

使用 `-o yaml` 参数可以指定 configMap 对象输出格式为 YAML 示例：

```bash
$ kubectl get configmap -oyaml [CONFIGMAP_NAME]
```



#### **命令行键值对**

使用 `--from-literal` 参数可以直接在命令行中定义键值对的 ConfigMap：

```sh
$ kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```

这里的 ConfigMap 创建了两个键值对：`special.how=very` 和 `special.type=charm`。你可以用上面的命令打印它。



**引用配置**

和其他 ConfigMap 对象一样，可以在部署对象引用赋值 Pod 的环境变量，Deploymen 配置：

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

说明：以上 Pod 通过 `configMapKeyRef` 引用 `special-config` 中键为 `special.how` 的值，并将其赋给了名为 `SPECIAL_LEVEL_KEY` 的环境变量。

验证：可以先创建部署，然后通过 `env` 命令打印环境变量查看 Pod 的加载情况：

```sh
# create  deployment
$ kubectl create -f downward-api-pod.yaml
# check pod
$ kubectl exec downward-api-pod -- env | grep "SPECIAL_LEVEL_KEY"
```

输出结果：

```sh
# output
SPECIAL_LEVEL_KEY=very
```



**挂载**

在 Deploymen 配置中也可以声明 `volume` 以挂载的方式访问 ConfigMap 对象，示例：

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

说明：

* `volumeMounts`  定义容器内的卷挂载点，引用的卷名称是  `config-volume`，指定路径是 `/etc/confg`
* `volumes` 定义卷的名称。指明这个卷来源 ConfigMap，通过 `name` 指定 `special-config` 的 ConfigMap 内容会将被映射到卷中



验证：参考上面的方式，在创建部署后，通过 `env` 命令查看 Pod 环境变量即可。



### 就绪探针

Readiness Probe（就绪探针）是用来检测容器是否已经启动并且准备好被使用的机制。主要用于提高系统的可靠性和稳定性。

基本定义探针配置示例：

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

说明：这个 Deployment 配置了一个就绪探针，这个探针是执行的命令是 `cat /tmp/healthy`。如果该命令成功执行（返回状态码 0），则认为容器就绪。

* readinessProbe：定义了就绪探针（Readiness Probe）
* exec：定义通过指定执行命令来检查就绪状态，`command` 是具体执行的命令。
* initialDelaySeconds：容器启动后 5 秒开始执行就绪探针。
* periodSeconds：每 5 秒执行一次就绪探针。



启动 Pod 验证：

```bash
$ kubectl create -f centos-readiness.yaml
```

启动后发现该 Pod 迟迟无法  `READY` ：

```bash
NAME                      READY   STATUS             RESTARTS   AGE
centos-54bc4f8766-m54hd   0/1     Running            0          4m21s
```

原因在于就绪探针的作用，想要 Pod 进入就绪状态，可以进入容器进行操作：

```bash
# Enter Pod
$ kubectl exec -it [POD_NAME] -- /bin/bash
# Create a file
$ echo "0" > /tmp/healthy
$ cat /tmp/healthy		# # output 0
```

添加探针检查的文件，返回正常的状态码，然后再查看 Pod：

```sh
$ kubectl get po
```

输出：

```sh
NAME                      READY   STATUS             RESTARTS   AGE
centos-54bc4f8766-m54hd   1/1     Running            0          5m24s
```

可以看到刚才的 Pod 已经进入 READY 状态。
