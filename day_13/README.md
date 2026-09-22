# Day 8 ML Preprocessing

Runnable lessons for numerical and categorical features, missing values, encoding, scaling, leakage, `ColumnTransformer`, and reusable scikit-learn pipelines.

## Run

Install dependencies:

```bash
python -m pip install pandas numpy scikit-learn
```

Run the complete project:

```bash
python employee_salary_pipeline.py
```

The first run creates 520 intentionally imperfect employee records in `data/employees.csv`, saves `models/employee_salary_pipeline.pkl`, and writes `reports/model_evaluation.md`. The prediction for the new employee is made by passing raw data to the fitted pipeline; no preprocessing is repeated manually.

## Evaluation questions

1. Preprocessing makes mixed data usable and keeps transformations consistent; compare the complete pipeline with a raw numeric-only baseline if a formal improvement claim is needed.
2. Experience, performance, age, and education generally carry signal because the synthetic salary formula uses them.
3. One-hot encoding creates separate indicator columns and ignores unseen categories safely.
4. Missing values are handled by median numerical imputation and most-frequent categorical imputation.
5. The pipeline prevents leakage because it is fit after the train/test split and learns transformation statistics from training rows only.