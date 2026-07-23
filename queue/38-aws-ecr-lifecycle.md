# {{DATE}} — ECR lifecycle policies and image hygiene

**Area:** AWS / Containers · **Tags:** `ecr` `docker` `cost`

## Why bother

Every CI push adds an image; nothing ever removes one. ECR bills per GB-month of storage, and repos full of thousands of stale tags make it harder to see what's actually deployed. Lifecycle policies are ECR's built-in, rule-based garbage collector.

## Anatomy of a policy

A policy is JSON with prioritized rules. Lower `rulePriority` is evaluated first, and once an image matches a rule, later rules can't touch it:

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Expire untagged images after 14 days",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 14
      },
      "action": { "type": "expire" }
    },
    {
      "rulePriority": 2,
      "description": "Keep only the last 30 release images",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["v"],
        "countType": "imageCountMoreThan",
        "countNumber": 30
      },
      "action": { "type": "expire" }
    }
  ]
}
```

Two selection styles: `sinceImagePushed` (age-based) and `imageCountMoreThan` (keep-last-N). The only action is `expire`.

## Applying and testing

```bash
aws ecr put-lifecycle-policy \
  --repository-name app/api \
  --lifecycle-policy-text file://policy.json

# dry run: see which images WOULD be expired
aws ecr start-lifecycle-policy-preview --repository-name app/api
aws ecr get-lifecycle-policy-preview --repository-name app/api
```

Always preview first — expiration is a delete. Note that expiration is asynchronous: matching images are typically removed within about a day of becoming eligible, not instantly.

## Gotchas

- Untagged doesn't always mean unused: multi-arch images reference untagged manifests, and a running pod can still point at a digest whose tag moved. Keep the untagged window generous.
- Deleting a tagged image deletes the image, not just the tag — if two tags point at the same digest, matching either affects both.
- Manage the policy in Terraform (`aws_ecr_lifecycle_policy`) so every repo gets one by default via your repo module.

## Takeaway

Give every ECR repo a lifecycle policy from day one — expire untagged images on an age window and cap tagged images with keep-last-N — and always run the preview before trusting a new rule.

**Source:** [Amazon ECR lifecycle policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)
