import streamlit as st
import pandas as pd
import numpy as np

# ---- Config ----
st.set_page_config(layout="wide")
st.title("🚖 Dynamic Pricing & Demand Intelligence Dashboard")

# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_csv("sample_data.csv")

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

    return df


df = load_data()

# ---- Sidebar ----
st.sidebar.header("⚙️ Controls")

driver_multiplier = st.sidebar.slider("Driver Supply Multiplier", 0.5, 2.0, 1.0)
base_fare_multiplier = st.sidebar.slider("Base Fare Multiplier", 0.5, 2.0, 1.0)
selected_hour = st.sidebar.slider("Filter by Hour", 0, 23, (0, 23))

# ---- Scenario ----
st.sidebar.header("🌍 Scenario Simulation")

scenario = st.sidebar.selectbox(
    "Select Scenario",
    ["Normal", "Rush Hour", "Rain", "Driver Strike", "High Supply"]
)

st.info(f"📌 Current Scenario: **{scenario}**")

# ---- Filter ----
df_filtered = df[
    (df["hour"] >= selected_hour[0]) &
    (df["hour"] <= selected_hour[1])
]

# ---- Scenario Adjustments ----
sim_df = df_filtered.copy()

if scenario == "Rush Hour":
    sim_df["demand"] *= 1.4
    sim_df["drivers_available"] *= 1.1

elif scenario == "Rain":
    sim_df["demand"] *= 1.3
    sim_df["drivers_available"] *= 0.8

elif scenario == "Driver Strike":
    sim_df["drivers_available"] *= 0.5

elif scenario == "High Supply":
    sim_df["drivers_available"] *= 1.5

# ---- Simulation Engine ----
sim_df["drivers_available"] *= driver_multiplier

sim_df["surge"] = sim_df["demand"] / sim_df["drivers_available"]
sim_df["surge"] = sim_df["surge"].clip(lower=1, upper=3)

sim_df["adjusted_fare"] = sim_df["fare_amount"] * sim_df["surge"] * base_fare_multiplier

k = 0.5
sim_df["conversion_rate"] = np.exp(-k * (sim_df["surge"] - 1))

sim_df["expected_revenue"] = sim_df["adjusted_fare"] * sim_df["conversion_rate"]

# ---- BASE METRICS ----
base_revenue = df_filtered["expected_revenue"].sum()
base_surge = df_filtered["surge"].mean()

# approximate base conversion proxy
base_conversion = (df_filtered["expected_revenue"] / df_filtered["fare_amount"]).mean()

# ---- SIM METRICS ----
sim_revenue = sim_df["expected_revenue"].sum()
sim_surge = sim_df["surge"].mean()
sim_conversion = sim_df["conversion_rate"].mean()

# ---- % CHANGE ----
revenue_change = ((sim_revenue - base_revenue) / base_revenue) * 100
surge_change = ((sim_surge - base_surge) / base_surge) * 100
conversion_change = ((sim_conversion - base_conversion) / base_conversion) * 100

# ---- KPIs ----
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Trips", len(sim_df))
col2.metric("Revenue", f"{sim_revenue:,.0f}", f"{revenue_change:.2f}%")
col3.metric("Avg Surge", f"{sim_surge:.2f}", f"{surge_change:.2f}%")
col4.metric("Conversion Rate", f"{sim_conversion:.2f}", f"{conversion_change:.2f}%")

# ---- Aggregation ----
agg_df = sim_df.groupby("hour").agg({
    "demand": "mean",
    "drivers_available": "mean",
    "surge": "mean",
    "expected_revenue": "sum"
}).reset_index()

# ---- Charts ----
st.subheader("📈 Demand vs Supply")
st.line_chart(agg_df.set_index("hour")[["demand", "drivers_available"]])

st.subheader("💸 Surge Trend")
st.line_chart(agg_df.set_index("hour")["surge"])

st.subheader("💰 Revenue Trend")
st.line_chart(agg_df.set_index("hour")["expected_revenue"])

# ---- Revenue vs Surge (FIXED) ----
st.subheader("📊 Revenue vs Surge")

sim_df["surge_bucket"] = pd.cut(sim_df["surge"], bins=10)

rev_surge = (
    sim_df.groupby("surge_bucket")["expected_revenue"]
    .mean()
    .reset_index()
)

rev_surge["surge_bucket"] = rev_surge["surge_bucket"].astype(str)

rev_surge = rev_surge.set_index("surge_bucket")

st.line_chart(rev_surge)

# ---- Insights ----
st.subheader("🧠 Key Insights")

peak_hour = agg_df.loc[agg_df["demand"].idxmax(), "hour"]
low_supply_hour = agg_df.loc[agg_df["drivers_available"].idxmin(), "hour"]

high_surge_count = (sim_df["surge"] > 1.5).sum()

st.write(f"• Peak demand occurs around **{peak_hour}:00 hrs**")
st.write(f"• Lowest driver availability occurs around **{low_supply_hour}:00 hrs**")
st.write(f"• {high_surge_count} rides experience surge pricing above 1.5x")

st.write(f"• Revenue changed by **{revenue_change:.2f}%** under current simulation")
st.write(f"• Surge changed by **{surge_change:.2f}%**, impacting demand and pricing")

# ---- Scenario Insights ----
if scenario == "Rain":
    st.write("🌧️ Rain increases demand but reduces supply → higher surge, lower conversion")

elif scenario == "Driver Strike":
    st.write("🚫 Driver strike drastically reduces supply → extreme surge, demand drops")

elif scenario == "Rush Hour":
    st.write("🚦 Rush hour increases demand → moderate surge and higher revenue")

elif scenario == "High Supply":
    st.write("🟢 Increased supply reduces surge → better conversion but lower price")

# ---- Final Insight ----
st.info("💡 Optimal pricing lies in balancing demand and supply. Excess surge reduces conversion, while low surge limits revenue.")
