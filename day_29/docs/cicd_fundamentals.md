# CI/CD Fundamentals

## Continuous Integration (CI)

Continuous Integration is the practice of automatically testing code changes as soon as they are pushed to a shared repository. The goal is to catch integration issues quickly and keep the codebase in a deployable state.

Key ideas:
- Developers merge frequently
- Automated tests run on every change
- Build and validation happens automatically
- Broken code is detected early

## Continuous Delivery (CD)

Continuous Delivery expands CI by making it easy to prepare release-ready artifacts for deployment. Code passes through automated validation and is kept in a state that can be deployed on demand.

## Continuous Deployment (CD)

Continuous Deployment goes one step further: every validated change is automatically pushed to production, provided the tests and checks pass.

## Build Pipeline

A build pipeline automates the process of compiling, installing dependencies, running tests, and packaging an application. It ensures the application can be built reproducibly.

## Deployment Pipeline

A deployment pipeline handles the release flow after build validation, such as pushing a container image to a registry, updating infrastructure, and starting the new application version.

## Automated Testing

Automated tests reduce manual verification effort and help catch bugs across health endpoints, authentication, data workflows, and deployment validation.

## Deployment Gates

Deployment gates are checkpoints that block a release if required conditions are not met, such as failing unit tests, unstable health checks, or misconfigured environment variables.

## Rollback

Rollback is the process of reverting to a previous working version when a deployment fails or a new release introduces instability. Rollback is essential for maintaining reliable production operations.

## Relationship Summary

CI = Automatically test code changes.
CD = Automatically prepare and deploy tested code.
