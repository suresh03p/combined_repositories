# Day 8: Why Preprocessing Is Required

## Starting example

| Age | Salary | City |
| ---: | ---: | --- |
| 25 | 30000 | Hyderabad |
| 30 | 50000 | Chennai |
| 28 | 45000 | Hyderabad |
| 35 | 80000 | Bangalore |

`Age` and `Salary` are numerical features, but they have different scales. `City` is categorical text. A model needs numeric input, so categories must be represented numerically without inventing a relationship that does not exist. Preprocessing prepares raw features for reliable model training.

## Core definitions

1. **Data preprocessing**: Cleaning and transforming raw data into a form an algorithm can use.
2. **Dataset**: A collection of observations, usually represented as rows and columns.
3. **Observation**: One row describing an item, person, event, or transaction.
4. **Feature**: An input column used by a model to make a prediction.
5. **Target**: The output column the model is trained to predict.
6. **Numerical data**: Quantities represented by numbers, such as age, experience, or salary.
7. **Categorical data**: Values that represent groups or labels, such as city or department.
8. **Nominal category**: A category with no natural order, such as Bangalore or Chennai.
9. **Ordinal category**: A category with meaningful order, such as Low, Medium, High.
10. **Missing value**: A value that was not recorded or is unavailable.
11. **Imputation**: Replacing missing values with a reasonable estimate.
12. **Mean**: The arithmetic average; useful for roughly symmetric numerical data without strong outliers.
13. **Median**: The middle value after sorting; more robust than the mean when outliers exist.
14. **Mode**: The most frequent value; useful for categorical columns.
15. **Encoding**: Converting categorical values into numeric representations.
16. **Label encoding**: Mapping categories to integer labels; appropriate for genuinely ordered categories.
17. **One-hot encoding**: Creating one binary column for each category.
18. **Scaling**: Changing numerical features to comparable ranges or distributions.
19. **Standardization**: Centering a feature around mean 0 with standard deviation 1.
20. **Normalization**: Often used to mean rescaling values to a fixed range, commonly 0 to 1.
21. **Feature engineering**: Creating useful input features from existing data or domain knowledge.
22. **Data leakage**: Allowing information unavailable at prediction time to influence training.
23. **Train/test split**: Separating data used for learning from data reserved for an honest evaluation.
24. **Pipeline**: An ordered, reusable sequence of transformations and a model.
25. **ColumnTransformer**: A scikit-learn utility that applies different transformations to different columns.
26. **Cross-validation**: Repeatedly training and validating on different folds to estimate generalization.

## Practical rules

- Fit imputers, encoders, and scalers on training data only; use them to transform test and future data.
- Use label encoding for ordered values only when the integer order is meaningful.
- Use one-hot encoding for nominal values such as cities. It creates multiple columns because each column answers a yes/no question: “is this row in category X?”
- Mean is sensitive to outliers. Median is safer for skewed measurements such as salary. Most frequent is useful for categorical or discrete values.
- A pipeline keeps training and prediction transformations identical and makes leakage harder to introduce.