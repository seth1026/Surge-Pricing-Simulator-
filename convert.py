import pandas as pd

df = pd.read_csv("processed_taxi_data.csv")

# Take smaller sample
df_sample = df.sample(n=50000, random_state=42)

df_sample.to_csv("sample_data.csv", index=False)

print("Sample dataset created!")