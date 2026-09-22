import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Dataset
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

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("R² Score:", r2)

print("\nMeaning:")
print("MAE tells us the average distance between actual and predicted values.")
print("MSE measures the squared average error and penalizes larger mistakes more.")
print("R² shows how much of the variation in the target is explained by the model.")
