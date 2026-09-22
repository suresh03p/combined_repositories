# Day 9 Regression

This folder is a complete beginner-friendly regression practice set. It includes
simple linear regression, residual analysis, multiple regression, metrics,
polynomial regression, Ridge, Lasso, Elastic Net, cross-validation, and a final
house-price model comparison.

## Run it

From this folder:

```powershell
python linear_regression.py
python residual_analysis.py
python multiple_regression.py
python regression_metrics.py
python polynomial_regression.py
python ridge_regression.py
python lasso_regression.py
python elastic_net.py
python cross_validation.py
python house_price_regression/run_project.py
```

The final command creates `data/house_prices.csv` with 500 records, saved models,
charts, `model_comparison.csv`, and `Model_Comparison_Report.md`.

## Dependencies

```powershell
python -m pip install numpy pandas scikit-learn matplotlib
```

The examples use synthetic data for learning. Do not treat the generated house
prices as real market valuations.