"""Calculate and plot residuals for the study-hours example."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).parent
X = np.array([[2], [3], [4], [5], [6], [7], [8]], dtype=float)
y = np.array([40, 45, 52, 60, 68, 75, 82], dtype=float)

model = LinearRegression().fit(X, y)
predicted = model.predict(X)
results = pd.DataFrame({"Actual": y, "Predicted": predicted})
results["Error"] = results["Actual"] - results["Predicted"]
results["Absolute_Error"] = results["Error"].abs()

print(results.round(2).to_string(index=False))
print("Largest error:", results.loc[results["Absolute_Error"].idxmax()].round(2).to_dict())
print("Smallest error:", results.loc[results["Absolute_Error"].idxmin()].round(2).to_dict())
print("Average error:", round(results["Error"].mean(), 2))

plt.figure(figsize=(7, 5))
plt.scatter(results["Actual"], results["Predicted"], color="#0f766e", s=70)
line_min, line_max = results[["Actual", "Predicted"]].min().min(), results[["Actual", "Predicted"]].max().max()
plt.plot([line_min, line_max], [line_min, line_max], "--", color="#b45309")
plt.xlabel("Actual score")
plt.ylabel("Predicted score")
plt.title("Actual vs Predicted Exam Scores")
plt.tight_layout()
plt.savefig(ROOT / "charts" / "actual_vs_predicted.png", dpi=150)
plt.close()