# Day29 AI Evaluation

This repository contains a practical AI evaluation framework for testing response quality, grounding, retrieval, safety, and regression risk for LLM-based applications.

## Project purpose

The goal is to move beyond "HTTP 200" and ask whether the answer is:

- correct
- relevant
- grounded in evidence
- supported by retrieved sources
- safe and non-hallucinatory
- stable across prompt and model changes

## Repository layout

```text
Day29_AI_Evaluation/
├── app/
├── docs/
├── evaluation/
├── prompts/
├── reports/
├── tests/
├── Dockerfile
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Included assets

- AI testing fundamentals overview
- Semantic evaluation guidance
- Golden dataset and evaluation datasets
- Exact match, semantic, relevance, and groundedness checks
- Retrieval quality and context relevance analysis
- Prompt regression comparison
- Safety and adversarial datasets
- Reporting and quality gate logic

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python evaluation/evaluator.py
python evaluation/generate_report.py
```

## Quality thresholds

The default thresholds are:

- Relevance >= 0.80
- Groundedness >= 0.85
- Retrieval Hit Rate >= 0.90
- Hallucination Rate <= 0.05

If any metric falls below threshold, the quality gate fails and deployment should be blocked.

## Evaluation flow

```text
Dataset
  ↓
AI Application
  ↓
Response + Retrieved Context
  ↓
Exact / Semantic / Relevance / Groundedness Checks
  ↓
Retrieval and Safety Evaluation
  ↓
Quality Gate
  ↓
Report
```

## Notes

This is a training-oriented evaluation harness. It uses a local mock AI response layer to demonstrate the testing workflow in a controlled and reproducible way.
