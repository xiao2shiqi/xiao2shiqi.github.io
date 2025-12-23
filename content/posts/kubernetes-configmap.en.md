+++
date = '2023-11-16T14:35:01+08:00'
draft = false
title = 'Understanding Kubernetes ConfigMap'
tags = ["Cloud Native"]
+++

### Local Setup (Docker Desktop)

If you are using Docker Desktop and Kubernetes won't start, common fixes include:
- Adding Chinese images mirrors.
- Using helper scripts to pull the required K8s images locally.

Verify your setup:
```sh
$ kubectl get nodes
$ kubectl cluster-info
```

### Pods and Services

A **Pod** is the smallest deployable unit. Let's start an Nginx deployment:
```sh
$ kubectl create deployment nginx --image=nginx
$ kubectl expose deployment nginx --port=80 --type=LoadBalancer
$ curl 127.0.0.1:80
```

### ConfigMap: Decoupling Config from Code

A **ConfigMap** stores non-confidential data in key-value pairs. This allows you to change environment variables or configuration files without rebuilding the container image.

#### Creation
From literal values:
```sh
$ kubectl create configmap settings --from-literal=mode=prod
```
From a file:
```sh
$ kubectl create configmap app-config --from-file=config.yaml
```

#### Usage in a Pod

**1. Environment Variables**
```yaml
env:
  - name: APP_MODE
    valueFrom:
      configMapKeyRef:
        name: settings
        key: mode
```

**2. Mounted Volumes**
The ConfigMap content appears as files within the container.
```yaml
volumeMounts:
  - name: config-volume
    mountPath: /etc/config
volumes:
  - name: config-volume
    configMap:
      name: app-config
```

### Probes: Health and Readiness

A **Readiness Probe** tells K8s when a container is ready to start accepting traffic. If the probe fails, the Pod is removed from service endpoints.

**Example: File-based Probe**
```yaml
readinessProbe:
  exec:
    command: ["cat", "/tmp/ready"]
  initialDelaySeconds: 5
  periodSeconds: 5
```
Traffic will only flow into the Pod after you manually create the file:
`$ kubectl exec -it [POD] -- touch /tmp/ready`

### Summary

ConfigMaps are essential for building portable, "write once, run anywhere" cloud-native applications. They separate the concern of *how to run* (Deployment) from *how to configure* (ConfigMap).
