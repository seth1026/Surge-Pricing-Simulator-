# 🚖 Ride Pricing Intelligence

A dynamic pricing and demand-supply simulation system for ride-hailing platforms, built using real-world NYC Taxi data.

---

## 🚀 Live Demo
👉 (https://kkxeahrc7c4rjnunwnis5r.streamlit.app/)

---

## 🎯 Problem

Ride-hailing platforms (Uber, Ola, Swiggy logistics) must continuously balance:

- Rider demand 📈  
- Driver supply 🚗  
- Dynamic pricing (surge) 💸  

Poor balance leads to:
- High wait times  
- Low conversions  
- Revenue loss  

This project models how **pricing strategies impact revenue, demand, and user behavior**.

---

## ⚙️ What This System Does

- Models **demand-supply imbalance** using real-world data  
- Simulates **surge pricing dynamically**  
- Estimates **user conversion drop at higher prices**  
- Enables **scenario-based decision making**  

---

## 🎛️ Key Features

- 📊 Dynamic Pricing Engine (surge based on demand/supply)  
- ⚡ Scenario Simulation:
  - Rush Hour
  - Rain Conditions
  - Driver Strike
  - High Supply  
- 📈 Revenue & Conversion Impact Analysis  
- 🎯 Interactive Dashboard (Streamlit)  

---

## 📊 Key Insights

- Peak demand occurs around **~6 PM**, while lowest supply is around **~4 AM**  
- **22,000+ rides** experienced high surge pricing (>1.5x)  
- Surge can increase by **~60–97% under supply shocks**, causing **~50–60% drop in conversion**  
- Optimal pricing strategies can yield **~6.5% revenue improvement**  

---

## 🧠 Product Thinking

This project focuses on **trade-offs**, not just visualization:

- Higher surge → ↑ revenue per ride but ↓ conversion  
- More supply → ↓ surge but ↑ ride completion  
- Optimal pricing lies in balancing both  

👉 Simulates real-world pricing decisions used in ride-hailing platforms.

---

## 🛠️ Tech Stack

- Python (Pandas, NumPy)  
- Streamlit  
- Data Modeling & Simulation  

---

## 📁 Dataset

- Uses NYC Taxi Trip Data  
- Due to size constraints, a **sample dataset (50K rows)** is included  

Full dataset:  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
