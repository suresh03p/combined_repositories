import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("employees_dirty.csv")
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Experience"] = pd.to_numeric(df["Experience"], errors="coerce")

    print("=== Salary Analysis ===")
    print(f"Average Salary: {df['Salary'].mean():.2f}")
    print(f"Highest Salary: {df['Salary'].max():.2f}")
    print(f"Lowest Salary: {df['Salary'].min():.2f}\n")

    print("=== Age Analysis ===")
    print(f"Youngest Employee Age: {df['Age'].min():.0f}")
    print(f"Oldest Employee Age: {df['Age'].max():.0f}")
    print(f"Average Age: {df['Age'].mean():.2f}\n")

    print("=== Department Analysis ===")
    dept_counts = df["Department"].value_counts()
    print("Employees per Department:")
    print(dept_counts, "\n")
    dept_salary = df.groupby("Department")["Salary"].mean()
    print(f"Highest Paying Department: {dept_salary.idxmax()}")
    print(f"Lowest Paying Department: {dept_salary.idxmin()}\n")

    print("=== Experience Analysis ===")
    print(f"Average Experience: {df['Experience'].mean():.2f}")
    most_exp = df.loc[df["Experience"].idxmax()]
    print("Most Experienced Employee:")
    print(most_exp.to_dict())
