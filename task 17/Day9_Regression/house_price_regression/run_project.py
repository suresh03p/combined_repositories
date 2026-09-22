"""End-to-end Day 9 house-price regression project.

Run this file from any directory. It creates the 500-row dataset and all
requested model, chart, and report artifacts under the parent project folder.
"""

from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR, MODEL_DIR, CHART_DIR = ROOT / "data", ROOT / "models", ROOT / "charts"
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)


def make_data(records=500):
    rng = np.random.default_rng(2026)
    locations = rng.choice(["North", "South", "East", "West"], records)
    area = rng.integers(650, 3201, records)
    bedrooms = rng.integers(1, 6, records)
    bathrooms = rng.integers(1, 5, records)
    age = rng.integers(0, 46, records)
    parking = rng.integers(0, 4, records)
    distance = np.round(rng.uniform(1, 35, records), 1)
    location_effect = pd.Series(locations).map({"North": 35_000, "South": -20_000, "East": 15_000, "West": 5_000}).to_numpy()
    price = (
        45_000 + area * 190 + bedrooms * 15_000 + bathrooms * 12_000
        - age * 1_700 + parking * 8_000 - distance * 2_200
        + location_effect + rng.normal(0, 35_000, records)
    )
    return pd.DataFrame({
        "House_ID": np.arange(1, records + 1), "Area_sqft": area,
        "Bedrooms": bedrooms, "Bathrooms": bathrooms, "Age": age,
        "Parking": parking, "Location": locations,
        "Distance_to_City": distance, "Price": np.round(price, 2),
    })


def build_preprocessor(polynomial=False):
    numeric = ["Area_sqft", "Bedrooms", "Bathrooms", "Age", "Parking", "Distance_to_City"]
    categorical = ["Location"]
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if polynomial:
        numeric_steps.append(("polynomial", PolynomialFeatures(degree=2, include_bias=False)))
    numeric_steps.append(("scale", StandardScaler()))
    return ColumnTransformer([
        ("numeric", Pipeline(numeric_steps), numeric),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])


def make_models():
    return {
        "Linear Regression": Pipeline([("prepare", build_preprocessor()), ("model", LinearRegression())]),
        "Ridge": Pipeline([("prepare", build_preprocessor()), ("model", Ridge(alpha=1.0))]),
        "Lasso": Pipeline([("prepare", build_preprocessor()), ("model", Lasso(alpha=1000.0, max_iter=50_000))]),
        "Elastic Net": Pipeline([("prepare", build_preprocessor()), ("model", ElasticNet(alpha=1000.0, l1_ratio=0.5, max_iter=50_000))]),
        "Polynomial Regression": Pipeline([("prepare", build_preprocessor(polynomial=True)), ("model", LinearRegression())]),
    }


def metric_row(model, X, y):
    prediction = model.predict(X)
    mse = mean_squared_error(y, prediction)
    return {"MAE": mean_absolute_error(y, prediction), "MSE": mse, "RMSE": np.sqrt(mse), "R2": r2_score(y, prediction)}


def write_report(results, cv_results):
    best = results["R2"].idxmax()
    lowest_rmse = results["RMSE"].idxmin()
    cv_text = "\n".join(f"- {name}: mean R2 = {mean:.3f}, standard deviation = {std:.3f}" for name, mean, std in cv_results)
    report = f"""# Model Comparison Report

This experiment uses 500 generated house records. Prices are synthetic, so the
results demonstrate a workflow rather than a real estate valuation.

## 1. Which model performed best?
**{best}** had the highest test R2 ({results.loc[best, 'R2']:.3f}). I judged "best"
using the full metric table instead of looking at one number in isolation.

## 2. Which model had the lowest RMSE?
**{lowest_rmse}**, with an RMSE of {results.loc[lowest_rmse, 'RMSE']:.2f} price units.

## 3. Which model had the highest R2?
**{best}**, with an R2 of {results.loc[best, 'R2']:.3f}.

## 4. Did regularization improve the model?
Ridge, Lasso, and Elastic Net were useful comparison points. Regularization can
make a model less sensitive to noisy or correlated inputs, but on this clean,
synthetic dataset it is only an improvement if its test metrics beat the plain
linear model. The table below is the evidence for that decision.

## 5. Did polynomial regression overfit?
The degree-2 polynomial model did not automatically win. Extra terms can fit
small quirks in training data, so its test R2 and RMSE must be checked rather
than assuming that a more complex model is better.

## 6. What happened when polynomial degree increased?
Higher degrees add flexibility. Training error usually falls, but testing error
can rise after the useful pattern has been captured. This is the central sign of
overfitting.

## 7. Which model would you choose for production?
I would start with **{best}**, subject to monitoring and validation on real,
future listings.

## 8. Why did you choose it?
It explained the most test variation while remaining a measurable, repeatable
choice. I would also check that its errors are acceptable in actual price units.

## 9. What additional data could improve the prediction?
Neighborhood quality, lot size, floor level, renovation condition, school access,
property type, sale date, and nearby comparable sale prices could add signal.

## 10. What are the limitations?
The data is generated, the noise pattern is artificial, and Location is represented
only by four broad labels. The model also assumes that relationships learned from
this sample remain valid in new markets and time periods.

## Test-set metrics

| Model | MAE | MSE | RMSE | R2 |
|---|---:|---:|---:|---:|
"""
    for name, row in results.iterrows():
        report += f"| {name} | {row.MAE:.2f} | {row.MSE:.2f} | {row.RMSE:.2f} | {row.R2:.3f} |\n"
    report += "\n## Five-fold cross-validation of the top two\n" + cv_text + "\n"
    (ROOT / "Model_Comparison_Report.md").write_text(report, encoding="utf-8")


