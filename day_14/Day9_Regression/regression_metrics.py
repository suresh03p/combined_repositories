"""Compare the four common regression metrics."""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

actual = np.array([100, 120, 140, 160, 180], dtype=float)
predicted = np.array([102, 115, 150, 156, 200], dtype=float)

mae = mean_absolute_error(actual, predicted)
mse = mean_squared_error(actual, predicted)
try:
    from sklearn.metrics import root_mean_squared_error
    rmse = root_mean_squared_error(actual, predicted)
except ImportError:
    rmse = np.sqrt(mse)

print(f"MAE: {mae:.2f} (average absolute mistake in target units)")
print(f"MSE: {mse:.2f} (squared mistakes; large errors count more)")
print(f"RMSE: {rmse:.2f} (typical error, in target units)")
print(f"R2: {r2_score(actual, predicted):.3f} (variation explained by the model)")