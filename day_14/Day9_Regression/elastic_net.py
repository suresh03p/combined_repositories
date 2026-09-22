"""Elastic Net combines L1 (Lasso) and L2 (Ridge) regularization."""

import numpy as np
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(6)
X = rng.normal(size=(200, 8))
y = 4 * X[:, 0] - 3 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0, 0.8, len(X))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=6)
models = {
    "Linear Regression": LinearRegression(),
    "Ridge": Ridge(alpha=1),
    "Lasso": Lasso(alpha=0.1, max_iter=10_000),
    "Elastic Net": ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=10_000),
}
for name, estimator in models.items():
    model = make_pipeline(StandardScaler(), estimator).fit(X_train, y_train)
    print(f"{name:<18} test_R2={r2_score(y_test, model.predict(X_test)):.3f}")