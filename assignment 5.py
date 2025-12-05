import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os


data_path = Path("data/")
csv_files = [f for f in data_path.glob("*.csv")]

combined = []

print("\nLoading CSV files...")

for file in csv_files:
    try:
        df = pd.read_csv(file, on_bad_lines='skip')
        df["building"] = file.stem           # filename = building name
        combined.append(df)
        print(f"Loaded {file.name}")
    except Exception as e:
        print(f"Error loading {file.name}: {e}")

df_combined = pd.concat(combined, ignore_index=True)

# Validate & clean
df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'], errors='coerce')
df_combined = df_combined.dropna(subset=['timestamp'])
df_combined['kwh'] = df_combined['kwh'].fillna(0)

print("\nMerged dataset preview:")
print(df_combined.head())


# Daily totals
df_daily = df_combined.set_index('timestamp').groupby('building')['kwh'].resample('D').sum().reset_index()

# Weekly totals
df_weekly = df_combined.set_index('timestamp').groupby('building')['kwh'].resample('W').sum().reset_index()

# Building summary table
building_summary = df_combined.groupby('building')['kwh'].agg(['mean','min','max','sum'])
building_summary.columns = ['avg_kwh','min_kwh','max_kwh','total_kwh']

print("\nBuilding-wise summary:")
print(building_summary)



class MeterReading:
    def _init_(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def _init_(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, timestamp, kwh):
        self.meter_readings.append(MeterReading(timestamp, kwh))

    def calculate_total_consumption(self):
        return sum([r.kwh for r in self.meter_readings])

    def generate_report(self):
        values = [r.kwh for r in self.meter_readings]
        return {
            "building": self.name,
            "total": sum(values),
            "max": max(values) if values else 0,
            "min": min(values) if values else 0,
            "avg": np.mean(values) if values else 0
        }

class BuildingManager:
    def _init_(self):
        self.buildings = {}

    def load_from_dataframe(self, df):
        for _, row in df.iterrows():
            bname = row['building']
            if bname not in self.buildings:
                self.buildings[bname] = Building(bname)
            self.buildings[bname].add_reading(row['timestamp'], row['kwh'])

# Initialize OOP manager
manager = BuildingManager()
manager.load_from_dataframe(df_combined)



fig, axs = plt.subplots(3, 1, figsize=(12, 14))

# LINE CHART — Daily Trend for all buildings
for bname in df_daily['building'].unique():
    bdata = df_daily[df_daily['building'] == bname]
    axs[0].plot(bdata['timestamp'], bdata['kwh'], label=bname)
axs[0].set_title("Daily Electricity Consumption")
axs[0].set_ylabel("kWh")
axs[0].legend()

# BAR CHART — Weekly averages per building
weekly_avg = df_weekly.groupby('building')['kwh'].mean()
axs[1].bar(weekly_avg.index, weekly_avg.values, color='orange')
axs[1].set_title("Average Weekly Usage (kWh)")
axs[1].set_ylabel("kWh")

# SCATTER PLOT — Peak hour distribution
axs[2].scatter(df_combined['timestamp'], df_combined['kwh'], s=10, alpha=0.5)
axs[2].set_title("Scatter Plot – All Hourly Readings")
axs[2].set_xlabel("Timestamp")
axs[2].set_ylabel("kWh")

plt.tight_layout()
plt.savefig("dashboard.png")
plt.close()

print("\nDashboard saved as dashboard.png")



# Create output folder
os.makedirs("output", exist_ok=True)

df_combined.to_csv("output/cleaned_energy_data.csv", index=False)
building_summary.to_csv("output/building_summary.csv")

# Executive summary
total_campus = building_summary['total_kwh'].sum()
highest_building = building_summary['total_kwh'].idxmax()
peak_load = df_combined.loc[df_combined['kwh'].idxmax()]

summary_text = f"""
CAMPUS ENERGY SUMMARY REPORT
----------------------------------------
Total Campus Consumption (kWh): {total_campus}

Highest Consuming Building: {highest_building}
Total Energy Usage: {building_summary.loc[highest_building,'total_kwh']} kWh

Peak Load Time: {peak_load['timestamp']}
Peak Load Value: {peak_load['kwh']} kWh

Daily and weekly trends charts saved in dashboard.png
Cleaned data saved in output/cleaned_energy_data.csv
Building summary saved in output/building_summary.csv
"""

with open("output/summary.txt", "w") as f:
    f.write(summary_text)

print("\nSummary report generated at output/summary.txt")
print("\nCapstone project completed successfully!")