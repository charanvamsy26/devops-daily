# {{DATE}} — Pod Security Standards

**Area:** DevSecOps / Kubernetes · **Tags:** `kubernetes` `pss` `security`

## The three levels
Pod Security Standards (PSS) define three cumulative policy levels:
- **privileged** — unrestricted; anything is allowed.
- **baseline** — blocks known privilege escalations (host namespaces, privileged containers, most hostPath). Minimally restrictive.
- **restricted** — the hardened tier: enforces non-root, dropped capabilities, seccomp `RuntimeDefault`, no privilege escalation.

## Enforcing with the Pod Security Admission controller
PSS is applied per **namespace** via labels read by the built-in Pod Security Admission (PSA) controller. Each level supports three modes:
- `enforce` — reject non-compliant pods
- `audit` — allow, but record a violation in the audit log
- `warn` — allow, but return a user-facing warning

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: payments
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.29
    pod-security.kubernetes.io/warn: restricted
```

## A compliant pod securityContext
To pass `restricted`, pods must set an explicit hardened `securityContext`:

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  seccompProfile: { type: RuntimeDefault }
  capabilities: { drop: ["ALL"] }
```

## Takeaway
Pod Security Standards give three levels (privileged, baseline, restricted) enforced per namespace by the Pod Security Admission controller in enforce, audit, or warn modes.

**Source:** [Kubernetes Docs — Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
