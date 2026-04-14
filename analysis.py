import pandas as pd
import numpy as np

# ---- Load Data ----
df = pd.read_csv("processed_taxi_data.csv")

# Reduce size for speed
df = df.sample(n=100000, random_state=42)

df = df[
    [
        "hour",
        "demand",
        "drivers_available",
        "surge",
        "fare_amount",
        "expected_revenue",
    ]
]

# ---- Base Metrics ----
base_revenue = df["expected_revenue"].sum()
base_surge = df["surge"].mean()
base_conversion = (df["expected_revenue"] / df["fare_amount"]).mean()

print("\n📊 BASELINE METRICS")
print(f"Revenue: {base_revenue:,.0f}")
print(f"Avg Surge: {base_surge:.2f}")
print(f"Conversion Proxy: {base_conversion:.2f}")

# ---- Scenario Function ----
def run_simulation(df, scenario_name):
    sim_df = df.copy()

    # Scenario adjustments
    if scenario_name == "Rush Hour":
        sim_df["demand"] *= 1.4
        sim_df["drivers_available"] *= 1.1

    elif scenario_name == "Rain":
        sim_df["demand"] *= 1.3
        sim_df["drivers_available"] *= 0.8

    elif scenario_name == "Driver Strike":
        sim_df["drivers_available"] *= 0.5

    elif scenario_name == "High Supply":
        sim_df["drivers_available"] *= 1.5

    # ---- Simulation ----
    sim_df["surge"] = sim_df["demand"] / sim_df["drivers_available"]
    sim_df["surge"] = sim_df["surge"].clip(lower=1, upper=3)

    sim_df["adjusted_fare"] = sim_df["fare_amount"] * sim_df["surge"]

    k = 0.5
    sim_df["conversion_rate"] = np.exp(-k * (sim_df["surge"] - 1))

    sim_df["expected_revenue"] = sim_df["adjusted_fare"] * sim_df["conversion_rate"]

    # ---- Metrics ----
    sim_revenue = sim_df["expected_revenue"].sum()
    sim_surge = sim_df["surge"].mean()
    sim_conversion = sim_df["conversion_rate"].mean()

    # % changes
    revenue_change = ((sim_revenue - base_revenue) / base_revenue) * 100
    surge_change = ((sim_surge - base_surge) / base_surge) * 100
    conversion_change = ((sim_conversion - base_conversion) / base_conversion) * 100

    return {
        "scenario": scenario_name,
        "revenue_change": revenue_change,
        "surge_change": surge_change,
        "conversion_change": conversion_change,
    }


# ---- Run All Scenarios ----
scenarios = ["Rush Hour", "Rain", "Driver Strike", "High Supply"]

results = []

print("\n🚀 SCENARIO ANALYSIS\n")

for scenario in scenarios:
    result = run_simulation(df, scenario)
    results.append(result)

    print(f"📌 {scenario}")
    print(f"Revenue Change: {result['revenue_change']:.2f}%")
    print(f"Surge Change: {result['surge_change']:.2f}%")
    print(f"Conversion Change: {result['conversion_change']:.2f}%")
    print("-" * 40)


# ---- Find Best Scenario ----
best = max(results, key=lambda x: x["revenue_change"])

print("\n🏆 BEST SCENARIO FOR REVENUE")
print(f"{best['scenario']} → {best['revenue_change']:.2f}% revenue increase")


# ---- Peak Demand & Supply Gaps ----
peak_hour = df.groupby("hour")["demand"].mean().idxmax()
low_supply_hour = df.groupby("hour")["drivers_available"].mean().idxmin()

high_surge_count = (df["surge"] > 1.5).sum()

print("\n📊 KEY INSIGHTS")
print(f"Peak Demand Hour: {peak_hour}:00")
print(f"Lowest Supply Hour: {low_supply_hour}:00")
print(f"High Surge Rides (>1.5x): {high_surge_count:,}")