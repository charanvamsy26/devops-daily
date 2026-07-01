# {{DATE}} — Terraform count vs for_each

**Area:** Terraform / IaC · **Tags:** `terraform` `meta-arguments` `iac`

## Two ways to make many
Both `count` and `for_each` create multiple instances of a resource or module from a single block, but they index them differently.

- **`count`** takes a whole number and produces instances indexed by **integer position** (`[0]`, `[1]`, ...).
- **`for_each`** takes a **map or set of strings** and produces instances indexed by **key**.

## Why the index matters
With `count`, removing an item from the middle of a list shifts every later index, so Terraform plans to destroy and recreate everything after it. `for_each` addresses instances by a stable key, so adding or removing one entry only touches that entry.

```hcl
# count: fine for N identical things
resource "aws_instance" "worker" {
  count         = 3
  ami           = var.ami
  instance_type = "t3.micro"
}

# for_each: stable keys for distinct things
resource "aws_iam_user" "team" {
  for_each = toset(["alice", "bob", "carol"])
  name     = each.key
}
```

## Referencing instances
`count` instances are a list: `aws_instance.worker[0]`. `for_each` instances are a map: `aws_iam_user.team["alice"]`, and inside the block you use `each.key` / `each.value`.

## Takeaway
Use `count` for N interchangeable copies; use `for_each` whenever instances have distinct identities, so edits don't cascade into needless recreation.

**Source:** [Terraform docs — The for_each meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
