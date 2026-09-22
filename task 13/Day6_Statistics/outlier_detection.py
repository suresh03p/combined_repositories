import numpy as np

salary = [25000, 27000, 28000, 30000, 32000, 34000, 35000, 37000, 40000, 42000, 45000, 500000]

q1 = np.percentile(salary, 25)
q3 = np.percentile(salary, 75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = [x for x in salary if x < lower_bound or x > upper_bound]

print("Salary data:", salary)
print("Q1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Lower Boundary:", lower_bound)
print("Upper Boundary:", upper_bound)
print("Outliers:", outliers)

# Basic explanation
print("\nThe value 500000 is far above the upper boundary, so it is an outlier.")
print("This happens because outliers can heavily distort metrics like mean and standard deviation.")
