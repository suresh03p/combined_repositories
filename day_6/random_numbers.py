import numpy as np

# Student Marks
student_marks = np.random.randint(0, 101, size=10)
print("Student Marks:", student_marks)
print("Max:", student_marks.max())
print("Min:", student_marks.min())
print("Mean:", student_marks.mean())
print("Std Dev:", student_marks.std())
print()

# Employee Salaries
employee_salaries = np.random.randint(30000, 100001, size=10)
print("Employee Salaries:", employee_salaries)
print("Max:", employee_salaries.max())
print("Min:", employee_salaries.min())
print("Mean:", employee_salaries.mean())
print("Std Dev:", employee_salaries.std())
print()

# Product Prices
product_prices = np.random.rand(10) * 100
print("Product Prices:", product_prices)
print("Max:", product_prices.max())
print("Min:", product_prices.min())
print("Mean:", product_prices.mean())
print("Std Dev:", product_prices.std())
print()

# Monthly Sales
monthly_sales = np.random.randint(500, 5001, size=12)
print("Monthly Sales:", monthly_sales)
print("Max:", monthly_sales.max())
print("Min:", monthly_sales.min())
print("Mean:", monthly_sales.mean())
print("Std Dev:", monthly_sales.std())
print()

# Demonstrate functions explicitly
print("np.random.rand(3):", np.random.rand(3))
print("np.random.randint(1, 10, size=3):", np.random.randint(1, 10, size=3))
print("np.random.randn(3):", np.random.randn(3))
print("np.random.choice([10, 20, 30, 40], size=3):", np.random.choice([10, 20, 30, 40], size=3))
np.random.seed(42)
print("np.random.seed(42) then rand(3):", np.random.rand(3))
