# {{DATE}} — VPC endpoints: gateway vs interface

**Area:** AWS / Networking · **Tags:** `vpc` `privatelink` `endpoints`

## The two flavors

Both let resources in a VPC reach AWS services without traversing the public internet, but they work very differently:

- **Gateway endpoints** — only for **S3 and DynamoDB**. They work by adding a route to your route tables that targets an AWS-managed prefix list. No ENIs, no extra cost.
- **Interface endpoints** — powered by **AWS PrivateLink**. They create an ENI with a private IP in your subnet(s) and support most AWS services (SSM, ECR, CloudWatch Logs, STS, etc.). Billed per hour per AZ plus per GB processed.

## Gateway endpoint (S3)

```bash
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0abc123 \
  --vpc-endpoint-type Gateway \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-0def456
```

The route table gets an entry like `pl-63a5400a (com.amazonaws.us-east-1.s3) -> vpce-...`. Traffic to S3 from associated subnets is routed through the endpoint automatically.

## Interface endpoint (SSM, for session manager without a NAT)

```bash
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0abc123 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.ssm \
  --subnet-ids subnet-0aaa subnet-0bbb \
  --security-group-ids sg-0ccc \
  --private-dns-enabled
```

With **private DNS** enabled, the default service hostname (`ssm.us-east-1.amazonaws.com`) resolves to the endpoint's private IPs inside the VPC — no application changes needed. The endpoint's security group must allow inbound 443 from the callers.

## Gotchas

- Gateway endpoints can't be reached from on-prem over VPN/Direct Connect or from a peered VPC; interface endpoints can.
- Endpoint policies (a resource policy on the endpoint) let you restrict which buckets/APIs are reachable — useful for data-exfiltration guardrails.
- S3 also offers interface endpoints now; you'd pick one when you need on-prem access to S3 privately, and keep the free gateway endpoint for in-VPC traffic.

## Takeaway

Default to the free gateway endpoints for S3/DynamoDB in-VPC traffic, and use interface endpoints (PrivateLink) for everything else or when on-prem/cross-VPC private access is required.

**Source:** [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)
