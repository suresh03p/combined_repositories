"""Lasso can shrink weak coefficients to exactly zero."""

import numpy as np
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(5)
X = rng.normal(size=(180, 8))
y = 4 * X[:, 0] - 3 * X[:, 1] + rng.normal(0, 0.7, len(X))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

for alpha in [0.01, 0.1, 1, 10]:
    model = make_pipeline(StandardScaler(), Lasso(alpha=alpha, max_iter=10_000)).fit(X_train, y_train)
    print(f"alpha={alpha:<4} coefficients={np.round(model[-1].coef_, 3)}")