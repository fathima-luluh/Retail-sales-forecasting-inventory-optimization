import matplotlib.pyplot as plt

# Check if filtered data exists
if not filtered.empty:
    row = filtered.iloc[0]

    st.subheader("📈 Forecast vs Actual")

    fig, ax = plt.subplots()
    ax.plot(filtered["actual"], label="Actual")
    ax.plot(filtered["predicted"], label="Predicted")
    ax.legend()

    st.pyplot(fig)

    # Download button
    csv = filtered.to_csv(index=False)
    st.download_button(
        "📥 Download Report",
        csv,
        "forecast_report.csv",
        "text/csv"
    )

    # Reorder alert
    if filtered["reorder_flag"].iloc[0]:
        st.error("⚠ Reorder Required!")
    else:
        st.success("Stock Level is Safe")

    # Display inventory values
    st.write("Safety Stock:", float(row["safety_stock"]))
    st.write("Reorder Point:", float(row["reorder_point"]))
    st.write("Current Stock:", int(row["current_stock"]))

else:
    st.warning("No data available")