# {{DATE}} — Terraform workspaces vs directory-per-environment

**Area:** Terraform / IaC · **Tags:** `terraform` `workspaces` `environments`

## What CLI workspaces actually do

A workspace is a named, separate state file for the **same configuration** in the same backend. Nothing more:

```bash
terraform workspace new staging
terraform workspace select staging
terraform workspace list
```

With the S3 backend, non-default workspace states land under an `env:/` prefix, e.g. `env:/staging/<key>`. Inside config you can branch on `terraform.workspace`:

```hcl
resource "aws_instance" "app" {
  instance_type = terraform.workspace == "prod" ? "m5.large" : "t3.small"

  tags = {
    Environment = terraform.workspace
  }
}
```

## Why they're a poor fit for prod vs non-prod

HashiCorp's own docs say workspaces are **not** designed for strongly separated environments. The problems:

- All workspaces share one backend and one set of credentials/config — you can't point prod at a different account/state bucket cleanly.
- `terraform.workspace` conditionals accumulate until the config is riddled with env-specific branching.
- It's dangerously easy to apply to the wrong workspace; nothing in the directory tells you where you're pointed.

## Directory-per-environment

```text
envs/
  staging/   # backend.tf -> staging state, terraform.tfvars
  prod/      # backend.tf -> prod state (separate bucket/account)
modules/
  app/       # all real logic lives here
```

Each env directory is a thin root module: backend config, provider config, a few variables, and calls into shared modules. You get separate state locations, separate credentials, independent versions during upgrades, and `pwd` tells you exactly what you're about to apply.

## Where workspaces do shine

Cheap, temporary copies of the *same* deployment: per-branch preview environments, per-developer sandboxes, spinning up a parallel copy to test a risky change — cases where the config should be identical and the state separation is the only difference.

## Takeaway

Use directories (thin roots + shared modules) for real environment isolation, and reserve CLI workspaces for ephemeral, identical copies like preview or dev sandboxes.

**Source:** [Terraform workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)
