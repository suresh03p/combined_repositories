# Inference Baseline

## Objective
Measure baseline latency for repeated requests on the inference service.

## Example measurements
- 10 requests: estimate latency across repeated API calls
- 50 requests: collect median and tail latency
- 100 requests: capture throughput and variance

## Metrics
- Average latency
- P50
- P95
- P99
- Tokens/second
- Requests/second

## Notes
In production, P95 and P99 are often more important than average because they reflect tail latency under load.

## Recommendation
Use a consistent benchmark harness and repeat measurements several times to reduce noise.
