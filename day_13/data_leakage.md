# Data Leakage

## The problem

This is the wrong order:

```text
Entire dataset -> fit scaler -> train/test split
```

The scaler's mean and standard deviation include test rows. The model evaluation is then optimistic because information from the supposed unseen data influenced training.

The correct order is:

```text
Dataset -> train/test split -> fit preprocessing on training data
        -> transform training data and test data -> train model
```

The test set may be transformed using statistics learned from training, but those statistics must never be learned from the test set.

## Five examples

1. Scaling or imputing the complete dataset before splitting.
2. Selecting features using correlations calculated with both train and test rows.
3. Oversampling the complete dataset before splitting, allowing duplicate synthetic information into test data.
4. Using a future salary, outcome, or status column that would not exist when a prediction is made.
5. Randomly splitting repeated records from the same employee, patient, or customer into both sets.

`Pipeline` and `ColumnTransformer` help enforce the correct fit/transform boundary.