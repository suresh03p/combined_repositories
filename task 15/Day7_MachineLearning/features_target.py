import pandas as pd

# Data for learning the meaning of features and target
student_data = {
    "Hours_Studied": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Exam_Score": [40, 45, 50, 55, 65, 70, 80, 85, 95],
}

df = pd.DataFrame(student_data)

print("Dataset:")
print(df)
print("\nFeature matrix X:")
X = df[["Hours_Studied"]]
print(X)
print("\nTarget y:")
y = df["Exam_Score"]
print(y)

print("\nWhy X is Input:")
print("X contains the information sent to the model to learn from.")
print("Why y is Answer:")
print("y contains the correct target value that the model tries to predict.")
print("\nImportant idea:")
print("X = Input")
print("y = Answer")
