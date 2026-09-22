# Model Comparison

When multiple models or configurations are available, they should be compared using the same evaluation dataset and the same task definition.

## Comparison dimensions

- quality
- latency
- token usage
- cost
- hallucination rate
- relevance
- groundedness

## Example

| Model | Quality | Latency | Cost | Hallucination |
| --- | --- | --- | --- | --- |
| Model A | 0.91 | 1.2s | $0.012 | 0.02 |
| Model B | 0.88 | 0.9s | $0.009 | 0.04 |

## Decision guidance

The best model is not always the cheapest or fastest. The best choice is the model that meets quality thresholds while staying within operational limits.

This comparison is essential for prompt and model regression tracking.
