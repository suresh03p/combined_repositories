import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

salary = [
    25000, 28000, 30000, 32000,
    35000, 36000, 38000, 40000,
    42000, 45000, 48000, 50000,
    150000
]

df = pd.DataFrame({'Salary': salary})

# Histogram: shows the salary distribution and frequency by salary range.
plt.figure(figsize=(8, 5))
sns.histplot(df['Salary'], bins=6, kde=False, color='skyblue')
plt.title('Salary Distribution')
plt.xlabel('Salary (USD)')
plt.ylabel('Frequency')
plt.savefig('charts/distribution_salary_histogram.png', dpi=150, bbox_inches='tight')
plt.close()

# Box plot: identifies min, max, median, and outliers in salary data.
plt.figure(figsize=(6, 5))
sns.boxplot(x=df['Salary'], color='lightcoral')
plt.title('Salary Box Plot')
plt.xlabel('Salary (USD)')
plt.savefig('charts/distribution_salary_boxplot.png', dpi=150, bbox_inches='tight')
plt.close()

observations = '''
Observations:
- The salary distribution shows most values are between 25,000 and 50,000.
- The histogram frequency indicates a right-skewed distribution because one very high salary pulls the shape.
- The box plot highlights a median near 37,500.
- The top value 150,000 is a possible outlier compared to the rest of the salaries.
- The lower and upper whiskers show the spread of most salaries, while the outlier is far above the interquartile range.
'''

if __name__ == '__main__':
    print('distribution_analysis.py ran successfully and created histogram and box plot charts.')
    print(observations)
