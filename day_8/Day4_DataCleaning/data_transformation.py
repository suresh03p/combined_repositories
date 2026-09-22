import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("employees_dirty.csv")

    print("=== Original Columns ===")
    print(df.columns.tolist(), "\n")

    df = df.rename(columns={
        "FirstName": "First_Name",
        "LastName": "Last_Name",
        "JoiningDate": "Joining_Date"
    })

    df["First_Name"] = df["First_Name"].astype(str).str.upper()
    df["Last_Name"] = df["Last_Name"].astype(str).str.upper()
    df["Department"] = df["Department"].astype(str).str.lower()
    df["Full_Name"] = df["First_Name"] + " " + df["Last_Name"]
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    df["Bonus"] = df["Salary"] * 0.10
    df["Annual_Salary"] = df["Salary"] * 12

    columns_to_drop = ["Email", "City"]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    print("=== Transformed Sample ===")
    print(df.head(), "\n")

    df.to_csv("transformed_data.csv", index=False)
    print("Exported transformed dataset to transformed_data.csv")
