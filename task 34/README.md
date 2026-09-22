# Fine-Tuned Customer Support AI

## Problem statement
Customer support teams need to route incoming messages into the correct intent category before they can triage or respond efficiently. This project builds a controlled fine-tuning workflow for a small customer-support intent classification task.

## Why fine-tuning was selected
This task depends on consistent behavior for a fixed set of support intents such as account login issues, payment issues, refund requests, technical issues, and general queries. A small, domain-specific improvement in output consistency is more reliable with a task-specific fine-tuned adapter than with a generic prompt alone.

## Why RAG was not the primary solution
RAG is best for external or frequently changing factual knowledge. This task is mostly about classifying customer message intent based on patterns and domain language. The main need is learned behavior, not document retrieval. Prompting alone can handle simple cases, but a fine-tuned adapter improves consistency for repeated task behavior.

## Dataset structure
Each record follows a consistent instruction format:

```json
{
  "instruction": "Classify the customer message.",
  "input": "I cannot log into my account.",
  "output": "account_login_issue"
}
```

Files:
- data/train.jsonl
- data/validation.jsonl
- data/test.jsonl

Dataset size:
- Training: 120 examples
- Validation: 25 examples
- Test: 25 examples

## Base model
Selected model: google/flan-t5-small

- Model size: ~80M parameters
- License: Apache 2.0
- Expected hardware: CPU or small GPU for fine-tuning; 16GB RAM is sufficient for a small experiment
- Context length: 512 tokens by default
- Tokenizer: T5 tokenizer
- Use case: compact instruction-following model with manageable compute needs

## LoRA configuration
The project uses a lightweight PEFT setup based on LoRA. The adapter keeps the base model frozen and trains a small number of low-rank parameters.

## Training configuration
Key settings include:
- learning rate: 2e-4
- batch size: 4
- gradient accumulation: 8
- epochs: 3
- warmup ratio: 0.1
- weight decay: 0.01
- evaluation frequency: every epoch
- checkpoint frequency: every epoch

## Training results
The small controlled experiment produced stable learning, with validation loss decreasing over the first few epochs before plateauing.

## Baseline results
See evaluation/baseline_results.json.

## Fine-tuned results
See evaluation/finetuned_results.json.

## Before vs after comparison
The fine-tuned model improved intent correctness and reduced invalid or ambiguous classifications compared with the base model. Gains were strongest for recurring patterns and domain-specific phrasing.

## Failure analysis
The main risks include label noise, class imbalance, poor formatting, or undertraining. A weak base model or poor prompt formatting can reduce performance despite fine-tuning.

## Model version
The repository uses versioned artifacts under models/v1_base and models/v1_lora.

## Deployment considerations
This is a small, narrow classification system. It is best suited for routing support tickets or triaging message intent before escalation. For rapidly changing knowledge, use RAG or tool-calling instead of relying only on a fine-tuned model.

## Project structure
```text
Day30_LLM_Fine_Tuning/
├── data/
├── training/
├── scripts/
├── evaluation/
├── models/
├── docs/
├── requirements-training.txt
├── README.md
├── .gitignore
└── ...
```

## Summary
This project demonstrates a controlled fine-tuning workflow: define the task, validate data, tokenize, choose a small model, train a LoRA adapter, evaluate objectively, compare with a baseline, and version the artifacts for deployment.
