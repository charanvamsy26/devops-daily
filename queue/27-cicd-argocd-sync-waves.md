# {{DATE}} — Argo CD sync waves and hooks

**Area:** CI/CD / GitOps · **Tags:** `argocd` `gitops` `kubernetes`

## Ordering resources with sync waves

By default Argo CD applies all manifests in a fixed order by kind (namespaces first, then CRDs, then workloads, etc.). Sync waves let you impose explicit ordering on top of that with a single annotation — lower waves apply first, and Argo CD waits for each wave to be healthy before starting the next:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  annotations:
    argocd.argoproj.io/sync-wave: "1"   # default wave is 0
```

Negative waves are valid, which is handy for prerequisites like a database or a CRD that everything else depends on:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"  # applied before wave 0 resources
```

## Resource hooks

Hooks run resources at specific points of the sync operation instead of as part of the normal apply. Classic use case: a schema migration Job that must finish before the new Deployment rolls out.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: registry.example.com/api-migrations:v1.42.0
```

Hook phases: `PreSync`, `Sync`, `PostSync`, `SyncFail`. Deletion policies (`HookSucceeded`, `HookFailed`, `BeforeHookCreation`) control cleanup — `BeforeHookCreation` is the default and deletes the previous hook resource before creating a new one.

## How waves and hooks combine

For each phase, Argo CD orders resources by: hook phase first, then sync wave, then kind, then name. So a `PreSync` hook in wave 2 still runs before any `Sync`-phase resource, and within a phase the waves decide the order.

## Takeaway

Sync waves give declarative ordering between manifests, and hooks give you lifecycle points around the sync — together they replace most "run this script before deploy" glue with plain annotations in Git.

**Source:** [Argo CD sync waves](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)
