# {{DATE}} — Scanning images and IaC with Trivy

**Area:** DevSecOps / Security · **Tags:** `trivy` `scanning` `iac`

## Scanning a container image
Trivy detects OS-package and language-dependency vulnerabilities. Point it at an image reference and it pulls, unpacks, and matches installed packages against its vulnerability database.

```bash
# Scan an image, fail only on HIGH/CRITICAL that have a fix
trivy image --severity HIGH,CRITICAL \
  --ignore-unfixed \
  myorg/my-app:1.4.2
```

`--ignore-unfixed` hides vulnerabilities with no available patch, cutting noise so the report shows what you can actually act on.

## Scanning IaC / misconfigurations
The `config` target runs Trivy's built-in misconfiguration checks against Terraform, Kubernetes manifests, Dockerfiles, and Helm charts — no separate tool needed.

```bash
# Scan a directory of Terraform / K8s / Dockerfiles
trivy config ./deploy/
```

Findings map to policy IDs (e.g. an S3 bucket without encryption, a container running as root) with a severity and remediation hint.

## Gating a pipeline
Use `--exit-code` so a build fails when findings exceed your threshold:

```bash
trivy image --exit-code 1 --severity CRITICAL myorg/my-app:1.4.2
```

Exit code `0` means clean (or below threshold); `1` fails the CI job.

## Takeaway
Trivy scans both running artifacts (`trivy image`) and infrastructure code (`trivy config`) from one CLI, and `--exit-code` plus `--severity` turn it into a CI gate.

**Source:** [Trivy Docs — Overview](https://trivy.dev/latest/docs/)
