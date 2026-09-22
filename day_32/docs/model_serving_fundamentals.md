# Model Serving Fundamentals

## Model serving
Model serving is the process of deploying a trained model so that it can consume input and produce predictions in a production environment. The model is usually packaged behind an API, worker, or service layer that receives requests and returns outputs.

## Inference
Inference is the act of running a trained model on new data to generate predictions. Unlike training, inference is usually optimized for speed, memory efficiency, and low-latency responses.

## Online inference
Online inference handles requests in real time as they arrive. This pattern is common in interactive systems like chatbots, search assistants, and customer support APIs.

## Batch inference
Batch inference processes groups of requests together. This is efficient when latency is less important than throughput, such as offline scoring or bulk classification.

## Real-time inference
Real-time inference aims to respond quickly enough for interactive workflows. It often balances latency constraints with throughput and cost.

## Model server
A model server is a service that manages model loading, request handling, batching, concurrency, and output delivery. It is responsible for making the model accessible to clients.

## Inference API
An inference API exposes model functionality through an HTTP endpoint or RPC interface. Clients send input data and receive predictions or generated text.

## Model loading
Model loading includes reading the model weights and configuration from disk or a registry and preparing them for inference. In production, this is often done once and reused across requests.

## Warm model
A warm model is already loaded into memory and ready to serve new requests. Warm starts are faster because they avoid repeated initialization overhead.

## Cold start
A cold start happens when a model is not yet loaded or when the process has just started. The first request may take much longer because the model must be loaded and initialized.

## Why these matter
Production inference needs to consider quality, cost, memory, throughput, and latency together. A model that answers correctly but cannot meet response-time or resource requirements is not production-ready.
