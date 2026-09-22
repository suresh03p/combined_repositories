# Student Statistical Report

## Overview
This report analyzes a synthetic dataset of 100 students with age, marks, attendance, and performance variables. The goal is to summarize student performance and identify relationships and unusual values.

### Question 1: What is the average student performance?
The average performance is measured using subject-wise mean marks. Based on the generated dataset, the average marks are around the mid-to-high range for all subjects because the marks were generated with a generally healthy distribution.

### Question 2: Which subject has the highest average?
The subject with the highest average depends on the generated values. In this dataset, Math marks are usually strong and may have the highest average because they are influenced by attendance.

### Question 3: Which subject has the highest variation?
The subject with the highest variation is usually the one with the largest standard deviation. This indicates wider spread of scores from the mean.

### Question 4: Are there any outliers?
Using the IQR method, unusually low or high marks can be detected. These are values beyond the lower or upper boundary defined by Q1 and Q3. If present, they should be checked for data quality or exceptional performance.

### Question 5: Does attendance appear related to marks?
Attendance is expected to be positively related to marks, because students with stronger attendance often perform better. The correlation between attendance and marks helps confirm this relationship.

### Question 6: Which two subjects have the strongest correlation?
The strongest correlation is generally between Math and Science marks, because both are analytical subjects and often rise together in well-performing students. This relationship can be confirmed using the correlation matrix.

### Question 7: Which students are significantly above average?
Students with a high positive Z-score in Math marks are significantly above the class average. These students stand out from the rest because their marks are far above the mean.

### Question 8: Which students are significantly below average?
Students with a large negative Z-score in Math marks are significantly below average. These students may need extra support or attention.

### Question 9: What data should potentially be investigated before ML?
Before building machine learning models, we should review:
- missing values
- outliers
- inconsistent ages or attendance values
- class imbalance or skewed marks
- duplicate records
- relationship between variables and target variables

This helps ensure the model learns from clean and meaningful data.
