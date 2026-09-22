import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Student score data
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

print("Actual Score\tPredicted Score")
for actual, predicted in zip(y_test, predictions):
    print(f"{actual}\t\t{predicted:.2f}")

print("\nmodel.fit() means: Learn from the training data.")
print("model.predict() means: Use what was learned to predict new data.")
