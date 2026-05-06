# ADR-00008: Adding CloudWatch resource monitoring.

## Status
Accepted

## Summary
Added CloudWatch resource monitoring through AWS so we get alert emails.

## Decision
Decided to use CloudWatch resource monitoring, as it is native to AWS and will email me when resources are struggling.

Decided to monitor the following items:
- ECS # of tasks (if 0, service outage)
- ALB 5XX Errors (we shouldn't be getting a lot of server errors)
- ALB Unhealthy Targets (backend tasks not healthy)
- ALB latency (the API needs to be quick)
- ECS CPU & Memory (if too high, we need to add more containers)
- RDS Low Storage (probably will never happen, but should know when it does)
