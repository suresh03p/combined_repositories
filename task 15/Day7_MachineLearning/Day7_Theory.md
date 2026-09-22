# Day 7: Machine Learning from Zero

## What is Machine Learning?

Machine Learning is a way to teach computers to learn patterns from examples instead of being told every rule directly. We give the computer data, it studies the pattern, and then it makes predictions on new data.

Example:

```
House Size → House Price

1000 sq.ft → ₹30 Lakhs
1500 sq.ft → ₹45 Lakhs
2000 sq.ft → ₹60 Lakhs
```

The computer studies these examples. It notices that as house size increases, price increases. Then if we ask:

```
2500 sq.ft → ?
```

it estimates a likely price using the pattern it learned.

---

## Important Terms in Simple English

1. Machine Learning: A method where computers learn from data to make predictions or find patterns.
2. Dataset: A collection of examples or records used for learning.
3. Feature: A property or input that helps the model make a decision, like house size or hours studied.
4. Target: The value we want to predict, such as house price or exam score.
5. Label: The correct answer attached to an example in supervised learning.
6. Training: The process of showing examples to a model so it can learn patterns.
7. Testing: Checking how well the model performs on data it has not seen before.
8. Model: A learned system that can make predictions.
9. Prediction: The output the model gives for a new input.
10. Algorithm: A step-by-step method or rule used to train a model.
11. Supervised Learning: Learning from examples where the correct answer is known.
12. Unsupervised Learning: Finding patterns or groups in data without known answers.
13. Regression: Predicting a continuous number, like price or temperature.
14. Classification: Predicting a category, like spam or not spam.
15. Clustering: Grouping similar data points together without labels.
16. Feature Engineering: Creating or changing features so the model can learn better.
17. Overfitting: When a model memorizes the training data too much and performs badly on new data.
18. Underfitting: When a model is too simple and cannot learn the pattern well.
19. Accuracy: A measure of how often a model predicts correctly.
20. Evaluation: Measuring how good the model is using test data.
21. Coefficient: The number that tells how much one feature affects the prediction.
22. Intercept: The starting value of the prediction when all inputs are zero.
23. Linear Regression: A machine learning method that finds a straight-line relationship between features and target.
24. Train/Test Split: Dividing the dataset into training data and testing data.
25. Input: The data sent into a model for processing.
26. Output: The result produced by the model.
27. Example: One row of data that shows a feature and target relationship.
28. Decision Boundary: A line or rule used to separate classes in classification.
29. Bias: The error caused by simplifying assumptions in a model.
30. Variance: The error caused by a model being too sensitive to small changes in training data.

---

## Simple Example of Learning

Suppose we show the computer:

```
Hours studied → Exam score
2 → 40
3 → 45
4 → 50
5 → 55
6 → 65
```

The model learns that more study time usually means a higher score. Then it can guess the score for a new student who studied 8 hours. This is the basic idea of machine learning.

---

## Why This Matters

Machine learning is useful because it helps us solve problems automatically. It can help predict prices, detect fraud, recommend movies, recognize faces, and understand spoken language. The main goal is to learn from data and use that knowledge to make useful predictions.

---

## Final Thought

Machine learning is not magic. It is simply a way for computers to look at examples, detect patterns, and use those patterns to make decisions for new situations. The more useful and clean the data, the better the learning can become.
