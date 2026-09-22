# Cost Estimation

AWS pricing varies by Region, usage, purchase model, and date. Use the AWS Pricing Calculator and set billing alarms before creating production resources.

| Cost area | Main drivers | Control |
| --- | --- | --- |
| EC2 | instance hours, EBS, public IPv4 | right-size, stop test instances, use Savings Plans when stable |
| ECR | stored image GB and transfer | prune old images with lifecycle policies |
| Storage | EBS, snapshots, S3, database storage | retention and lifecycle policies |
| Network | internet egress, NAT Gateway processing, cross-AZ traffic | keep chatty services local; use endpoints where appropriate |
| Load Balancer | hours and processed capacity units | use only when availability and routing require it |
| CloudWatch | ingested/stored logs, metrics, alarms | structured logs, retention, sampling |
| Database | instance hours, storage, I/O, backups | right-size and schedule non-production downtime |
| Redis | node hours and storage | size for working set and availability target |
| LLM API | input/output tokens, model, embeddings, retries | budgets, limits, caching, prompt controls |

AI infrastructure cost is both cloud infrastructure and model/API usage. A low-cost EC2 instance can still produce a large bill through LLM tokens, retries, NAT traffic, or logs.
