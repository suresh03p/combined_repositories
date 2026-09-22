import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("employees_dirty.csv")

    total_duplicates = df.duplicated().sum()
    print(f"Total duplicate rows: {total_duplicates}\n")

    duplicate_rows = df[df.duplicated()]
    print("=== Duplicate Rows ===")
    print(duplicate_rows, "\n")

    cleaned_df = df.drop_duplicates()
    removed = df.shape[0] - cleaned_df.shape[0]
    print(f"Removed duplicate rows: {removed}")
    print(f"Final dataset size: {cleaned_df.shape[0]} rows, {cleaned_df.shape[1]} columns\n")

    cleaned_df.to_csv("cleaned_duplicates.csv", index=False)
    print("Exported cleaned duplicates file to cleaned_duplicates.csv")
