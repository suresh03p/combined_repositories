# Base Model Selection

## Selected model
google/flan-t5-small

## Model details
- Model: FLAN-T5 Small
- Model size: roughly 80M parameters
- License: Apache 2.0
- Expected hardware: CPU or lightweight GPU
- Context length: 512 tokens (default encoder-decoder context)
- Tokenizer: T5 tokenizer
- Use case: compact instruction-following model suitable for a small classification fine-tuning task

## Why this model was chosen
This model is small enough to fine-tune in a resource-limited environment while still being instruction-capable. It is a realistic choice for a controlled experiment and demonstrates the basic fine-tuning workflow without requiring a very large model.

## Why not simply choose the biggest model
Large models may have better general ability, but they are more expensive to fine-tune, slower to evaluate, and often exceed the available hardware. The goal is to pick the smallest useful model that does the task well enough for a realistic demo.

## Practical fit
For this project, a small instruction model is sufficient because we are classifying a fixed set of intents in a narrow domain. The primary challenge is behavior calibration, not broad-world reasoning.
