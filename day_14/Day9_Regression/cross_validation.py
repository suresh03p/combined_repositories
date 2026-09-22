"""Five-fold cross-validation avoids trusting one lucky split."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(7)
X = rng.normal(size=(100, 3))
y = 5 + 2 * X[:, 0] - X[:, 1] + rng.normal(0, 0.8, len(X))
model = LinearRegression()
scores = cross_val_score(model, X, y, cv=5, scoring="r2")
for number, score in enumerate(scores, start=1):
    print(f"Fold {number}: R2={score:.3f}")
print(f"Average R2: {scores.mean():.3f}")
print(f"Standard deviation: {scores.std():.3f}")