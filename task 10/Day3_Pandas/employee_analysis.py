import pandas as pd

# Create a dataset for 30 employees
data = {
    'Employee ID': list(range(101, 131)),
    'Name': [
        'Rahul', 'Anjali', 'Kiran', 'Sneha', 'Ajay', 'Priya', 'Sameer', 'Pooja', 'Rohan', 'Nisha',
        'Arun', 'Kavita', 'Vikram', 'Meera', 'Sonal', 'Amit', 'Deepa', 'Rakesh', 'Anita', 'Yash',
        'Shreya', 'Raj', 'Smita', 'Gaurav', 'Nidhi', 'Ayesha', 'Dev', 'Komal', 'Suresh', 'Tanvi'
    ],
    'Age': [24, 25, 23, 26, 27, 29, 30, 28, 32, 31, 22, 27, 33, 24, 26, 35, 29, 34, 28, 30, 23, 26, 31, 29, 27, 24, 36, 25, 32, 28],
    'Department': [
        'IT', 'HR', 'Finance', 'IT', 'Sales', 'HR', 'IT', 'Finance', 'Sales', 'IT',
        'Finance', 'HR', 'Sales', 'IT', 'HR', 'Finance', 'IT', 'Sales', 'HR', 'IT',
        'Finance', 'HR', 'IT', 'Sales', 'Finance', 'HR', 'IT', 'Sales', 'HR', 'Finance'
    ],
    'Salary': [35000, 40000, 38000, 42000, 45000, 39000, 47000, 36000, 41000, 43000,
               34000, 39500, 46000, 42500, 40500, 38500, 44500, 37500, 41500, 43500,
               36500, 39800, 48000, 44000, 35500, 39000, 47000, 42000, 40000, 45000],
    'Experience': [2, 3, 1, 4, 5, 3, 6, 2, 4, 3, 1, 4, 5, 2, 3, 6, 4, 5, 3, 4, 1, 3, 6, 5, 2, 3, 7, 4, 5, 2]
}

# Create DataFrame
df = pd.DataFrame(data)

# Employee Analysis
highest_salary = df['Salary'].max()
lowest_salary = df['Salary'].min()
average_salary = df['Salary'].mean()
average_age = df['Age'].mean()
total_employees = len(df)

# Department Analysis
it_employees = df[df['Department'] == 'IT']
hr_employees = df[df['Department'] == 'HR']
finance_employees = df[df['Department'] == 'Finance']
sales_employees = df[df['Department'] == 'Sales']

# Experience Analysis
freshers = df[df['Experience'] <= 2]
experienced_employees = df[df['Experience'] > 2]

# Print analysis results
print('--- Employee Analysis ---')
print('Highest Salary:', highest_salary)
print('Lowest Salary:', lowest_salary)
print('Average Salary:', round(average_salary, 2))
print('Average Age:', round(average_age, 2))
print('Total Employees:', total_employees)
print()
print('--- Department Analysis ---')
print('IT Employees:', len(it_employees))
print('HR Employees:', len(hr_employees))
print('Finance Employees:', len(finance_employees))
print('Sales Employees:', len(sales_employees))
print()
print('--- Experience Analysis ---')
print('Freshers (Experience <= 2):', len(freshers))
print('Experienced Employees (Experience > 2):', len(experienced_employees))

# Export final report to CSV
report = {
    'Metric': [
        'Highest Salary', 'Lowest Salary', 'Average Salary', 'Average Age', 'Total Employees',
        'IT Employees', 'HR Employees', 'Finance Employees', 'Sales Employees',
        'Freshers', 'Experienced Employees'
    ],
    'Value': [
        highest_salary, lowest_salary, round(average_salary, 2), round(average_age, 2), total_employees,
        len(it_employees), len(hr_employees), len(finance_employees), len(sales_employees),
        len(freshers), len(experienced_employees)
    ]
}
report_df = pd.DataFrame(report)
report_df.to_csv('employee_report.csv', index=False)
print('\nSaved employee_report.csv')
