import pandas as pd
from sklearn.linear_model import LinearRegression

# Data
hours = [2, 3, 4, 5, 6, 7, 8, 9, 10]
scores = [40, 45, 50, 55, 65, 70, 80, 85, 95]

X = pd.DataFrame({"Hours_Studied": hours})
y = pd.Series(scores)

model = LinearRegression()
model.fit(X, y)

print("Equation used by Linear Regression:")
print("y = mx + b")
print("where:")
print("y = prediction")
print("m = slope")
print("x = input")
print("b = intercept")
print("\nLearned model parameters:")
print("Coefficient:", model.coef_)
print("Intercept:", model.intercept_)

print("\nSimple explanation:")
print("- The coefficient shows how much the exam score changes when study time changes.")
print("- The intercept is the starting score when study hours are zero.")
print("- If the slope is positive, more study time generally leads to higher predicted marks.")
