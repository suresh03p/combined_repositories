"""Compare polynomial degrees on a curved relationship."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

ROOT = Path(__file__).parent
rng = np.random.default_rng(12)
X = np.linspace(-3, 3, 80).reshape(-1, 1)
y = 4 * X.ravel() ** 2 + 2 * X.ravel() + 5 + rng.normal(0, 2.0, len(X))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=12)

rows = []
for degree in [1, 2, 3, 5]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression()).fit(X_train, y_train)
    prediction = model.predict(X_test)
    rows.append((degree, mean_absolute_error(y_test, prediction), np.sqrt(mean_squared_error(y_test, prediction)), r2_score(y_test, prediction)))

print("Degree | MAE | RMSE | R2")
for degree, mae, rmse, r2 in rows:
    print(f"{degree:>6} | {mae:>5.2f} | {rmse:>5.2f} | {r2:>.3f}")

grid = np.linspace(-3.1, 3.1, 300).reshape(-1, 1)
plt.figure(figsize=(8, 5))
plt.scatter(X, y, color="#334155", alpha=0.55, label="data")
for degree in [1, 2, 3, 5]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression()).fit(X_train, y_train)
    plt.plot(grid, model.predict(grid), label=f"degree {degree}")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Polynomial Regression Degrees")
plt.legend()
plt.tight_layout()
plt.savefig(ROOT / "charts" / "polynomial_comparison.png", dpi=150)
plt.close()