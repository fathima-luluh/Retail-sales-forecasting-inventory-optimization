import streamlit as st
import pandas as pd

st.title("Retail Sales Forecasting & Inventory Optimization System")

df = pd.read_csv("data/inventory_recommendations.csv")

store = st.selectbox("Select Store", df["store_id"].unique())
item = st.selectbox("Select Item", df["item_id"].unique())

filtered = df[(df["store_id"] == store) & (df["item_id"] == item)]

st.subheader("Inventory Recommendation")
st.dataframe(filtered)

if not filtered.empty:
    row = filtered.iloc[0]

st.subheader("📈 Forecast vs Actual")

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(filtered["actual"], label="Actual")
ax.plot(filtered["predicted"], label="Predicted")
ax.legend()

st.pyplot(fig)


csv = filtered.to_csv(index=False)
st.download_button(
    "📥 Download Report",
    csv,
    "forecast_report.csv",
    "text/csv"
)

if filtered["reorder_flag"].iloc[0]:
    st.error("⚠ Reorder Required!")
else:
    st.success("Stock Level is Safe")


st.write("Safety Stock:", float(row["safety_stock"]))
st.write("Reorder Point:", float(row["reorder_point"]))
st.write("Current Stock:", int(row["current_stock"]))
st.write("Reorder Needed:", bool(row["reorder_flag"]))