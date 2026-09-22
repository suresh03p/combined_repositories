# PEFT: Parameter-Efficient Fine-Tuning

## What PEFT is
Parameter-efficient fine-tuning is a family of training strategies that updates only a small part of a model instead of all weights. This helps keep the base model stable while learning the new task.

## Why PEFT matters
PEFT reduces:

- GPU memory usage
- Training cost
- Training time
- Storage requirements for adapters

## Full fine-tuning vs LoRA / PEFT

| Approach | Parameters updated | Memory use | Training cost | Storage | Typical use |
|---|---|---|---|---|---|
| Full Fine-Tuning | All model parameters | High | High | Large | Large labs or big compute budgets |
| LoRA / PEFT | Small adapter parameters | Lower | Lower | Small | Practical domain-specific adaptation |

## Why LoRA is a common PEFT method
LoRA adds small trainable low-rank matrices into selected layers. The original model weights remain mostly frozen, which makes training cheaper and simpler while still allowing the model to learn domain-specific behavior.

## Main lesson
PEFT is valuable when the task is narrow, the data is realistic, and the goal is to get a strong task-specific result without paying the cost of full-model retraining.
