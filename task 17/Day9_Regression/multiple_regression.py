"""Multiple linear regression for a small house-price dataset."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(9)
X = rng.integers([700, 1, 1, 0, 0], [2600, 5, 4, 40, 3], size=(120, 5))
X = X.astype(float)
X[:, 0] = np.round(X[:, 0] / 10) * 10
y = 50_000 + X @ np.array([210.0, 18_000.0, 12_000.0, -1_500.0, 8_000.0]) + rng.normal(0, 25_000, len(X))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=9)
model = LinearRegression().fit(X_train, y_train)
predictions = model.predict(X_test)

print("Features: House_Area, Bedrooms, Bathrooms, Age, Parking")
print("Coefficients:", np.round(model.coef_, 2))
print("MAE:", round(mean_absolute_error(y_test, predictions), 2))
print("MSE:", round(mean_squared_error(y_test, predictions), 2))
print("RMSE:", round(np.sqrt(mean_squared_error(y_test, predictions)), 2))
print("R2:", round(r2_score(y_test, predictions), 3))