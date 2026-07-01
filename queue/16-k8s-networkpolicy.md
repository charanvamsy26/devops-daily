# {{DATE}} — NetworkPolicies and default-deny

**Area:** Kubernetes / Security · **Tags:** `kubernetes` `security` `networkpolicy`

## Pods are open by default
Out of the box, any Pod can talk to any other Pod — the cluster network is flat and fully permissive. A **NetworkPolicy** lets you define allowed ingress/egress at the IP/port level, selected by Pod labels.

Important: NetworkPolicies are enforced by the **CNI plugin** (Calico, Cilium, etc.). If your CNI doesn't implement them, the objects are accepted but have no effect.

## Additive, allow-only rules
A crucial mental model: **as soon as any NetworkPolicy selects a Pod for a direction (ingress or egress), that Pod becomes "isolated" for that direction** and only the traffic explicitly allowed is permitted. Policies are additive — there is no "deny" rule; you deny by *not* allowing.

## Default-deny for a namespace
Select all Pods and permit nothing:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: prod
spec:
  podSelector: {}        # selects every Pod in the namespace
  policyTypes:
  - Ingress
  - Egress
```

With `podSelector: {}` and empty ingress/egress rules, all in- and outbound traffic for those Pods is dropped. You then layer allow-policies on top.

## Allowing specific traffic
```yaml
spec:
  podSelector:
    matchLabels: { app: db }
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels: { app: web }
    ports:
    - protocol: TCP
      port: 5432
```

This lets only `app: web` Pods reach the database on 5432, while default-deny blocks everything else.

## Takeaway
NetworkPolicies are additive allow-lists enforced by the CNI; start with a namespace default-deny, then explicitly permit the flows your apps actually need.

**Source:** [Kubernetes docs — Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
