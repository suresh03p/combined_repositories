import numpy as np

salary = [25000, 28000, 30000, 32000, 35000, 38000, 40000, 45000, 50000, 60000]

q1 = np.percentile(salary, 25)
q2 = np.percentile(salary, 50)
q3 = np.percentile(salary, 75)

print("Salary data:", salary)
print("25th percentile (Q1):", q1)
print("50th percentile (Q2):", q2)
print("75th percentile (Q3):", q3)
print("IQR = Q3 - Q1 =", q3 - q1)
print("Q1 = 25th percentile")
print("Q2 = 50th percentile")
print("Q3 = 75th percentile")
