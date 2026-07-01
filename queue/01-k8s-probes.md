# {{DATE}} — Liveness, readiness, and startup probes

**Area:** Kubernetes / Reliability · **Tags:** `kubernetes` `probes` `reliability`

## Three probes, three different questions
The kubelet runs probes against containers to answer distinct questions:

- **livenessProbe** — "Is the container still healthy?" If it fails, the kubelet **restarts** the container. Use it to recover from deadlocks where a process is running but stuck.
- **readinessProbe** — "Can the container serve traffic?" If it fails, the Pod's IP is **removed from Service Endpoints** so no traffic is routed to it. The container is *not* restarted.
- **startupProbe** — "Has the app finished booting?" While it runs, liveness and readiness probes are **disabled**. Once it succeeds, the other probes take over. Ideal for slow-starting apps.

## Example spec
```yaml
containers:
- name: web
  image: myapp:1.0
  ports:
  - containerPort: 8080
  startupProbe:
    httpGet: { path: /healthz, port: 8080 }
    failureThreshold: 30
    periodSeconds: 10          # allows up to 300s to start
  livenessProbe:
    httpGet: { path: /healthz, port: 8080 }
    periodSeconds: 10
    failureThreshold: 3
  readinessProbe:
    httpGet: { path: /ready, port: 8080 }
    periodSeconds: 5
```

## Probe mechanisms and tuning
Each probe supports one handler: `httpGet`, `tcpSocket`, `grpc`, or `exec`.
Key fields:

- `initialDelaySeconds` — wait before the first probe.
- `periodSeconds` — how often to probe (default 10).
- `timeoutSeconds` — per-probe timeout (default 1).
- `failureThreshold` / `successThreshold` — consecutive results before acting.

A common mistake is pointing a **liveness** probe at a dependency (like a database). If that dependency blips, the kubelet will restart otherwise-healthy Pods in a cascade. Keep liveness checks local and cheap.

## Takeaway
Use readiness to gate traffic, liveness to restart wedged processes, and startup to protect slow boots — and never let liveness depend on external services.

**Source:** [Kubernetes docs — Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
