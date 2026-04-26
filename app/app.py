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
@st.cache_data
def get_data():
    df = load_data()
    df = create_features(df)
    return df

df = get_data()

X = df[["lag_1", "lag_7", "rolling_mean"]]
y = df["sales"]

# Train model
@st.cache_resource
def get_model(X, y):
    return train_model(X, y)

model = get_model(X, y)

# Sidebar inputs
st.sidebar.header("Input Parameters")
on_hand = st.sidebar.number_input("Current Stock", value=100)
lead_time = st.sidebar.number_input("Lead Time (days)", value=7)

# Forecast
future_X = X.tail(7).copy()
forecast = model.predict(future_X)
std = y.std()

# Inventory calculation
ss, rop = calculate_inventory(
    forecast.mean(),
    std,
    lead_time
)

# Display
st.subheader("📈 Forecast (Next 7 Days)")
st.write(forecast)

st.subheader("📦 Inventory Recommendation")
st.write(f"Safety Stock: {round(ss,2)}")
st.write(f"Reorder Point: {round(rop,2)}")

# Chart
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    st.line_chart(df.sort_values("date").set_index("date")["sales"])
else:
    st.warning("Date column not found for chart")
    st.line_chart(df["sales"])