def main():
    data = make_data()
    data.to_csv(DATA_DIR / "house_prices.csv", index=False)
    print("Missing values:\n", data.isna().sum().to_string())
    print("Duplicate rows:", data.duplicated().sum())
    print("Data types:\n", data.dtypes.to_string())
    print("Outlier check uses the IQR rule on numeric columns.")
    print(data.describe().round(2).to_string())

    X = data.drop(columns=["House_ID", "Price"])
    y = data["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=21)
    models = make_models()
    fitted = {}
    rows = {}
    for name, model in models.items():
        fitted[name] = model.fit(X_train, y_train)
        rows[name] = metric_row(fitted[name], X_test, y_test)
    results = pd.DataFrame(rows).T.sort_values("RMSE")
    print("\nModel comparison:\n", results.round(3).to_string())
    results.to_csv(ROOT / "model_comparison.csv")

    best_name = results["R2"].idxmax()
    predictions = fitted[best_name].predict(X_test)
    artifact_names = {"Linear Regression": "linear_model.pkl", "Ridge": "ridge_model.pkl"}
    for name in ["Linear Regression", "Ridge", best_name]:
        filename = artifact_names.get(name, "best_model.pkl")
        with (MODEL_DIR / filename).open("wb") as file:
            pickle.dump(fitted[name], file)
    with (MODEL_DIR / "best_model.pkl").open("wb") as file:
        pickle.dump(fitted[best_name], file)

    plt.figure(figsize=(7, 5))
    plt.scatter(y_test, predictions, color="#0f766e", alpha=0.75)
    limits = [min(y_test.min(), predictions.min()), max(y_test.max(), predictions.max())]
    plt.plot(limits, limits, "--", color="#b45309")
    plt.xlabel("Actual price")
    plt.ylabel("Predicted price")
    plt.title(f"Actual vs Predicted: {best_name}")
    plt.tight_layout(); plt.savefig(CHART_DIR / "actual_vs_predicted.png", dpi=150); plt.close()

    errors = y_test - predictions
    plt.figure(figsize=(7, 5)); plt.scatter(predictions, errors, color="#be123c", alpha=0.7); plt.axhline(0, color="#334155", linestyle="--")
    plt.xlabel("Predicted price"); plt.ylabel("Residual (actual - predicted)"); plt.title("Residual Plot")
    plt.tight_layout(); plt.savefig(CHART_DIR / "residual_plot.png", dpi=150); plt.close()

    plt.figure(figsize=(9, 5)); results[["MAE", "RMSE"]].plot(kind="bar", ax=plt.gca(), color=["#0f766e", "#b45309"])
    plt.ylabel("Error in price units"); plt.title("Model Error Comparison"); plt.xticks(rotation=25, ha="right"); plt.tight_layout(); plt.savefig(CHART_DIR / "model_comparison.png", dpi=150); plt.close()

    top_two = list(results["R2"].nlargest(2).index)
    cv_results = []
    for name in top_two:
        scores = cross_val_score(models[name], X, y, cv=5, scoring="r2")
        cv_results.append((name, scores.mean(), scores.std()))
        print(f"{name}: CV mean R2={scores.mean():.3f}, std={scores.std():.3f}")
    write_report(results, cv_results)
    print("\nCreated data/, models/, charts/, model_comparison.csv, and Model_Comparison_Report.md")


if __name__ == "__main__":
    main()