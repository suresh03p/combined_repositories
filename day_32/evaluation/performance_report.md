# Performance Report

## Scope
This report summarizes the expected behavior of the inference service under small load tests.

## Benchmark pattern
- 10 requests
- 50 requests
- 100 requests
- concurrency: 5, 10, 20

## Metrics tracked
- P50
- P95
- P99
- throughput
- error rate
- memory usage
- CPU/GPU utilization

## Interpretation
High concurrency increases throughput but may increase latency and memory use. Tail latency (P95/P99) is often a critical production metric.
