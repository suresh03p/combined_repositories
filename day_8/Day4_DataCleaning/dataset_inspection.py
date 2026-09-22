import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("employees_dirty.csv")

    print("=== First 10 Rows ===")
    print(df.head(10), "\n")

    print("=== Last 10 Rows ===")
    print(df.tail(10), "\n")

    print("=== Number of Rows and Columns ===")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}", "\n")

    print("=== Column Names ===")
    print(df.columns.tolist(), "\n")

    print("=== Data Types ===")
    print(df.dtypes, "\n")

    print("=== Dataset Information ===")
    df.info()
    print("\n=== Summary Statistics ===")
    print(df.describe(include='all'))
