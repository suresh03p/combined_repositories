# Docker Image Versioning

A predictable image tagging strategy is essential for safe production deployments.

Examples:
- `production-ai-api:<git-sha>`
- `production-ai-api:v1.0.0`

These tags let teams identify exactly which source revision produced the running image.

## Why not use only `latest`

The `latest` tag is ambiguous and can be overwritten. In production, that makes debugging and rollback difficult because it is not clear which build is actually running. Using immutable tags like a Git SHA or semantic version ensures traceability and repeatability.

## Recommended practice

- Tag each build with a unique Git SHA for traceability
- Tag release builds with a semantic version such as `v1.0.0`
- Keep previous images available for rollback
- Avoid mutating a previously released tag
