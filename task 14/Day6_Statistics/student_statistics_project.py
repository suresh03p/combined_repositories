import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

# Generate dataset for 100 students
n = 100
students = pd.DataFrame({
    'Student_ID': [f'STU-{i:03d}' for i in range(1, n + 1)],
    'Age': np.random.randint(18, 26, size=n),
    'Math_Marks': np.random.randint(40, 100, size=n),
    'Science_Marks': np.random.randint(35, 98, size=n),
    'English_Marks': np.random.randint(45, 96, size=n),
    'Attendance': np.random.randint(50, 100, size=n),
})

# Add some relationships to make analysis meaningful
students['Math_Marks'] = np.clip(students['Math_Marks'] + students['Attendance'] // 10 - 5, 35, 100)
students['Science_Marks'] = np.clip(students['Science_Marks'] + students['Attendance'] // 12 - 3, 30, 100)
students['English_Marks'] = np.clip(students['English_Marks'] + students['Attendance'] // 15 - 4, 40, 100)

# Save dataset
students.to_csv('data/students.csv', index=False)

print("Student dataset created with 100 students.")
print(students.head())

# Part 1: Central Tendency
subject_columns = ['Math_Marks', 'Science_Marks', 'English_Marks']
print("\n--- Central Tendency ---")
for subject in subject_columns:
    values = students[subject]
    print(f"{subject}:")
    print(f"  Mean = {values.mean():.2f}")
    print(f"  Median = {values.median():.2f}")
    mode_value = values.mode().iloc[0] if not values.mode().empty else 'No mode'
    print(f"  Mode = {mode_value}")

# Part 2: Dispersion
print("\n--- Dispersion ---")
for subject in subject_columns:
    values = students[subject]
    print(f"{subject}:")
    print(f"  Range = {values.max() - values.min():.2f}")
    print(f"  Variance = {values.var():.2f}")
    print(f"  Standard Deviation = {values.std():.2f}")

# Part 3: Percentiles
print("\n--- Percentiles ---")
for subject in subject_columns:
    values = students[subject]
    print(f"{subject}:")
    print(f"  25th percentile = {np.percentile(values, 25):.2f}")
    print(f"  50th percentile = {np.percentile(values, 50):.2f}")
    print(f"  75th percentile = {np.percentile(values, 75):.2f}")

# Part 4: Outliers via IQR
print("\n--- Outliers ---")
for subject in subject_columns:
    q1 = np.percentile(students[subject], 25)
    q3 = np.percentile(students[subject], 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = students[students[subject] < lower][subject].tolist() + students[students[subject] > upper][subject].tolist()
    print(f"{subject}: lower={lower:.2f}, upper={upper:.2f}, outliers={outliers[:5]}")

# Part 5: Z-score for Math marks
print("\n--- Z-score Analysis ---")
math_mean = students['Math_Marks'].mean()
math_std = students['Math_Marks'].std()
students['Math_ZScore'] = (students['Math_Marks'] - math_mean) / math_std
print("Top performing students:")
print(students.nlargest(5, 'Math_ZScore')[['Student_ID', 'Math_Marks', 'Math_ZScore']])
print("Below-average students:")
print(students.nsmallest(5, 'Math_ZScore')[['Student_ID', 'Math_Marks', 'Math_ZScore']])

# Part 6: Correlation
print("\n--- Correlation ---")
for pair in [
    ('Attendance', 'Math_Marks'),
    ('Age', 'Math_Marks'),
    ('Math_Marks', 'Science_Marks'),
    ('Math_Marks', 'English_Marks')
]:
    corr = students[pair[0]].corr(students[pair[1]])
    print(f"{pair[0]} vs {pair[1]}: {corr:.4f}")

# Part 7: Visualization
plt.figure(figsize=(8, 6))
plt.hist(students['Math_Marks'], bins=15, edgecolor='black', alpha=0.7)
plt.title('Math Marks Distribution')
plt.xlabel('Marks')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('charts/marks_distribution.png')
plt.close()

plt.figure(figsize=(8, 6))
students.boxplot(column=['Math_Marks', 'Science_Marks', 'English_Marks'])
plt.title('Subject Marks Box Plot')
plt.ylabel('Marks')
plt.tight_layout()
plt.savefig('charts/marks_boxplot.png')
plt.close()

plt.figure(figsize=(8, 6))
plt.scatter(students['Attendance'], students['Math_Marks'], alpha=0.7)
plt.title('Attendance vs Marks')
plt.xlabel('Attendance')
plt.ylabel('Math Marks')
plt.tight_layout()
plt.savefig('charts/attendance_vs_marks.png')
plt.close()

correlation_matrix = students[['Math_Marks', 'Science_Marks', 'English_Marks', 'Attendance', 'Age']].corr()
plt.figure(figsize=(8, 6))
plt.imshow(correlation_matrix, cmap='coolwarm')
plt.colorbar(label='Correlation')
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('charts/correlation_heatmap.png')
plt.close()

print("\nPlots saved to charts/marks_distribution.png, charts/marks_boxplot.png, charts/attendance_vs_marks.png, and charts/correlation_heatmap.png")
print("Project complete.")
