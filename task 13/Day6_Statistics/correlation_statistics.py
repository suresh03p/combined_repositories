import numpy as np
import pandas as pd

experience = [1, 2, 3, 4, 5, 6]
salary = [25000, 28000, 32000, 37000, 42000, 50000]

df = pd.DataFrame({
    'experience': experience,
    'salary': salary
})

print("Covariance:", np.cov(experience, salary)[0][1])
print("Correlation:", df['experience'].corr(df['salary']))
print("\nInterpretation: Salary rises as experience increases, showing a strong positive relationship.")

# Test with 5 datasets
print("\n--- Testing 5 Datasets ---")
examples = [
    ([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]),
    ([1, 2, 3, 4, 5], [10, 8, 6, 4, 2]),
    ([1, 2, 3, 4, 5], [5, 3, 4, 6, 1]),
    ([1, 2, 3, 4, 5], [7, 7, 7, 7, 7]),
    ([1, 2, 3, 4, 5], [1, 4, 2, 5, 3])
]

for i, (x, y) in enumerate(examples, 1):
    corr = pd.DataFrame({'x': x, 'y': y}).corr().iloc[0, 1]
    print(f"Dataset {i}: correlation = {corr:.2f}")

print("\nCorrelation values:")
print("+1 -> Strong positive relationship")
print("0 -> No linear relationship")
print("-1 -> Strong negative relationship")
