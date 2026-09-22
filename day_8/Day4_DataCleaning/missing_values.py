import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("employees_dirty.csv")

    print("=== Missing Value Count ===")
    print(df.isnull().sum(), "\n")

    print("=== Rows with Any Missing Values ===")
    print(df[df.isnull().any(axis=1)], "\n")

    print("=== Drop Rows with Missing Values ===")
    dropna_df = df.dropna()
    print(f"Rows after dropna: {dropna_df.shape[0]}")
    print(dropna_df, "\n")

    print("=== Fill Missing Numeric Values with Mean or Median ===")
    fill_df = df.copy()
    fill_df["Age"] = pd.to_numeric(fill_df["Age"], errors="coerce")
    fill_df["Salary"] = pd.to_numeric(fill_df["Salary"], errors="coerce")
    fill_df["Experience"] = pd.to_numeric(fill_df["Experience"], errors="coerce")
    fill_df["Age"] = fill_df["Age"].fillna(fill_df["Age"].mean())
    fill_df["Salary"] = fill_df["Salary"].fillna(fill_df["Salary"].median())
    fill_df["Experience"] = fill_df["Experience"].fillna(fill_df["Experience"].median())
    print(fill_df[fill_df.isnull().any(axis=1)], "\n")

    print("=== Fill Missing Categorical Values with Mode ===")
    mode_df = df.copy()
    if mode_df["Department"].isnull().any():
        mode_df["Department"] = mode_df["Department"].fillna(mode_df["Department"].mode()[0])
    if mode_df["Email"].isnull().any():
        mode_df["Email"] = mode_df["Email"].fillna("unknown@example.com")
    if mode_df["City"].isnull().any():
        mode_df["City"] = mode_df["City"].fillna(mode_df["City"].mode()[0])
    print(mode_df[mode_df.isnull().any(axis=1)], "\n")

    print("=== Forward Fill ===")
    ffill_df = df.fillna(method="ffill")
    print(ffill_df[ffill_df.isnull().any(axis=1)], "\n")

    print("=== Backward Fill ===")
    bfill_df = df.fillna(method="bfill")
    print(bfill_df[bfill_df.isnull().any(axis=1)], "\n")

    print("=== Summary of Methods ===")
    print(f"Original missing rows: {df.isnull().any(axis=1).sum()}")
    print(f"dropna keeps rows: {dropna_df.shape[0]}")
    print(f"fill mean/median keeps missing rows: {fill_df.isnull().any(axis=1).sum()}")
    print(f"forward fill keeps missing rows: {ffill_df.isnull().any(axis=1).sum()}")
    print(f"backward fill keeps missing rows: {bfill_df.isnull().any(axis=1).sum()}")
