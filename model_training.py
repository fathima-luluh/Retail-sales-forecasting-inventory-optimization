import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load data
df = pd.read_csv("data/cleaned_sales.csv")
df["date"] = pd.to_datetime(df["date"])

# Sort values
df = df.sort_values(["store_id", "item_id", "date"])

# Feature Engineering
df["day"] = df["date"].dt.day
df["month"] = df["date"].dt.month
df["dayofweek"] = df["date"].dt.dayofweek

# Lag feature (previous day sales)
df["lag_1"] = df.groupby(["store_id", "item_id"])["sales"].shift(1)

# Drop NA from lag
df = df.dropna()

# Features & Target
features = ["store_id", "item_id", "day", "month", "dayofweek", "lag_1"]
X = df[features]
y = df["sales"]

# Train-test split (simple)
split = int(len(df) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print("MODEL PERFORMANCE")
print("MAE:", mae)
print("R2 Score:", r2)

# Save predictions
output = X_test.copy()
output["Actual"] = y_test.values
output["Predicted"] = preds

output.to_csv("data/predictions.csv", index=False)

print("Model training completed successfully!")