# {{DATE}} — ALB vs NLB: choosing a load balancer

**Area:** AWS / Networking · **Tags:** `aws` `elb` `networking`

## Different layers of the stack
Elastic Load Balancing offers several types. The two most common are:

- **Application Load Balancer (ALB)** — operates at **Layer 7** (HTTP/HTTPS). It understands requests, so it can route on host, path, headers, query strings, and HTTP methods.
- **Network Load Balancer (NLB)** — operates at **Layer 4** (TCP/UDP/TLS). It forwards packets with ultra-low latency and can handle millions of requests per second.

## When to use an ALB
Choose an ALB for web applications and microservices that need content-based routing.

```text
# Path-based routing on one ALB listener
/api/*     -> target group: api-service
/images/*  -> target group: static-service
default    -> target group: web-frontend
```

ALB also natively supports redirects, fixed responses, and integrations with WAF and Cognito authentication.

## When to use an NLB
Choose an NLB when you need:

- Raw **TCP/UDP** support (not just HTTP).
- **Static IP addresses** per Availability Zone (or an Elastic IP).
- Extreme performance and low, consistent latency.
- **Preservation of the client source IP** by default.

## Takeaway
Route on request content and need HTTP smarts → ALB. Need Layer 4 throughput, static IPs, or non-HTTP protocols → NLB.

**Source:** [Elastic Load Balancing — Product comparison](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
