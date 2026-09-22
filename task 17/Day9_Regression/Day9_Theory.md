# Day 9: Understand Regression From Zero

## A tiny example

| Hours Studied | Exam Score |
|---:|---:|
| 2 | 40 |
| 3 | 45 |
| 4 | 52 |
| 5 | 60 |
| 6 | 68 |
| 7 | 75 |
| 8 | 82 |

A machine-learning model learns a relationship from **input to output**. Here,
Hours Studied is the feature and Exam Score is the target. Because the target is
a continuous number, this is a regression problem.

## Core vocabulary

1. **Regression:** A supervised-learning method for predicting a numerical value.
2. **Independent variable:** An input that may help explain or predict an output.
3. **Dependent variable:** The output whose value depends on the inputs.
4. **Feature:** The name used for an input column given to a model.
5. **Target:** The correct output column the model is trained to predict.
6. **Prediction:** The value estimated by a trained model for new input.
7. **Coefficient:** A learned number that says how strongly a feature changes the prediction.
8. **Intercept:** The model's starting prediction when all numeric inputs are zero.
9. **Residual:** The remaining difference after the model makes a prediction.
10. **Error:** Another common name for a residual; here, `Actual - Predicted`.
11. **Continuous variable:** A numerical quantity that can take many values, such as price.
12. **Categorical variable:** A label from a set of groups, such as North or South.
13. **Observation:** One row representing one example, person, house, or event.
14. **Dataset:** A collection of observations arranged in rows and columns.
15. **Training data:** The examples used to learn coefficients and other model parameters.
16. **Testing data:** Held-out examples used to estimate performance on unseen data.
17. **Train/test split:** The act of separating data for learning from data for checking.
18. **Linear relationship:** A relationship that can be approximated by a straight line.
19. **Slope:** The amount the prediction changes for a one-unit increase in an input.
20. **Model:** A learned mathematical rule that maps features to predictions.
21. **Generalization:** Performing well on new data, not just memorized training rows.
22. **Metric:** A score used to summarize prediction quality.
23. **MAE:** Mean Absolute Error; the average size of mistakes without signs cancelling.
24. **MSE:** Mean Squared Error; the average squared mistake, which emphasizes large errors.
25. **RMSE:** The square root of MSE, putting the result back in target units.
26. **R²:** The fraction of target variation explained compared with a simple mean baseline.

## Simple linear regression

The basic equation is:

$$y = mx + b$$

- `y` is the predicted value.
- `m` is the coefficient or slope.
- `x` is the input feature.
- `b` is the intercept.

A positive coefficient means the prediction tends to rise as the feature rises. A
negative coefficient means the prediction tends to fall. A coefficient close to
zero means that feature has little linear influence, after the other features are
considered.

## Why residuals are not all zero

Real outcomes depend on more information than the columns in a small dataset.
People study differently, houses differ in condition, and measurements contain
noise. A straight line is also only an approximation. A good model tries to make
the residuals small and patternless; it does not promise perfect predictions for
every row.

## The learning path

Run the Python files in order. They move from one feature, to many features, to
curves, regularization, validation, and finally a complete house-price workflow.