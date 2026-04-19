import matplotlib.pyplot as plt

def plot_forecast(df, forecast):
    plt.figure(figsize=(10,5))

    # Actual sales
    plt.plot(df["date"], df["sales"], label="Actual Sales")

    # Forecast (last part of data)
    future_dates = df["date"].tail(len(forecast))
    plt.plot(future_dates, forecast, label="Forecast", linestyle="dashed")

    plt.title("Sales Forecast")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend()

    # Save image
    plt.savefig("outputs/forecast_plot.png")

    # IMPORTANT FIX
    plt.close()   # prevents freezing