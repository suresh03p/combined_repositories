# Employee handles employee data

class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


# Salary Calculation

class SalaryCalculator:

    def calculate_salary(self, employee):
        print(
            f"Salary of {employee.name}: "
            f"{employee.salary}"
        )


# Database Storage

class EmployeeRepository:

    def save(self, employee):
        print(
            f"{employee.name} saved to database"
        )


emp = Employee("Suresh", 50000)

SalaryCalculator().calculate_salary(emp)

EmployeeRepository().save(emp)