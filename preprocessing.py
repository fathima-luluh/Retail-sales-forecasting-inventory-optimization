import pandas as pd

df = pd.read_csv("data/retail_sales.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Sort
df = df.sort_values(["store_id", "item_id", "date"])

# Check missing values
print("Missing values:\n", df.isnull().sum())

# Basic stats
print("\nDataset Info:\n", df.describe())

# Save cleaned data
df.to_csv("data/cleaned_sales.csv", index=False)

print("\nPreprocessing completed successfully!")