# Model Comparison Report

This experiment uses 500 generated house records. Prices are synthetic, so the
results demonstrate a workflow rather than a real estate valuation.

## 1. Which model performed best?
**Linear Regression** had the highest test R2 (0.951). I judged "best"
using the full metric table instead of looking at one number in isolation.

## 2. Which model had the lowest RMSE?
**Linear Regression**, with an RMSE of 34481.59 price units.

## 3. Which model had the highest R2?
**Linear Regression**, with an R2 of 0.951.

## 4. Did regularization improve the model?
Ridge, Lasso, and Elastic Net were useful comparison points. Regularization can
make a model less sensitive to noisy or correlated inputs, but on this clean,
synthetic dataset it is only an improvement if its test metrics beat the plain
linear model. The table below is the evidence for that decision.

## 5. Did polynomial regression overfit?
The degree-2 polynomial model did not automatically win. Extra terms can fit
small quirks in training data, so its test R2 and RMSE must be checked rather
than assuming that a more complex model is better.

## 6. What happened when polynomial degree increased?
Higher degrees add flexibility. Training error usually falls, but testing error
can rise after the useful pattern has been captured. This is the central sign of
overfitting.

## 7. Which model would you choose for production?
I would start with **Linear Regression**, subject to monitoring and validation on real,
future listings.

## 8. Why did you choose it?
It explained the most test variation while remaining a measurable, repeatable
choice. I would also check that its errors are acceptable in actual price units.

## 9. What additional data could improve the prediction?
Neighborhood quality, lot size, floor level, renovation condition, school access,
property type, sale date, and nearby comparable sale prices could add signal.

## 10. What are the limitations?
The data is generated, the noise pattern is artificial, and Location is represented
only by four broad labels. The model also assumes that relationships learned from
this sample remain valid in new markets and time periods.

## Test-set metrics

| Model | MAE | MSE | RMSE | R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 28761.05 | 1188979789.83 | 34481.59 | 0.951 |
| Ridge | 28856.07 | 1196922614.90 | 34596.57 | 0.951 |
| Lasso | 29760.75 | 1266879917.43 | 35593.26 | 0.948 |
| Polynomial Regression | 30071.66 | 1343708714.39 | 36656.63 | 0.944 |
| Elastic Net | 131269.12 | 24115098393.38 | 155290.37 | 0.003 |

## Five-fold cross-validation of the top two
- Linear Regression: mean R2 = 0.948, standard deviation = 0.013
- Ridge: mean R2 = 0.948, standard deviation = 0.013
