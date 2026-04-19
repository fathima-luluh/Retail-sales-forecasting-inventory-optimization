def create_features(df):
    df = df.sort_values("date")

    df["lag_1"] = df["sales"].shift(1)
    df["lag_7"] = df["sales"].shift(7)
    df["rolling_mean"] = df["sales"].rolling(7).mean()

    df = df.dropna()
    return df