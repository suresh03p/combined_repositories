# Train / Validation / Test Split

The split of a dataset is one of the most important quality controls in model development.

## Training dataset
The training set is used to teach the model. The model learns patterns, label boundaries, and task behavior from these examples.

## Validation dataset
The validation set is used during training to monitor progress and make decisions about hyperparameters and stopping points. It helps the developer avoid blindly over-training the model.

## Test dataset
The test set is used only for the final evaluation. It should not be used repeatedly to tune the model because doing so leaks information into the evaluation process and makes results less trustworthy.

## Why this matters
If the same data is used for both training and evaluation, the model may appear to perform well only because it is memorizing examples rather than learning general rules.

## Recommended flow
```text
Training Dataset
       ↓
Model learns

Validation Dataset
       ↓
Training decisions

Test Dataset
       ↓
Final evaluation
```

## Rule of thumb
Use the training set for learning, the validation set for tuning, and the test set for the final truth check.
