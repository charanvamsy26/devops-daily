# {{DATE}} — IAM roles vs users and AssumeRole

**Area:** AWS / Security · **Tags:** `aws` `iam` `security`

## Users vs roles
An **IAM user** is a long-lived identity with permanent credentials (a password and/or access keys). An **IAM role** is an identity with a permissions policy but **no long-term credentials** — instead, anyone who assumes the role receives **temporary security credentials** vended by AWS STS.

Roles are the preferred way to grant access to AWS services, EC2 instances, Lambda functions, and federated or cross-account principals, because there are no static keys to leak or rotate.

## The trust policy
Every role has two policies:

- A **permissions policy** — what the role *can do*.
- A **trust policy** (assume-role policy) — *who is allowed to assume it*.

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::111122223333:root" },
    "Action": "sts:AssumeRole"
  }]
}
```

This trust policy lets any principal in account `111122223333` (subject to its own IAM permissions) call `AssumeRole`.

## Assuming a role
Calling `sts:AssumeRole` returns temporary credentials that expire (default 1 hour, configurable up to the role's max session duration):

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::444455556666:role/ReadOnlyAudit \
  --role-session-name audit-session
```

The response contains an `AccessKeyId`, `SecretAccessKey`, and `SessionToken` used for subsequent calls.

## Takeaway
Prefer roles over users wherever possible: temporary, auto-rotating credentials shrink the blast radius of a leak, and cross-account access becomes a trust-policy edit rather than a shared secret.

**Source:** [AWS IAM User Guide — IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
