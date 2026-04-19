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

# Load and prepare data
df = load_data()
df = create_features(df)

X = df[["lag_1", "lag_7", "rolling_mean"]]
y = df["sales"]

# Train model
model = train_model(X, y)

# Sidebar inputs
st.sidebar.header("Input Parameters")
on_hand = st.sidebar.number_input("Current Stock", value=100)
lead_time = st.sidebar.number_input("Lead Time (days)", value=7)

# Forecast
forecast = model.predict(X.tail(7))
std = y.std()

# Inventory calculation
ss, rop = calculate_inventory(forecast, std, lead_time)

# Display
st.subheader("📈 Forecast (Next 7 Days)")
st.write(forecast)

st.subheader("📦 Inventory Recommendation")
st.write(f"Safety Stock: {round(ss,2)}")
st.write(f"Reorder Point: {round(rop,2)}")

# Chart
st.line_chart(df.set_index("date")["sales"])