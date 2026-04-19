import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)

np.random.seed(42)

dates = pd.date_range("2023-01-01", periods=365)

data = []

for store in range(1, 4):
    for item in range(1, 6):
        base = np.random.randint(20, 100)

        for date in dates:
            seasonality = 10 * np.sin(date.dayofyear / 365 * 2 * np.pi)
            noise = np.random.randint(-5, 5)

            sales = max(0, base + seasonality + noise)

            data.append([store, item, date, sales])

df = pd.DataFrame(data, columns=["store_id","item_id","date","sales"])

df.to_csv("data/retail_sales.csv", index=False)

print("Dataset created successfully!")