import pandas as pd


def calculate_index(df):
    """Overall daily airfare price index (base = first day = 100)."""

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    daily_average = (
        df.groupby("date")["total_fare"]
        .mean()
        .reset_index()
    )

    base_price = daily_average["total_fare"].iloc[0]

    daily_average["index"] = (
        daily_average["total_fare"] / base_price
    ) * 100

    return daily_average


def calculate_route_index(df, origin, destination):
    """Daily index for a single origin-destination route."""

    route_df = df[
        (df["origin"] == origin) &
        (df["destination"] == destination)
    ].copy()

    route_df["date"] = pd.to_datetime(route_df["date"])

    daily_average = (
        route_df.groupby("date")["total_fare"]
        .mean()
        .reset_index()
    )

    if daily_average.empty:
        return daily_average

    base_price = daily_average["total_fare"].iloc[0]

    daily_average["index"] = (
        daily_average["total_fare"] / base_price
    ) * 100

    return daily_average


def get_airline_average(df):
    """Average fare per airline, cheapest first."""

    if df.empty:
        return df

    return (
        df.groupby("airline")["total_fare"]
        .mean()
        .reset_index()
        .sort_values("total_fare")
    )


def get_wow_change(index_df):
    """Week-over-week % change in the index (last 7 days vs prior 7 days)."""

    if len(index_df) < 8:
        return None

    last_7 = index_df["total_fare"].iloc[-7:].mean()
    prior_7 = (
        index_df["total_fare"].iloc[-14:-7].mean()
        if len(index_df) >= 14
        else index_df["total_fare"].iloc[:7].mean()
    )

    if prior_7 == 0:
        return None

    return ((last_7 - prior_7) / prior_7) * 100


def get_best_value_airline(df):
    """Airline with the lowest average fare in the current selection."""

    avg = get_airline_average(df)

    if avg.empty:
        return None, None

    row = avg.iloc[0]
    return row["airline"], row["total_fare"]


def get_route_volatility(df):
    """Coefficient of variation (%) of fares per route — higher = more price swings."""

    if df.empty:
        return pd.DataFrame(columns=["route", "volatility"])

    route_df = df.copy()
    route_df["route"] = route_df["origin"] + " → " + route_df["destination"]

    volatility = (
        route_df.groupby("route")["total_fare"]
        .agg(["mean", "std"])
        .reset_index()
    )
    volatility["volatility"] = (
        volatility["std"] / volatility["mean"] * 100
    )

    return volatility[["route", "volatility"]].sort_values(
        "volatility", ascending=False
    )


def filter_data(df, date_range=None, airlines=None, fare_classes=None):
    """Apply sidebar filters (date range, airlines, fare class) to the dataframe."""

    filtered = df.copy()

    if date_range is not None and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[
            (filtered["date"] >= start) & (filtered["date"] <= end)
        ]

    if airlines:
        filtered = filtered[filtered["airline"].isin(airlines)]

    if fare_classes:
        filtered = filtered[filtered["fare_class"].isin(fare_classes)]

    return filtered