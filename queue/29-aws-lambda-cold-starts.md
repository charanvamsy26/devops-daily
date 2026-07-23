# {{DATE}} — Lambda cold starts and how to reduce them

**Area:** AWS / Serverless · **Tags:** `lambda` `performance` `serverless`

## What a cold start actually is

When a request arrives and no warm execution environment exists, Lambda must: download the code/image, start the runtime, and run your initialization code (everything outside the handler). That's the **Init phase**. Subsequent invocations reuse the environment and skip it entirely — that's a warm start. Environments are also recycled periodically, so cold starts never fully disappear on their own.

Main factors in init duration: package/image size, runtime choice (interpreted vs JVM/.NET), and how much work your init code does (SDK clients, config fetches, framework bootstrapping).

## Cheap wins first

- Trim the deployment package — smaller artifacts download and load faster.
- Do heavy init **once, outside the handler**, so warm invocations reuse it:

```python
import boto3

# runs once per environment (init phase), reused across invocations
table = boto3.resource("dynamodb").Table("orders")

def handler(event, context):
    return table.get_item(Key={"id": event["id"]})
```

- More memory also means proportionally more CPU, which speeds up init for CPU-bound bootstrapping.

## Provisioned concurrency

For latency-sensitive endpoints, provisioned concurrency keeps N environments initialized and ready, so requests up to that concurrency never see a cold start:

```bash
aws lambda put-provisioned-concurrency-config \
  --function-name checkout-api \
  --qualifier live \
  --provisioned-concurrent-executions 10
```

It applies to a version or alias (not `$LATEST`), is billed for the time it's configured, and can be scheduled or target-tracked via Application Auto Scaling to match traffic patterns.

## SnapStart

For JVM-heavy functions (and now also Python/.NET), **SnapStart** takes a Firecracker snapshot of the initialized environment when you publish a version, then resumes from the snapshot on invoke instead of re-running init. Beware of anything captured in the snapshot that must be unique per environment — seed randomness and re-establish network connections after restore.

## Takeaway

Measure the Init duration in your logs/traces before spending money: most cold-start pain yields to smaller packages and lean init code, and only steady latency-critical paths justify provisioned concurrency or SnapStart.

**Source:** [Lambda execution environment](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html)
