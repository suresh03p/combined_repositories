import pandas as pd
from sklearn.model_selection import train_test_split

# Example dataset
student_data = {
    "Hours_Studied": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    "Exam_Score": [40, 45, 50, 55, 60, 68, 75, 82, 90, 96, 100, 105],
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

print("Training Data (X_train):")
print(X_train)
print("\nTesting Data (X_test):")
print(X_test)
print("\nTraining Target (y_train):")
print(y_train)
print("\nTesting Target (y_test):")
print(y_test)

print("\nWhy split the data?")
print("The model should learn from training data and then be evaluated on unseen testing data.")
print("This helps us check whether the model generalizes to real-world data.")
