# Understanding LoRA

## Concept
Low-Rank Adaptation (LoRA) is a parameter-efficient strategy for fine-tuning large language models. Instead of updating all weights, LoRA adds small trainable matrices to selected layers while the original model remains mostly frozen.

```text
Base Model
   |
   | Frozen Parameters
   |
   +----> LoRA Adapter
              |
              v
        Train Small Number
        of Parameters
```

## Frozen model weights
The original pretrained model is preserved. This reduces the risk of catastrophic forgetting and keeps the base model stable.

## Trainable adapter weights
The LoRA adapter contains trainable low-rank matrices. These are the only parts updated during fine-tuning. The adapted model gains task-specific behavior while keeping the larger model fixed.

## Rank
The rank controls how much capacity the adapter has. A lower rank means fewer trainable parameters and a smaller adapter footprint. A higher rank can represent more complexity but costs more memory and training time.

## Adapter layers
LoRA is typically applied to transformer attention and feed-forward layers. This is a targeted way to adapt the model without retraining everything.

## Parameter efficiency
LoRA is efficient because it reduces:

- GPU memory usage
- Training cost
- Training time
- Stored model size for adapted versions

## Why LoRA is useful
For many tasks, task-specific behavior is more important than full-model retraining. LoRA gives a practical compromise between quality and efficiency.
