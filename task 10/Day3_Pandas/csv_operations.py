import pandas as pd

# Create a DataFrame manually for employee data
employees = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105],
    'Name': ['Rahul', 'Anjali', 'Kiran', 'Sneha', 'Ajay'],
    'Age': [24, 25, 23, 26, 27],
    'Department': ['IT', 'HR', 'Finance', 'IT', 'Sales'],
    'Salary': [35000, 40000, 38000, 42000, 45000]
})

# Save the manual dataset to a CSV file
employees.to_csv('employees.csv', index=False)
print('Saved employees.csv')

# Read CSV file into a DataFrame
df = pd.read_csv('employees.csv')
print('\nRead CSV file:')
print(df)
print()

# Display first 5 rows
print('First 5 rows:')
print(df.head())
print()

# Display last 5 rows
print('Last 5 rows:')
print(df.tail())
print()

# Save DataFrame as new CSV
new_csv_file = 'employees_copy.csv'
df.to_csv(new_csv_file, index=False)
print(f'Saved new CSV file: {new_csv_file}')

# Export DataFrame to Excel
excel_file = 'employees.xlsx'
df.to_excel(excel_file, index=False)
print(f'Saved Excel file: {excel_file}')
