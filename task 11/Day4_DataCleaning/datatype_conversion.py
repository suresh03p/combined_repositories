import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("employees_dirty.csv")

    print("=== Before Conversion ===")
    print(df.dtypes, "\n")

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce").astype("Float64")
    df["Experience"] = pd.to_numeric(df["Experience"], errors="coerce").astype("Int64")
    df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce")

    print("=== After Conversion ===")
    print(df.dtypes, "\n")

    print(df.head())
    df.to_csv("datatype_converted.csv", index=False)
    print("Exported dataset with converted data types to datatype_converted.csv")
