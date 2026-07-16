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
<!-- NEXT-ENTRY -->


## Areas covered

`kubernetes` · `terraform` · `aws` · `azure` · `ci-cd` · `observability` · `prometheus` ·
`devsecops` · `networking` · `linux` · `python`

---

Maintained by [Guru Charan Vamsy Vardhineedi](https://github.com/charanvamsy26) ·
companion to [eks-gitops-platform](https://github.com/charanvamsy26/eks-gitops-platform) and
[slo-operator](https://github.com/charanvamsy26/slo-operator).
