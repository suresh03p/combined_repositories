# Day 4 Theory: Understanding Data Cleaning

## What is Data Cleaning?
1. Data cleaning is the process of detecting and correcting inaccurate, incomplete, or inconsistent records in a dataset.
2. It removes or repairs errors and anomalies so the data becomes suitable for analysis or machine learning.
3. Cleaning data improves reliability, accuracy, and the quality of insights derived from the dataset.

## What are Missing Values?
4. Missing values occur when no data value is stored for a variable in an observation.
5. Common causes include skipped fields, transfer errors, and data collection problems.
6. Missing values can bias results, reduce training set size, and break analysis logic.

## What are Duplicate Records?
7. Duplicate records are repeated observations that represent the same real-world entity multiple times.
8. They often arise from repeated data entry, merged datasets, or failed deduplication.
9. Duplicates distort counts, averages, and model training if not removed.

## What are Incorrect Data Types?
10. Incorrect data types happen when numeric, date, or categorical values are stored as text or wrong formats.
11. Wrong data types make aggregation, mathematical operations, and date comparisons invalid.
12. Converting data types properly ensures computations and plots work correctly.

## What are Outliers?
13. Outliers are extreme values that differ significantly from the other observations.
14. They can be caused by data entry errors, measurement problems, or rare but real cases.
15. Outliers may skew averages, inflate variance, and affect model performance.

## Why Data Cleaning is Important in AI/ML?
16. Machine learning models need clean inputs to generalize reliably and avoid learning noise.
17. Poor-quality data can cause overfitting, biased predictions, and incorrect business decisions.
18. Data cleaning reduces false positives, missing feature problems, and training instability.
19. Clean data enables accurate feature engineering, scaling, and model validation.
20. It also improves interpretability and trust in model outcomes.

## Additional Important Points
21. Data cleaning is often the most time-consuming part of any data science workflow.
22. A good cleaning process includes inspection, diagnosis, transformation, and validation.
23. Consistent formatting helps with reproducibility and data sharing across tools.
24. Documenting the cleaning steps is essential for transparency and collaboration.
25. A strong cleaning pipeline makes it easier to maintain data quality as datasets grow.

## Interview Questions with Answers

1. **What is data cleaning?**
   - Data cleaning is the process of correcting or removing flawed, incomplete, or inaccurate records to make data usable for analysis.

2. **Why are missing values problematic?**
   - Missing values reduce the effective sample size and can bias statistical estimates or machine learning models.

3. **How can duplicate records affect analysis?**
   - Duplicates inflate counts and averages and can make models overfit to repeated observations.

4. **What should you do when a numeric column is stored as text?**
   - Convert it using type conversion functions like `astype`, `to_numeric`, or `to_datetime` and handle errors appropriately.

5. **When is it safe to use `dropna()`?**
   - When only a small fraction of rows contain missing values and those rows do not hold critical information.

6. **What is the difference between mean and median imputation?**
   - Mean replaces missing values with the average, while median uses the middle value and is less sensitive to outliers.

7. **What is forward fill?**
   - Forward fill propagates the last valid observation forward to fill subsequent missing values, useful in time series.

8. **What types of problems can incorrect dates cause?**
   - They can prevent sorting, filtering by date ranges, and calculating time-based features.

9. **What is an outlier?**
   - An outlier is a data point that is significantly different from the rest of the dataset.

10. **How can you find duplicate rows in pandas?**
    - Use `df.duplicated()` to locate duplicates and `df.drop_duplicates()` to remove them.

11. **Why is data cleaning important for machine learning?**
    - Because models trained on unclean data can learn noise, make biased predictions, and perform poorly on new data.

12. **How do you handle a categorical column with missing values?**
    - You can fill with the mode, a constant placeholder like "Unknown", or use a dedicated categorical imputation method.

13. **What does `df.info()` tell you?**
    - It shows row count, column names, non-null counts, and data types for each column.

14. **What is the benefit of standardizing text columns?**
    - Standardization reduces variation from uppercase/lowercase differences and makes grouping and filtering consistent.

15. **How do you detect wrong data types in pandas?**
    - Use `df.dtypes`, `df.info()`, and inspect sample values to find columns that should be numeric or datetime.

## Real-World Examples of Dirty Data

1. A customer database with blank `email` fields and inconsistent phone number formats.
2. A retail sales file that duplicates the same invoice multiple times after system retries.
3. A survey dataset where numeric ratings are stored as text and missing answers are blank strings.
4. A product catalog where prices are entered as "50k" or "fifty thousand" instead of numeric values.
5. A time-series log file with missing timestamps and event records out of order.
