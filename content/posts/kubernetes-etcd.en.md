+++
date = '2023-11-25T14:29:56+08:00'
draft = false
title = 'Understanding Kubernetes Etcd'
tags = ["Cloud Native"]
+++

### 1. Overview

**etcd** is a distributed, reliable key-value store for the most critical data of a distributed system. Based on the **Raft** consensus algorithm, it provides strong consistency and high availability.

In Kubernetes, etcd is the **single source of truth**. It stores:
- Cluster configuration (API objects).
- Actual state info (Which pods are running where).
- Service discovery and config sharing.
- Backups and recovery data.

### 2. Basic Operations (etcdctl)

- **Member List**: `$ etcdctl member list`
- **Storing Data**: `$ etcdctl put key value`
- **Retrieving Data**: `$ etcdctl get key`
- **Watching**: `$ etcdctl watch key` (Triggers a notification when the key changes).

### 3. Leases and TTL

A **Lease** is a mechanism for expiring keys after a set time.
- **Grant Lease**: `$ etcdctl lease grant 60` (Creates a 60s lease).
- **Bind Key**: `$ etcdctl put k v --lease=[LEASE_ID]`
- **Keep-alive**: `$ etcdctl lease keep-alive [ID]` (Extends the TTL).
- **Revoke**: `$ etcdctl lease revoke [ID]` (Deletes the lease and associated keys).

Leases are commonly used for **Distributed Locking** and **Service Discovery** (e.g., if a node crashes and stops sending heartbeats, its lease expires and its registration key is removed).

### 4. Snapshots and Backup

A snapshot captures the entire state of the etcd database.
- **Save**: `$ etcdctl snapshot save backup.db`
- **Restore**: `$ etcdctl snapshot restore backup.db`

### 5. Running Etcd in K8s

For production, etcd usually runs on dedicated nodes. For development, you can use **Helm** to deploy it inside your cluster.

1. **Add Repo**: `helm repo add bitnami https://charts.bitnami.com/bitnami`
2. **Install**: `helm install my-etcd bitnami/etcd --set persistence.enabled=false`
3. **Verify**: Use a client pod to test K-V operations.
   - `$ kubectl exec -it my-etcd-0 -- etcdctl put /test "Hello"`

### Summary

The reliability of your entire Kubernetes cluster depends on etcd. Understanding its consensus model, watching capabilities, and backup procedures is vital for any cluster administrator.
