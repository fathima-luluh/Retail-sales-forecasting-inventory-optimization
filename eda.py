import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/cleaned_sales.csv")
df["date"] = pd.to_datetime(df["date"])

# 1. Overall sales trend
plt.figure()
df.groupby("date")["sales"].sum().plot()
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Sales by store
plt.figure()
sns.barplot(x="store_id", y="sales", data=df)
plt.title("Sales by Store")
plt.show()

# 3. Sales by item
plt.figure()
sns.barplot(x="item_id", y="sales", data=df)
plt.title("Sales by Item")
plt.show()

print("EDA completed successfully!")