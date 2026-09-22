# Day 31 - AI Model Serving

This project captures the key production patterns for serving a fine-tuned language model in a real-world inference stack.

## Architecture

- Client request enters the FastAPI application.
- Input validation checks for empty, too-long, or invalid requests.
- The inference service loads a base model and optional LoRA adapter.
- A model version and adapter metadata are attached to every response.
- Redis caching can avoid repeated work for identical prompts.
- Async queue workers can decouple request handling from model execution.
- Metrics and logs provide latency and throughput insights.

## Included components

- Base model loading scripts
- LoRA adapter loading script
- Prediction pipeline example
- Generation parameter notes
- Inference latency and memory docs
- FastAPI inference API
- Docker and Compose deployment

## Core principles

A production AI service must optimize beyond raw model quality:

- Latency
- Throughput
- Memory footprint
- Reliability
- Cost
- Version traceability

## Quick start

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the health endpoint:
   ```bash
   uvicorn app.api.inference:app --reload
   ```
4. Send a sample request:
   ```bash
   curl -X POST http://localhost:8000/inference \
     -H "Content-Type: application/json" \
     -d '{"text":"I cannot log into my account."}'
   ```

## Model serving fundamentals

Model serving is the stage where a trained model is exposed for inference in production, often behind an API or worker system. Inference differs from training because it emphasizes latency, memory, and predictable throughput rather than learning through gradients.

## Base model

A base model is a pretrained model before any domain-specific adapter or fine-tuning. It provides general language capabilities, while LoRA adapters add task-specific behavior with smaller parameter updates.

## LoRA adapter

A LoRA adapter modifies the original weights using low-rank updates, allowing efficient specialization without retraining the full model.

## Generation parameters

Key generation controls:

- temperature: higher values increase diversity
- top_k: limits sampling to the highest-probability tokens
- top_p: nucleus sampling with probability cutoff
- max_new_tokens: controls output length
- do_sample: enables stochastic decoding when true

## Inference API

The endpoint is implemented in [app/api/inference.py](app/api/inference.py).

## Caching

Identical requests can be served from Redis to reduce repeated inference cost. The cache key is often a hash of the normalized input text.

## Batching and concurrency

Both are important in production:

- Batching improves hardware utilization
- Concurrency improves throughput for multiple users
- Too much concurrency can increase latency or trigger OOM conditions

## Quantization

Quantization lowers numerical precision to reduce memory and accelerate execution. Depending on hardware and model, it may improve throughput while trading off small output quality changes.

## Monitoring

Observability includes:

- request ID
- model version
- input and output token count
- cache hit/miss
- queue wait and inference time
- success or failure

## Known limitations

This repository is intentionally designed as a project skeleton and learning scaffold. For full production deployment you should tune the model, validate real hardware behavior, and run proper load tests against your target environment.
