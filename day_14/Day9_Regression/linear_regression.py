"""Simple linear regression: hours studied versus exam score."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = np.array([[2], [3], [4], [5], [6], [7], [8]], dtype=float)
y = np.array([40, 45, 52, 60, 68, 75, 82], dtype=float)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("Test hours:", X_test.ravel())
print("Predictions:", np.round(predictions, 2))
print("Coefficient (slope):", model.coef_)
print("Intercept:", model.intercept_)
print("A positive coefficient means more study hours are associated with a higher score.")
print("A negative coefficient means more study hours are associated with a lower score.")
print("A coefficient near zero means the feature has little linear effect on the prediction.")