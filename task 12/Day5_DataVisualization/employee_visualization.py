import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample cleaned employee dataset for visualization.
data = {
    'Department': ['Sales', 'HR', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'Finance', 'Finance', 'IT',
                   'Sales', 'HR', 'Finance', 'IT', 'HR', 'Sales', 'Finance', 'IT', 'Sales', 'HR'],
    'Salary': [42000, 35000, 55000, 48000, 36000, 62000, 52000, 47000, 51000, 60000,
               45000, 39000, 53000, 58000, 38000, 49000, 50000, 62000, 54000, 41000],
    'Age': [28, 33, 29, 31, 35, 27, 30, 38, 42, 26, 34, 32, 41, 25, 37, 30, 39, 28, 33, 36],
    'Experience': [3, 6, 4, 5, 7, 2, 5, 10, 12, 3, 6, 5, 11, 2, 8, 5, 9, 4, 7, 6],
    'Performance Score': [72, 68, 78, 75, 70, 80, 73, 82, 85, 79, 74, 69, 83, 81, 71, 76, 84, 79, 77, 70]
}

df = pd.DataFrame(data)

# 1. Employees by Department - Bar chart
plt.figure(figsize=(8, 5))
dep_count = df['Department'].value_counts()
sns.barplot(x=dep_count.index, y=dep_count.values, palette='muted')
plt.title('Employees by Department')
plt.xlabel('Department')
plt.ylabel('Count')
plt.savefig('charts/employees_by_department.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. Salary Distribution - Histogram
plt.figure(figsize=(8, 5))
sns.histplot(df['Salary'], bins=6, color='skyblue')
plt.title('Salary Distribution')
plt.xlabel('Salary (USD)')
plt.ylabel('Frequency')
plt.savefig('charts/salary_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 3. Salary by Department - Box plot
plt.figure(figsize=(8, 5))
sns.boxplot(x='Department', y='Salary', data=df, palette='pastel')
plt.title('Salary by Department')
plt.xlabel('Department')
plt.ylabel('Salary (USD)')
plt.savefig('charts/salary_by_department.png', dpi=150, bbox_inches='tight')
plt.close()

# 4. Age Distribution - Histogram
plt.figure(figsize=(8, 5))
sns.histplot(df['Age'], bins=6, color='lightgreen')
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.savefig('charts/age_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 5. Experience Distribution - Histogram
plt.figure(figsize=(8, 5))
sns.histplot(df['Experience'], bins=6, color='orange')
plt.title('Experience Distribution')
plt.xlabel('Experience (Years)')
plt.ylabel('Frequency')
plt.savefig('charts/experience_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 6. Age vs Salary - Scatter plot
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Age', y='Salary', hue='Department', data=df, s=100)
plt.title('Age vs Salary')
plt.xlabel('Age')
plt.ylabel('Salary (USD)')
plt.savefig('charts/age_vs_salary.png', dpi=150, bbox_inches='tight')
plt.close()

# 7. Experience vs Salary - Scatter plot
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Experience', y='Salary', hue='Department', data=df, s=100)
plt.title('Experience vs Salary')
plt.xlabel('Experience (Years)')
plt.ylabel('Salary (USD)')
plt.savefig('charts/experience_vs_salary.png', dpi=150, bbox_inches='tight')
plt.close()

# 8. Employee Count by Department - Count plot
plt.figure(figsize=(8, 5))
sns.countplot(x='Department', data=df, palette='bright')
plt.title('Employee Count by Department')
plt.xlabel('Department')
plt.ylabel('Count')
plt.savefig('charts/employee_count_by_department.png', dpi=150, bbox_inches='tight')
plt.close()

# 9. Salary Statistics - Bar chart
salary_stats = df.groupby('Department')['Salary'].mean().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(x='Department', y='Salary', data=salary_stats, palette='cool')
plt.title('Average Salary by Department')
plt.xlabel('Department')
plt.ylabel('Average Salary (USD)')
plt.savefig('charts/salary_statistics.png', dpi=150, bbox_inches='tight')
plt.close()

# 10. Correlation Heatmap
corr = df[['Experience', 'Age', 'Salary', 'Performance Score']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='viridis', vmin=-1, vmax=1)
plt.title('Employee Feature Correlation Heatmap')
plt.savefig('charts/employee_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

if __name__ == '__main__':
    print('employee_visualization.py ran successfully and saved 10 charts in charts/')
