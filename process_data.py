import pandas as pd
import numpy as np

# Load dataset
df = pd.read_parquet("data/yellow_tripdata_2026-01.parquet")

# Select relevant columns
df = df[
    [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "trip_distance",
        "PULocationID",
        "DOLocationID",
        "fare_amount",
        "total_amount",
    ]
]

# Convert datetime
df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

# Create trip duration (minutes)
df["trip_duration"] = (
    (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"])
    .dt.total_seconds() / 60
)

# Remove bad data
df = df[
    (df["trip_distance"] > 0) &
    (df["trip_duration"] > 0) &
    (df["fare_amount"] > 0)
]

# ---- Time Features ----
df["hour"] = df["tpep_pickup_datetime"].dt.hour
df["day_of_week"] = df["tpep_pickup_datetime"].dt.dayofweek

# Peak hours (simple assumption)
df["is_peak"] = df["hour"].isin([8,9,10,17,18,19]).astype(int)

# ---- Demand (Trips per hour) ----
hourly_demand = df.groupby("hour").size().reset_index(name="demand")

# Merge back
df = df.merge(hourly_demand, on="hour", how="left")

# ---- Supply Simulation ----
np.random.seed(42)

df["drivers_available"] = (
    df["demand"] * np.random.uniform(0.6, 0.9, size=len(df))
)

# ---- Surge Pricing ----
df["surge"] = df["demand"] / df["drivers_available"]
df["surge"] = df["surge"].clip(lower=1, upper=3)

# ---- Adjusted Fare ----
df["adjusted_fare"] = df["fare_amount"] * df["surge"]

# ---- Conversion Model ----
k = 0.5
df["conversion_rate"] = np.exp(-k * (df["surge"] - 1))

# ---- Revenue ----
df["expected_revenue"] = df["adjusted_fare"] * df["conversion_rate"]

# Save processed data
df.to_csv("processed_taxi_data.csv", index=False)

print("✅ Data processed and saved!")