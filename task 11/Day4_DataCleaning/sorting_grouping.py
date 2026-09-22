import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("employees_dirty.csv")
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Experience"] = pd.to_numeric(df["Experience"], errors="coerce")

    print("=== Sorted by Salary ===")
    print(df.sort_values(by="Salary", ascending=False).head(), "\n")

    print("=== Sorted by Age ===")
    print(df.sort_values(by="Age").head(), "\n")

    print("=== Sorted by Experience ===")
    print(df.sort_values(by="Experience", ascending=False).head(), "\n")

    print("=== Filter: IT Department ===")
    print(df[df["Department"] == "IT"], "\n")

    print("=== Filter: Salary > 50000 ===")
    print(df[df["Salary"] > 50000], "\n")

    print("=== Filter: Experience > 5 Years ===")
    print(df[df["Experience"] > 5], "\n")

    print("=== Group by Department ===")
    dept_group = df.groupby("Department")
    summary = dept_group["Salary"].agg(["mean", "max", "min", "count"]).rename(columns={
        "mean": "Average Salary",
        "max": "Maximum Salary",
        "min": "Minimum Salary",
        "count": "Employee Count"
    })
    print(summary, "\n")
