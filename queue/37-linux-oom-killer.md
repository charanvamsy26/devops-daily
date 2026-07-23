# {{DATE}} — The Linux OOM killer and container memory

**Area:** Linux / Reliability · **Tags:** `oom` `memory` `kernel`

## What the OOM killer does

When the kernel cannot satisfy an allocation after reclaiming everything it can, it invokes the OOM killer: pick a process, SIGKILL it, free its memory. In a container world there are two flavors:

- **Global OOM** — the whole node is out of memory; any process on the host is a candidate.
- **cgroup OOM** — a cgroup hits its `memory.max`; the killer picks a victim **inside that cgroup only**. This is the normal "OOMKilled, exit code 137" container death.

## How the victim is chosen

Each process has `/proc/<pid>/oom_score` — a badness score derived mostly from its share of memory used. It can be biased with `/proc/<pid>/oom_score_adj`, ranging **-1000 to +1000**:

```bash
cat /proc/self/oom_score_adj   # 0 by default
# -1000 = never kill this process; +1000 = kill it first
echo -500 > /proc/$PID/oom_score_adj   # needs privilege to lower
```

Kubernetes uses exactly this knob: the kubelet sets `oom_score_adj` per QoS class so that under **node-level** memory pressure, BestEffort pods (adj +1000) die before Burstable pods, which die before Guaranteed pods (adj -997) and node daemons.

## Reading the aftermath

The kernel logs every OOM kill — this is the ground truth when a container "randomly restarted":

```bash
dmesg -T | grep -i -E "killed process|oom"
# [Wed Jul 22 03:14:07] Memory cgroup out of memory: Killed process 21748 (java)
#   total-vm:5214032kB, anon-rss:2097100kB ...

# per-cgroup counters (cgroup v2)
cat /sys/fs/cgroup/<pod-cgroup>/memory.events
# oom 3
# oom_kill 3
```

`Memory cgroup out of memory` means a container limit was hit — raise the limit or fix the leak. A global `Out of memory: Killed process ...` (no "Memory cgroup") means the node itself was exhausted — an overcommit/eviction problem, not one container's limit.

## Gotcha: the victim isn't always who exceeded

Within a cgroup, the killer picks the process with the highest score — usually the biggest RSS. In a multi-process container, a small helper can exceed the limit but the kernel kills the big main process. And since only PID 1's death restarts the container, an OOM kill of a child process can leave the container "running" but degraded.

## Takeaway

OOMKilled/exit 137 is the kernel's cgroup OOM killer enforcing `memory.max`, with victims ranked by `oom_score` and biased via `oom_score_adj` — which is precisely how Kubernetes QoS classes decide who dies first under node pressure. `dmesg` tells you whether the limit or the node ran out.

**Source:** [man7 — proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html)
