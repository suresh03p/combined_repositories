# AWS Fundamentals

## Core concepts

- **Cloud computing:** on-demand compute, storage, networking, and managed services billed according to use instead of owned hardware.
- **Region:** an independent geographic area containing multiple isolated Availability Zones.
- **Availability Zone (AZ):** one or more separate data centers within a Region, with independent power and networking.
- **Compute:** EC2 virtual machines, containers, serverless functions, or managed Kubernetes capacity that runs application code.
- **Storage:** durable object storage such as S3, block storage such as EBS, and databases for structured data.
- **Networking:** VPCs, subnets, routes, load balancers, DNS, and security controls that connect services safely.
- **IAM:** AWS Identity and Access Management controls who or what may perform which actions on which resources.
- **Managed services:** AWS operates much of the infrastructure and maintenance, for example ECR, RDS, ElastiCache, and CloudWatch.
- **Monitoring:** CloudWatch logs, metrics, alarms, dashboards, and events used to detect and investigate operational problems.

## Local machine, Docker, and cloud

```text
Local machine: developer hardware, local network, local files, and local credentials.
       |
Docker: repeatable image and isolated process, but still uses the host's CPU, memory, and network.
       |
Cloud infrastructure: remotely operated AWS resources with IAM, networking, availability, billing, and monitoring.
```

Docker packages the application; it does not provide the server, durable data, IAM, or production availability by itself. AWS supplies those infrastructure boundaries. The image built locally should be immutable and promoted through environments; configuration and secrets are injected at runtime.

## Deployment account structure

Use these dimensions in resource names and tags:

| Dimension | Example |
| --- | --- |
| Project | `ai-api` |
| Environment | `production` |
| Region | `us-east-1` |
| Resource | `ecr`, `api`, `logs`, `ec2` |
| Owner | `platform-team` |

Preferred names include `production-ai-api`, `production-ai-ecr`, and `production-ai-logs`. Apply the same values as tags, including `Project`, `Environment`, `ManagedBy`, and `Owner`.
