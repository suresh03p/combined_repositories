# Underfitting and Overfitting

## Three situations

### Underfitting

```text
Model too simple
       ↓
Does not learn enough
```

Training and testing scores are both poor. A straight line on a strongly curved
relationship is a common example.

### Good fit

```text
Learns important patterns
       ↓
Generalizes to new data
```

Training and testing scores are both reasonably strong and fairly close together.

### Overfitting

```text
Model learns training data too closely
       ↓
Performs poorly on new data
```

Training R² becomes very high while testing R² stays much lower or becomes
unstable. The model is learning noise and quirks instead of reusable patterns.

## Practical experiment

`polynomial_regression.py` demonstrates degrees 1, 2, 3, and 5. Fit degrees 1,
2, 3, 5, 10, and 15 on the same train/test split and record this table:

| Degree | Training R² | Testing R² |
|---:|---:|---:|
| 1 | 0.056 | 0.191 |
| 2 | 0.979 | 0.951 |
| 3 | 0.980 | 0.952 |
| 5 | 0.981 | 0.946 |
| 10 | 0.983 | 0.952 |
| 15 | 0.933 | 0.893 |

In this run, the useful curve is captured by degree 2 or 3. Small overfitting
starts around degree 5: training R² rises slightly while testing R² falls. Degree
15 is a clearer warning because its testing score drops substantially. The exact
degree depends on the data, noise, and split. More polynomial terms are not
automatically better.

## Ways to respond

Use more representative data, reduce model complexity, use cross-validation, or
add regularization. Ridge discourages large coefficients. Lasso can also shrink
some coefficients to zero, making it useful for feature selection.