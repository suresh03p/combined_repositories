# IAM and Security

## Authentication versus authorization

**Authentication** answers: “Who or what are you?” **Authorization** answers: “What may that identity do?” A successful login does not grant permission to read ECR, change EC2, or access secrets.

## IAM building blocks

- **User:** a human identity. Prefer federation or IAM Identity Center for people instead of long-lived access keys.
- **Role:** an assumable identity for AWS services, workloads, or operators. EC2 should use an instance role to pull from ECR and publish logs.
- **Policy:** JSON rules that allow or deny actions against resources.
- **Permission:** the effective result of applicable policies, resource policies, boundaries, and explicit denies.
- **Temporary credentials:** short-lived access key, secret, and session token issued when a role is assumed.

Apply least privilege: grant only required actions, resources, and conditions; separate build, deploy, runtime, and read-only roles; review access regularly; enable MFA for human operators; and log IAM activity with CloudTrail.

## Credential rule

Never commit AWS credentials or LLM keys to GitHub, a Dockerfile, source code, README, or a committed `.env` file. Use local AWS profiles, environment variables supplied by a secret manager, GitHub OIDC for CI, and EC2 instance roles. Rotate and revoke exposed keys immediately.

## Minimum role intent

- CI role: push a specific repository in ECR and deploy the approved artifact.
- EC2 role: pull images from the specific ECR repository and write to the specific CloudWatch log group.
- Operator role: inspect production and deploy through an approved process, with no application secret read unless required.
