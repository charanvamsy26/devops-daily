# {{DATE}} — PromQL: rate vs irate vs increase

**Area:** Observability / Prometheus · **Tags:** `promql` `counters` `queries`

## The three counter functions

All three only make sense on counters, and all three handle counter resets automatically. The difference is *how* they use the samples in the range window:

```promql
# Per-second average rate over the whole 5m window (uses all samples)
rate(http_requests_total[5m])

# Per-second instant rate using only the LAST TWO samples in the window
irate(http_requests_total[5m])

# Total increase over the window (roughly rate * range duration)
increase(http_requests_total[5m])
```

## When to use which

- `rate()` — the default for alerting and recording rules. Smooths over the full window, so it's resilient to scrape jitter and slow-moving counters.
- `irate()` — only for fast-moving counters on high-resolution graphs. Because it looks at just the last two points, it reacts instantly but is far too spiky for alerts.
- `increase()` — human-friendly "how many requests happened in the last hour" questions. It extrapolates to the window edges, so results can be non-integer even for integer counters.

```promql
# Good alert expression: smoothed, per-second
sum(rate(http_requests_total{code=~"5.."}[5m])) by (job)
  / sum(rate(http_requests_total[5m])) by (job) > 0.05

# Anti-pattern: irate in an aggregation for alerting — spiky and misleading
# sum(irate(http_requests_total[5m]))
```

## Window sizing rule of thumb

The range must contain at least two samples, so the window should be at least 2x the scrape interval — ideally 4x to survive a failed scrape. With a 30s scrape interval, `[1m]` is fragile; `[2m]` or `[5m]` is safe.

```promql
# 30s scrape interval -> [5m] gives up to 10 samples to work with
rate(node_network_receive_bytes_total[5m])
```

## Takeaway

Use `rate()` for alerts and dashboards, `increase()` for human-readable totals, and reserve `irate()` for zoomed-in graphs of volatile counters — and always size the range window to several scrape intervals.

**Source:** [Prometheus query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/)
