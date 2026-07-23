# {{DATE}} — StatefulSets and stable pod identity

**Area:** Kubernetes / Workloads · **Tags:** `statefulset` `storage` `headless-service`

## Why Deployments aren't enough for stateful apps

Deployment pods are interchangeable: random name suffixes, no per-pod storage, no ordering guarantees. Databases and quorum systems (etcd, Kafka, Postgres replicas) need each member to keep the same name, network address, and disk across restarts. StatefulSets provide a **sticky identity**: an ordinal-based pod name (`db-0`, `db-1`, `db-2`) that survives rescheduling.

## Stable network identity via a headless Service

A StatefulSet requires a headless Service (`clusterIP: None`) to own the DNS domain for its pods. Each pod then gets a stable, resolvable hostname:

```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
# e.g. db-0.db-hs.prod.svc.cluster.local
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: db-hs
spec:
  clusterIP: None        # headless — per-pod DNS records
  selector:
    app: db
  ports:
    - port: 5432
```

Peers can address `db-0` directly even after it's rescheduled to another node — the name is stable even though the pod IP is not.

## Per-pod storage with volumeClaimTemplates

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: db-hs
  replicas: 3
  selector:
    matchLabels: { app: db }
  template:
    metadata:
      labels: { app: db }
    spec:
      containers:
        - name: postgres
          image: postgres:16
          volumeMounts: [{ name: data, mountPath: /var/lib/postgresql/data }]
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests: { storage: 20Gi }
```

Each replica gets its own PVC (`data-db-0`, `data-db-1`, ...). When `db-1` is rescheduled, it reattaches to the same PVC. Deleting or scaling down the StatefulSet does **not** delete the PVCs by default — data outlives the pods.

## Ordered rollout

With the default `podManagementPolicy: OrderedReady`, pods are created sequentially `0 → N-1` (each must be Running and Ready before the next starts) and terminated in reverse order `N-1 → 0`. Updates roll in reverse ordinal order too, which is what you want for primary/replica topologies.

## Takeaway

StatefulSets give each replica a stable name, stable per-pod DNS (via a headless Service), and its own PVC that survives rescheduling — the three guarantees that clustered stateful software depends on and that Deployments deliberately don't provide.

**Source:** [Kubernetes docs — StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
