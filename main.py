from src.visualization import plot_forecast
from src.data_preprocessing import load_data
from src.feature_engineering import create_features
from src.model import train_model
from src.inventory import calculate_inventory

print("Step 1: Loading data...")
df = load_data()

print("Step 2: Creating features...")
df = create_features(df)

print("Step 3: Preparing data...")
X = df[["lag_1", "lag_7", "rolling_mean"]]
y = df["sales"]

print("Step 4: Training model...")
model = train_model(X, y)

print("Step 5: Generating forecast...")
forecast = model.predict(X.tail(7))

std = y.std()

print("Step 6: Calculating inventory...")
ss, rop = calculate_inventory(forecast, std)

print("\n✅ RESULTS")
print("Forecast (next 7 days):", forecast)
print("Safety Stock:", round(ss, 2))
print("Reorder Point:", round(rop, 2))
print("Step 7: Plotting forecast...")
plot_forecast(df, forecast)