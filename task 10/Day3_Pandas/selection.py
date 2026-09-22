import pandas as pd

# Create an example employee DataFrame
employees = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105],
    'Name': ['Rahul', 'Anjali', 'Kiran', 'Sneha', 'Ajay'],
    'Age': [24, 25, 23, 26, 27],
    'Department': ['IT', 'HR', 'Finance', 'IT', 'Sales'],
    'Salary': [35000, 40000, 38000, 42000, 45000]
})

# Single row using loc
print('Single row with loc (ID 101):')
print(employees.loc[0])
print()

# Multiple rows using loc
print('Multiple rows with loc (first three rows):')
print(employees.loc[0:2])
print()

# Single column using loc
print('Single column Name using loc:')
print(employees.loc[:, 'Name'])
print()

# Multiple columns using loc
print('Multiple columns Name and Salary using loc:')
print(employees.loc[:, ['Name', 'Salary']])
print()

# First row using iloc
print('First row with iloc:')
print(employees.iloc[0])
print()

# Last row using iloc
print('Last row with iloc:')
print(employees.iloc[-1])
print()

# Employee by ID (3rd row)
print('Employee by ID using iloc (third row):')
print(employees.iloc[2])
print()

# Retrieve a specific value: Name of employee in first row
print('Name of employee in first row:')
print(employees.loc[0, 'Name'])
print()

# Retrieve multiple rows and columns using iloc
print('Rows 1 to 3 and columns 1 to 3 using iloc:')
print(employees.iloc[0:3, 1:4])
