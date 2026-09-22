import pandas as pd

# Create an example employee DataFrame
employees = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105],
    'Name': ['Rahul', 'Anjali', 'Kiran', 'Sneha', 'Ajay'],
    'Age': [24, 25, 23, 26, 27],
    'Department': ['IT', 'HR', 'Finance', 'IT', 'Sales'],
    'Salary': [35000, 40000, 38000, 42000, 45000]
})

# Salary > 40000
high_salary = employees[employees['Salary'] > 40000]
print('Employees with salary > 40000:')
print(high_salary)
print()

# Department = IT
it_department = employees[employees['Department'] == 'IT']
print('Employees in IT department:')
print(it_department)
print()

# Age > 24
age_above_24 = employees[employees['Age'] > 24]
print('Employees with age > 24:')
print(age_above_24)
print()

# Salary between 35000 and 45000
salary_between = employees[(employees['Salary'] >= 35000) & (employees['Salary'] <= 45000)]
print('Employees with salary between 35000 and 45000:')
print(salary_between)
print()

# Names starting with A
names_starting_with_a = employees[employees['Name'].str.startswith('A')]
print('Employees whose names start with A:')
print(names_starting_with_a)
