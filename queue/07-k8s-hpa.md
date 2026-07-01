# {{DATE}} — Horizontal Pod Autoscaler (HPA)

**Area:** Kubernetes / Scaling · **Tags:** `kubernetes` `autoscaling` `hpa`

## Scaling out, not up
The **HorizontalPodAutoscaler** automatically adjusts the number of Pod replicas in a workload (Deployment, StatefulSet, etc.) to match observed demand. It scales *out* by adding replicas — contrast with the Vertical Pod Autoscaler, which resizes a Pod's requests.

## The control loop
The HPA controller runs a periodic loop (default every 15s). Its core formula is:

```
desiredReplicas = ceil[ currentReplicas * ( currentMetricValue / desiredMetricValue ) ]
```

For example, if CPU utilization averages 200m against a 100m target across 3 replicas, it scales toward 6. Metrics come from the metrics-server (resource metrics) or custom/external metrics adapters.

## Example manifest
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

CPU **Utilization** is measured as a percentage of the Pod's CPU **request** — so HPA only works meaningfully when your Pods declare resource requests.

## Stabilization to avoid flapping
To prevent thrashing, HPA supports a `behavior` block with `scaleUp`/`scaleDown` policies and a stabilization window. By default scale-down uses a 300s stabilization window, picking the highest recommendation over that period before shrinking.

## Takeaway
HPA keeps replica count proportional to load using a simple ratio formula; it depends on accurate resource requests and metrics, and uses stabilization windows to avoid flapping.

**Source:** [Kubernetes docs — Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
