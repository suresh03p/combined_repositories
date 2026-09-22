"""Ridge regression: compare regularization strengths."""

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(4)
X = rng.normal(size=(160, 6))
y = 3 * X[:, 0] - 2 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0, 0.8, len(X))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=4)

for alpha in [0.01, 0.1, 1, 10, 100]:
    model = make_pipeline(StandardScaler(), Ridge(alpha=alpha)).fit(X_train, y_train)
    print(f"alpha={alpha:<5} train_R2={r2_score(y_train, model.predict(X_train)):.3f} test_R2={r2_score(y_test, model.predict(X_test)):.3f}")