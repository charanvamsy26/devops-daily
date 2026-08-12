# DevOps & SRE — Daily Learning Log

A daily log of things I learn and practice across **DevOps and Site Reliability Engineering** —
Kubernetes, Terraform, AWS/Azure, CI/CD, observability, and DevSecOps. One focused note per day:
a concept, a command, a gotcha, or a pattern, with a source so it's verifiable.

It doubles as a searchable personal knowledge base — `grep` the `entries/` folder and you'll usually
find the answer faster than the docs.

## Index

| Date | Topic | Area |
| --- | --- | --- |
| [2026-06-28](entries/2026-06-28.md) | Multi-window, multi-burn-rate SLO alerting | SRE / Observability |
| [2026-06-29](entries/2026-06-29.md) | Kubernetes requests vs limits: throttling & OOMKills | Kubernetes / Reliability |
| [2026-06-30](entries/2026-06-30.md) | Terraform remote state locking with S3 + DynamoDB | Terraform / IaC |
| [2026-07-01](entries/2026-07-01.md) | GitHub Actions → AWS with OIDC (no long-lived keys) | CI/CD / DevSecOps |
| [2026-07-02](entries/2026-07-02.md) | Liveness, readiness, and startup probes | Kubernetes / Reliability |
| [2026-07-03](entries/2026-07-03.md) | IAM roles vs users and AssumeRole | AWS / Security |
| [2026-07-04](entries/2026-07-04.md) | Blue-green vs canary deployments | CI/CD / Delivery |
| [2026-07-05](entries/2026-07-05.md) | Kubernetes Services and kube-proxy | Kubernetes / Networking |
| [2026-07-06](entries/2026-07-06.md) | Security groups vs network ACLs | AWS / Networking |
| [2026-07-07](entries/2026-07-07.md) | RED and USE monitoring methods | Observability / SRE |
| [2026-07-08](entries/2026-07-08.md) | Horizontal Pod Autoscaler (HPA) | Kubernetes / Scaling |
| [2026-07-09](entries/2026-07-09.md) | ALB vs NLB: choosing a load balancer | AWS / Networking |
| [2026-07-10](entries/2026-07-10.md) | Prometheus histograms and quantiles | Observability / Prometheus |
| [2026-07-11](entries/2026-07-11.md) | PodDisruptionBudgets and voluntary disruptions | Kubernetes / Reliability |
| [2026-07-12](entries/2026-07-12.md) | S3 storage classes and lifecycle policies | AWS / Storage |
| [2026-07-13](entries/2026-07-13.md) | Scanning images and IaC with Trivy | DevSecOps / Security |
| [2026-07-14](entries/2026-07-14.md) | Taints, tolerations, and node affinity | Kubernetes / Scheduling |
| [2026-07-15](entries/2026-07-15.md) | Terraform modules for reuse | Terraform / IaC |
| [2026-07-16](entries/2026-07-16.md) | Alertmanager routing and grouping | Observability / Alerting |
| [2026-07-17](entries/2026-07-17.md) | NetworkPolicies and default-deny | Kubernetes / Security |
| [2026-07-18](entries/2026-07-18.md) | Terraform count vs for_each | Terraform / IaC |
| [2026-07-19](entries/2026-07-19.md) | Reusable and matrix GitHub Actions workflows | CI/CD |
| [2026-07-20](entries/2026-07-20.md) | Kubernetes RBAC: Roles and bindings | Kubernetes / Security |
| [2026-07-21](entries/2026-07-21.md) | Terraform lifecycle meta-arguments | Terraform / IaC |
| [2026-07-22](entries/2026-07-22.md) | Pod Security Standards | DevSecOps / Kubernetes |
| [2026-07-23](entries/2026-07-23.md) | Kubernetes DNS: CoreDNS and service discovery | Kubernetes / Networking |
| [2026-07-24](entries/2026-07-24.md) | StatefulSets and stable pod identity | Kubernetes / Workloads |
| [2026-07-25](entries/2026-07-25.md) | VPC endpoints: gateway vs interface | AWS / Networking |
| [2026-07-26](entries/2026-07-26.md) | PromQL: rate vs irate vs increase | Observability / Prometheus |
| [2026-07-27](entries/2026-07-27.md) | etcd: the Kubernetes datastore | Kubernetes / Internals |
| [2026-07-28](entries/2026-07-28.md) | Terraform import and moved blocks | Terraform / IaC |
| [2026-07-29](entries/2026-07-29.md) | Argo CD sync waves and hooks | CI/CD / GitOps |
| [2026-07-30](entries/2026-07-30.md) | Ingress vs Gateway API | Kubernetes / Networking |
| [2026-07-31](entries/2026-07-31.md) | Lambda cold starts and how to reduce them | AWS / Serverless |
| [2026-08-01](entries/2026-08-01.md) | OpenTelemetry traces, spans, and context propagation | Observability / Tracing |
| [2026-08-02](entries/2026-08-02.md) | cgroups v2: how containers are limited | Linux / Containers |
| [2026-08-03](entries/2026-08-03.md) | Azure managed identities vs service principals | Azure / Security |
| [2026-08-04](entries/2026-08-04.md) | Toil, error budgets, and when to stop paging | SRE / Practice |
| [2026-08-05](entries/2026-08-05.md) | Init containers and sidecar containers | Kubernetes / Workloads |
| [2026-08-06](entries/2026-08-06.md) | Terraform workspaces vs directory-per-environment | Terraform / IaC |
| [2026-08-07](entries/2026-08-07.md) | Docker multi-stage builds and layer caching | Containers / CI |
| [2026-08-08](entries/2026-08-08.md) | The Linux OOM killer and container memory | Linux / Reliability |
| [2026-08-09](entries/2026-08-09.md) | ECR lifecycle policies and image hygiene | AWS / Containers |
| [2026-08-10](entries/2026-08-10.md) | GitHub Actions environments and deployment protection | CI/CD |
| [2026-08-11](entries/2026-08-11.md) | Pod priority and preemption | Kubernetes / Scheduling |
| [2026-08-12](entries/2026-08-12.md) | AKS node pools, system vs user | Azure / Kubernetes |
<!-- NEXT-ENTRY -->


## Areas covered

`kubernetes` · `terraform` · `aws` · `azure` · `ci-cd` · `observability` · `prometheus` ·
`devsecops` · `networking` · `linux` · `python`

---

Maintained by [Guru Charan Vamsy Vardhineedi](https://github.com/charanvamsy26) ·
companion to [eks-gitops-platform](https://github.com/charanvamsy26/eks-gitops-platform) and
[slo-operator](https://github.com/charanvamsy26/slo-operator).
