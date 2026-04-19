import pandas as pd
import numpy as np

df = pd.read_csv("data/predictions.csv")

# Average demand per item-store
summary = df.groupby(["store_id", "item_id"])["Predicted"].mean().reset_index()
summary.rename(columns={"Predicted": "avg_demand"}, inplace=True)

# Inventory assumptions
lead_time = 3  # days
service_level_factor = 1.65  # ~95% service level
safety_stock_factor = 0.2

# Inventory calculations
summary["safety_stock"] = summary["avg_demand"] * safety_stock_factor
summary["reorder_point"] = (summary["avg_demand"] * lead_time) + summary["safety_stock"]
summary["recommended_stock"] = summary["reorder_point"] * 1.5

# Simulated current stock
np.random.seed(42)
summary["current_stock"] = np.random.randint(10, 100, len(summary))

# Reorder decision
summary["reorder_flag"] = summary["current_stock"] < summary["reorder_point"]

# Save output
summary.to_csv("data/inventory_recommendations.csv", index=False)

print("Inventory Optimization Completed!")
print(summary.head())