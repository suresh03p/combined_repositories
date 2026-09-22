import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create a simple employee dataset.
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Sales': [12000, 15000, 18000, 14000, 22000],
    'Customers': [100, 120, 140, 110, 160],
    'Profit': [4000, 5200, 6200, 5000, 7800]
}
df = pd.DataFrame(data)

# Line plot: shows trend over time.
plt.figure(figsize=(8, 5))
sns.lineplot(x='Month', y='Sales', data=df, marker='o')
plt.title('Seaborn Line Plot: Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Sales (USD)')
plt.savefig('charts/seaborn_lineplot.png', dpi=150, bbox_inches='tight')
plt.close()

# Bar plot: compares amounts by category.
plt.figure(figsize=(8, 5))
sns.barplot(x='Month', y='Customers', data=df, palette='pastel')
plt.title('Seaborn Bar Plot: Monthly Customers')
plt.xlabel('Month')
plt.ylabel('Number of Customers')
plt.savefig('charts/seaborn_barplot.png', dpi=150, bbox_inches='tight')
plt.close()

# Scatter plot: shows relationship between sales and profit.
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Sales', y='Profit', data=df, s=100)
plt.title('Seaborn Scatter Plot: Sales vs Profit')
plt.xlabel('Sales (USD)')
plt.ylabel('Profit (USD)')
plt.savefig('charts/seaborn_scatterplot.png', dpi=150, bbox_inches='tight')
plt.close()

# Histogram: shows sales distribution.
plt.figure(figsize=(8, 5))
sns.histplot(df['Sales'], kde=False, bins=5, color='teal')
plt.title('Seaborn Histogram: Sales Distribution')
plt.xlabel('Sales (USD)')
plt.ylabel('Frequency')
plt.savefig('charts/seaborn_histplot.png', dpi=150, bbox_inches='tight')
plt.close()

# Box plot: shows profit distribution and outliers.
plt.figure(figsize=(6, 5))
sns.boxplot(x=df['Profit'], color='lightgreen')
plt.title('Seaborn Box Plot: Profit Distribution')
plt.xlabel('Profit (USD)')
plt.savefig('charts/seaborn_boxplot.png', dpi=150, bbox_inches='tight')
plt.close()

# Count plot: shows count by month (useful for categorical counts).
plt.figure(figsize=(8, 5))
sns.countplot(x='Month', data=df, palette='muted')
plt.title('Seaborn Count Plot: Month Frequency')
plt.xlabel('Month')
plt.ylabel('Count')
plt.savefig('charts/seaborn_countplot.png', dpi=150, bbox_inches='tight')
plt.close()

if __name__ == '__main__':
    print('seaborn_basics.py ran successfully and saved seaborn charts in charts/')
