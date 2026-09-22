# Manual vs Automated Deployment

## Manual Deployment Flow

The Day 26 manual deployment process is:

Code
↓
Docker Build
↓
Docker Tag
↓
ECR Login
↓
ECR Push
↓
EC2 Login
↓
Pull Image
↓
Stop Old Container
↓
Start New Container
↓
Test API

This flow depends on engineers remembering and performing every step manually. It is slow, error-prone, and hard to reproduce consistently.

## Automated Equivalent

Git Push
↓
CI
↓
Test
↓
Build
↓
Push
↓
Deploy
↓
Health Check

The automated pipeline ensures the same workflow is executed consistently every time code changes are introduced. It reduces human error and enables repeatable releases.

## Benefits of Automation

- Faster delivery
- Reliable deployments
- Better traceability
- Reduced operational mistakes
- Easier rollback
- Standardized validation before production
