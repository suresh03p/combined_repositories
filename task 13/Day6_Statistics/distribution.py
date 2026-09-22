import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Approximate normal distribution: student heights
heights = np.random.normal(loc=165, scale=8, size=200)
# Right-skewed data: employee salaries
salaries = np.random.lognormal(mean=11.0, sigma=0.5, size=200)

print("Normal-like data sample:", heights[:10])
print("Right-skewed data sample:", salaries[:10])

# Plot histograms and KDE
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(heights, bins=20, edgecolor='black', alpha=0.7)
plt.title('Student Heights - Approximate Normal Distribution')
plt.xlabel('Height')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(salaries, bins=20, edgecolor='black', alpha=0.7)
plt.title('Employee Salaries - Right-Skewed Distribution')
plt.xlabel('Salary')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('charts/marks_distribution.png')
plt.close()

print("\nDistribution plots saved to charts/marks_distribution.png")
print("Observation: heights are more evenly centered around the mean, while salaries are skewed to the right because a few high salaries stretch the distribution.")
