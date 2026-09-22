import pandas as pd
import random
from datetime import datetime, timedelta
import os

random.seed(42)

routes = [
    ("DEL", "BOM"),
    ("DEL", "BLR"),
    ("DEL", "HYD"),
    ("DEL", "CCU"),
    ("BOM", "BLR"),
    ("BOM", "DEL"),
    ("BLR", "HYD"),
    ("DEL", "MAA")
]

airlines = [
    "IndiGo",
    "Air India",
    "Akasa Air",
    "SpiceJet"
]

start_date = datetime(2026, 8, 1)

data = []

for day in range(31):

    date = start_date + timedelta(days=day)

    for origin, destination in routes:

        for airline in airlines:

            # Base fare differs by route
            route_base = {
                ("DEL", "BOM"): 4000,
                ("DEL", "BLR"): 4500,
                ("DEL", "HYD"): 3500,
                ("DEL", "CCU"): 4200,
                ("BOM", "BLR"): 3000,
                ("BOM", "DEL"): 4000,
                ("BLR", "HYD"): 2800,
                ("DEL", "MAA"): 4500
            }[(origin, destination)]

            # Increasing trend + random variation
            trend = day * random.uniform(20, 45)

            airline_factor = {
                "IndiGo": 1.00,
                "Air India": 1.08,
                "Akasa Air": 0.96,
                "SpiceJet": 0.92
            }[airline]

            base_fare = (
                route_base
                + trend
            ) * airline_factor

            base_fare += random.randint(-250, 250)

            base_fare = max(1500, round(base_fare))

            taxes = round(base_fare * 0.18)

            total_fare = base_fare + taxes

            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "origin": origin,
                "destination": destination,
                "airline": airline,
                "base_fare": base_fare,
                "taxes": taxes,
                "total_fare": total_fare,
                "fare_class": random.choice(
                    ["Economy", "Economy Saver"]
                ),
                "availability": random.randint(5, 80),
                "source": random.choice(
                    ["Airline Portal", "OTA"]
                )
            })


df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)

df.to_csv("data/fare_data.csv", index=False)

print("Sample airfare data generated successfully.")
print(f"Total observations: {len(df)}")