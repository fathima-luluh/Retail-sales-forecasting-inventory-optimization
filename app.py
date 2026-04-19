import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Forecast System", layout="wide")

st.title("📊 Retail Sales Forecasting & Inventory Optimization System")

# -----------------------------
# LOAD DATA
# -----------------------------
inventory_df = pd.read_csv("data/inventory_recommendations.csv")
sales_df = pd.read_csv("data/cleaned_sales.csv")
pred_df = pd.read_csv("data/predictions.csv")

# Clean column names (VERY IMPORTANT)
inventory_df.columns = inventory_df.columns.str.strip()
sales_df.columns = sales_df.columns.str.strip()
pred_df.columns = pred_df.columns.str.strip()

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Select Filters")

store = st.sidebar.selectbox("Select Store", inventory_df["store_id"].unique())
item = st.sidebar.selectbox("Select Item", inventory_df["item_id"].unique())

# -----------------------------
# FILTER INVENTORY
# -----------------------------
filtered = inventory_df[
    (inventory_df["store_id"] == store) &
    (inventory_df["item_id"] == item)
]

st.subheader("📦 Inventory Recommendation")

if not filtered.empty:
    row = filtered.iloc[0]

    st.write("Safety Stock:", float(row["safety_stock"]))
    st.write("Reorder Point:", float(row["reorder_point"]))
    st.write("Current Stock:", int(row["current_stock"]))

    if bool(row["reorder_flag"]):
        st.error("⚠ Reorder Required!")
    else:
        st.success("Stock Level is Safe")

    st.dataframe(filtered)

    # Download button
    csv = filtered.to_csv(index=False)
    st.download_button("📥 Download Report", csv, "inventory_report.csv", "text/csv")

else:
    st.warning("No data found for selected filter")

# -----------------------------
# MERGE FOR FORECAST PLOT
# -----------------------------
forecast_df = sales_df.merge(
    pred_df,
    on=["store_id", "item_id"],
    how="inner"
)

# Rename columns safely (fix case mismatch)
forecast_df.rename(columns={
    "Actual": "Actual",
    "Predicted": "Predicted"
}, inplace=True)

st.subheader("📈 Forecast vs Actual")

# -----------------------------
# CHECK COLUMNS SAFELY
# -----------------------------
if "Actual" in forecast_df.columns and "Predicted" in forecast_df.columns:

    forecast_df = forecast_df.dropna(subset=["Actual", "Predicted"])

    fig, ax = plt.subplots()

    ax.plot(forecast_df["Actual"].values, label="Actual")
    ax.plot(forecast_df["Predicted"].values, label="Predicted")

    ax.set_xlabel("Time")
    ax.set_ylabel("Sales")
    ax.legend()

    st.pyplot(fig)

else:
    st.warning("Actual/Predicted columns not found in dataset")
    st.dataframe(forecast_df)