# Git Branching Strategy

A simple and effective branch model is:

- `feature/*` for new functionality
- `develop` for integration work
- `main` for production-ready code
- `hotfix/*` for urgent fixes

## Recommended flow

feature branch
↓
Pull Request
↓
CI tests
↓
Code review
↓
main
↓
Deployment

This keeps development work isolated, ensures quality checks before merge, and provides a consistent path to production.
