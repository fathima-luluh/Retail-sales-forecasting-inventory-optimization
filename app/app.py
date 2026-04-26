import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

from src.data_preprocessing import load_data
from src.feature_engineering import create_features
from src.model import train_model
from src.inventory import calculate_inventory

st.title("📊 Retail Forecast & Inventory Optimization")

# Load data
@st.cache_data
def get_data():
    df = load_data()
    df = create_features(df)
    return df

df = get_data()

# Features
feature_cols = [col for col in df.columns if col not in ["sales", "date"]]
X = df[feature_cols]
y = df["sales"]

# Train model
@st.cache_resource
def get_model(X, y):
    return train_model(X, y)

model = get_model(X, y)

# Sidebar
st.sidebar.header("Input Parameters")
on_hand = st.sidebar.number_input("Current Stock", value=100)
lead_time = st.sidebar.number_input("Lead Time (days)", value=7)

# Forecast
future_X = X.tail(7)
forecast = model.predict(future_X)
forecast = [max(0, f) for f in forecast]

std = y.std()

# Inventory
ss, rop = calculate_inventory(
    forecast,
    std,
    lead_time
)

# Output
st.subheader("📈 Forecast (Next 7 Days)")

forecast_df = pd.DataFrame({
    "Day": range(1, 8),
    "Predicted Sales": forecast
})
st.dataframe(forecast_df)

st.subheader("📦 Inventory Recommendation")
st.success(f"Safety Stock: {round(ss,2)}")
st.success(f"Reorder Point: {round(rop,2)}")

# Chart
st.subheader("📊 Sales Trend")

if "date" in df.columns:
   df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

st.line_chart(df.set_index("date")["sales"])
else:
    st.line_chart(df["sales"])