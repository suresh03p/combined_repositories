# Training vs Inference

| Area | Training | Inference |
|---|---|---|
| Dataset | Large labeled datasets used to learn representations and update weights. | New inputs are processed in real time or in batches; no learning is needed during the request. |
| GPU usage | High GPU demand for forward passes, backpropagation, and gradient updates. | GPU usage is usually focused on forward pass execution and may be lower per request, but highly sensitive to latency and throughput. |
| Memory | Requires storage for activations, gradients, optimizer states, and large batches. | Requires model weights, KV cache, temporary activations, and enough memory for requests under load. |
| Backpropagation | Essential for learning and updating parameters. | Not used in standard inference; only forward pass is performed. |
| Latency | Training latency is usually tolerant because it is offline. | Inference latency is critical because user-facing requests must finish quickly. |
| Cost | Volume of computation is high and expensive, especially for large models. | Cost is driven by per-request compute, memory usage, concurrency, and serving infrastructure. |
| Model updates | Parameters change continuously during training. | Parameters remain fixed after deployment unless a new version or adapter is loaded. |

## Why production inference has different requirements
Production inference is optimized for repeatability, bounded latency, low memory use, and service reliability. A model may be highly accurate during training but still fail in production if it is too slow, too memory-hungry, or too variable under concurrent load. Inference systems therefore prioritize throughput, version tracking, caching, batching, and operational stability.
