import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create a dataset for correlation analysis.
data = {
    'Experience': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Age': [22, 24, 25, 27, 29, 32, 34, 36, 38, 40],
    'Salary': [28000, 32000, 36000, 40000, 45000, 50000, 56000, 62000, 68000, 75000],
    'Working Hours': [35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
    'Performance Score': [65, 70, 72, 75, 78, 80, 82, 85, 88, 90]
}

df = pd.DataFrame(data)

# Calculate correlation matrix.
corr_matrix = df.corr()
print('Correlation matrix:')
print(corr_matrix)

# Create a heatmap to visualize correlations.
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Heatmap')
plt.savefig('charts/correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

if __name__ == '__main__':
    print('correlation.py ran successfully and saved charts/correlation_heatmap.png')
