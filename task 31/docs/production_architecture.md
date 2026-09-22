# Production Architecture

```text
Internet
   |
HTTPS load balancer / reverse proxy (public subnet)
   |
FastAPI container on EC2 or ECS (private subnet where practical)
   |
Redis, PostgreSQL, and vector storage (private subnets)
   |
LLM provider through controlled egress
```

## Region and Availability Zone choice

Choose a Region based on user latency, data residency and compliance, support requirements, disaster recovery, service availability, and total cost. Place production components across at least two AZs when the service and budget justify it. Confirm that the selected Region offers the required EC2 types, ECR, CloudWatch, database, cache, and networking features before committing.

## VPC basics

- A VPC is the account's isolated network boundary.
- Public subnets have a route to an Internet Gateway; private subnets do not accept unsolicited internet traffic.
- Route tables determine where packets go.
- A NAT Gateway gives private workloads outbound access for updates or provider calls without making them public.
- Security Groups are stateful allow rules attached to network interfaces. Permit only required source CIDRs or security groups.

## Data layer decision

Run the FastAPI process and background worker in containers. Prefer Amazon RDS for PostgreSQL and ElastiCache for Redis in production because backups, patching, failover, and maintenance are managed. Choose a managed vector-capable database or a PostgreSQL extension after validating workload and availability requirements. Self-managed services are acceptable for learning or strict customization, but require backup, patching, scaling, and failure ownership.
