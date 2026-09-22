from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

base_dir = Path(__file__).resolve().parent
chart_dir = base_dir / "charts"
chart_dir.mkdir(exist_ok=True)

# Data
student_data = {
    "Hours_Studied": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Exam_Score": [40, 45, 50, 55, 65, 70, 80, 85, 95],
}

df = pd.DataFrame(student_data)
X = df[["Hours_Studied"]]
y = df["Exam_Score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

plt.figure(figsize=(8, 5))
plt.scatter(X_test, y_test, color="blue", label="Actual Scores")
plt.scatter(X_test, predictions, color="red", label="Predicted Scores")
plt.plot(sorted(X_test["Hours_Studied"]), [model.predict([[x]])[0] for x in sorted(X_test["Hours_Studied"])], color="green", linewidth=2, label="Regression Line")
plt.title("Actual vs Predicted Scores")
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.legend()
plt.grid(True)
plt.tight_layout()
output_path = chart_dir / "actual_vs_predicted.png"
plt.savefig(output_path)
plt.show()

print(f"Actual vs Predicted chart created at: {output_path}")
print("Questions to answer:")
print("1. Are predictions close to actual values?")
print("2. Where is the biggest error?")
print("3. Is the model performing reasonably?")
print("4. What could improve the model?")
