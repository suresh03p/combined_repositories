# CI/CD IAM Permissions

The deployment identity should be limited to the minimum resources needed to complete its job.

## Minimum required access

- Amazon ECR permissions to push and pull container images
- Access to the deployment target, such as EC2 or the ECS/ECR related resources
- Permissions required for application startup, environment setup, and log access only when strictly required

## Principles

- Use least privilege
- Prefer temporary credentials over long-lived keys
- Use IAM roles and OIDC for GitHub Actions when possible
- Restrict access by account, region, and resource scope

## Example principle

The CI/CD identity should not have full administrative access to the AWS account. It should only be allowed to perform deployment tasks necessary for the application runtime.

## AWS credential security rule

Never write AWS access keys directly inside source code or workflow files. Use repository secrets or federated identity. For example, store them as GitHub Actions secrets and use OIDC-based AWS authentication whenever possible.
