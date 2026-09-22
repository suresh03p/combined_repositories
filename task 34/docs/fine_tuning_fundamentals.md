# Fine-Tuning Fundamentals

## What is fine-tuning?
Fine-tuning is the process of taking a pretrained model and adapting it to a narrower task or domain using additional training data. Instead of building a model from scratch, we start from a model that already learned broad language patterns and then specialize it for a target behavior.

## Pretraining vs fine-tuning
Pretraining teaches a model general language understanding using large-scale data and self-supervised objectives. It helps the model learn grammar, semantics, and broad world knowledge. Fine-tuning uses a smaller, task-specific dataset to steer the model toward a defined behavior such as intent classification, summarization, or instruction following.

The key idea is:

- Pretraining: broad capability
- Fine-tuning: focused specialization

## Instruction tuning
Instruction tuning trains a model to follow natural-language instructions more reliably. The model learns to map an instruction and input to the expected answer. This is especially useful when a model must follow a given behavior consistently across many similar requests.

## Supervised fine-tuning
Supervised fine-tuning (SFT) uses labeled examples where each example contains an input and a target output. The model learns to minimize differences between its prediction and the expected answer. For classification tasks, this means learning the correct label for each pattern; for generation tasks, it learns the expected text.

## Domain adaptation
Domain adaptation changes a model's behavior for a specific area such as customer support, medical documentation, legal drafting, or financial analysis. The goal is to improve performance on terms, phrasing, and patterns common to that domain without starting from zero.

## Parameter-efficient fine-tuning
Full fine-tuning updates all model parameters, which can require large memory and compute. Parameter-efficient fine-tuning (PEFT) keeps most model weights frozen and trains only a small subset of parameters. This reduces memory consumption, cost, and training time while still providing strong task adaptation.

## LoRA
Low-Rank Adaptation (LoRA) injects trainable low-rank matrices into selected layers of the model while leaving the original weights mostly untouched. It is efficient because it updates a small number of parameters rather than the full model.

The main intuition is:

- Base model weights remain frozen
- Small adapter matrices are trained
- The model gains task-specific behavior with limited compute

## PEFT
PEFT is a family of methods that includes LoRA and related approaches. It is useful when:

- GPU memory is limited
- Training time must stay low
- The model must be stored in a smaller footprint
- Multiple task adapters are needed for different use cases

## Why fine-tuning matters
Fine-tuning is appropriate when the task is stable, the required behavior is specific, and repeated examples exist. It is not a replacement for retrieval when the required knowledge is current or private.

### Key reminder
Fine-tuning changes learned behavior; it does not add new documents or real-time knowledge automatically. For current facts, retrieval is often the better tool.
