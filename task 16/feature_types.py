import pandas as pd


df = pd.DataFrame({
    "Employee_ID": ["E001", "E002", "E003", "E004"],
    "Age": [25, 30, 28, 35],
    "Gender": ["Female", "Male", "Female", "Male"],
    "City": ["Hyderabad", "Chennai", "Hyderabad", "Bangalore"],
    "Department": ["IT", "HR", "Finance", "IT"],
    "Experience": [2, 5, 4, 10],
    "Salary": [30000, 50000, 45000, 80000],
    "Education": ["Bachelor's", "Master's", "Bachelor's", "PhD"],
})

numerical = df.select_dtypes(include=["number"])
categorical = df.select_dtypes(include=["object"])

print("Numerical columns:", list(numerical.columns))
print(numerical)
print("\nCategorical columns:", list(categorical.columns))
print(categorical)