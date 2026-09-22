import sqlite3
import pandas as pd
import streamlit as st


DATABASE = "data/airfare.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    df = pd.read_csv("data/fare_data.csv")

    df.to_sql(
        "fare_observations",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print("Database created successfully.")
    print(f"Records inserted: {len(df)}")


@st.cache_data(ttl=600)
def get_data():
    """
    Cached read of the fare observations table.
    Caching avoids re-hitting SQLite on every widget interaction,
    which is what makes the filters feel instant.
    """

    connection = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        "SELECT * FROM fare_observations",
        connection
    )

    connection.close()

    df["date"] = pd.to_datetime(df["date"])

    return df


if __name__ == "__main__":
    create_database()