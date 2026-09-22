# Rollback Strategy

Rollback is a required control when a deployment introduces an error or a service becomes unhealthy.

## Example flow

`v1.0.0 = working`
`v1.0.1 = broken`

1. Deploy `v1.0.1`
2. Health check fails
3. Roll back to `v1.0.0`
4. Verify health passes again

## Principles

- Keep previous image versions available
- Use a reliable tagging strategy
- Trigger automatic rollback on health-check failure when appropriate
- Maintain clear deployment history for incident response
