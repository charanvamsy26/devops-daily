# {{DATE}} — Terraform lifecycle meta-arguments

**Area:** Terraform / IaC · **Tags:** `terraform` `lifecycle` `iac`

## Controlling how resources change
The `lifecycle` nested block customizes how Terraform creates, updates, and destroys a resource — overriding its default behavior when the standard plan would be disruptive or unsafe.

## create_before_destroy
By default Terraform destroys a resource before creating its replacement. Setting `create_before_destroy` inverts that order, provisioning the new resource first to avoid downtime.

```hcl
resource "aws_instance" "app" {
  ami           = var.ami
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
  }
}
```

## prevent_destroy and ignore_changes
- **`prevent_destroy`** — makes Terraform reject any plan that would destroy the resource, guarding critical stateful infrastructure like databases.
- **`ignore_changes`** — tells Terraform to ignore drift on specific attributes (useful when something outside Terraform mutates them).

```hcl
resource "aws_db_instance" "main" {
  # ...
  lifecycle {
    prevent_destroy = true
    ignore_changes  = [tags["LastModified"]]
  }
}
```

## Takeaway
Reach for `lifecycle` to make replacements zero-downtime, fence off resources that must never be destroyed, and tolerate externally managed attributes without perpetual diffs.

**Source:** [Terraform docs — The lifecycle meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)
