import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("weather.csv")      # <-- Replace with your dataset
print("\n===== DATA HEAD =====")
print(df.head())

print("\n===== INFO =====")
print(df.info())

print("\n===== DESCRIBE =====")
print(df.describe())


# Convert date column
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Drop missing dates
df = df.dropna(subset=['date'])

# Fill other missing values with median
df['temperature'] = df['temperature'].fillna(df['temperature'].median())
df['humidity'] = df['humidity'].fillna(df['humidity'].median())
df['rainfall'] = df['rainfall'].fillna(0)

# Filter only relevant columns
df = df[['date', 'temperature', 'humidity', 'rainfall']]


# Daily statistics already present
daily_mean = df['temperature'].mean()
daily_max = df['temperature'].max()
daily_min = df['temperature'].min()
daily_std = df['temperature'].std()

print("\n===== DAILY TEMPERATURE STATS =====")
print("Mean:", daily_mean)
print("Max:", daily_max)
print("Min:", daily_min)
print("Std Dev:", daily_std)


# Monthly & yearly grouping
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

monthly_mean = df.groupby('month')['temperature'].mean()
yearly_mean = df.groupby('year')['temperature'].mean()

print("\n===== MONTHLY MEAN TEMP =====")
print(monthly_mean)

print("\n===== YEARLY MEAN TEMP =====")
print(yearly_mean)


# ---------- Line Chart: Daily Temperature ----------
plt.figure(figsize=(10,5))
plt.plot(df['date'], df['temperature'])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.savefig("daily_temperature.png")
plt.close()

# ---------- Bar Chart: Monthly Rainfall ----------
monthly_rainfall = df.groupby('month')['rainfall'].sum()

plt.figure(figsize=(10,5))
plt.bar(monthly_rainfall.index, monthly_rainfall.values)
plt.title("Total Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.savefig("monthly_rainfall.png")
plt.close()

# ---------- Scatter Plot: Humidity vs Temperature ----------
plt.figure(figsize=(7,5))
plt.scatter(df['humidity'], df['temperature'])
plt.title("Humidity vs Temperature")
plt.xlabel("Humidity")
plt.ylabel("Temperature")
plt.savefig("humidity_vs_temp.png")
plt.close()

# ---------- Combined Plot (Line + Scatter) ----------
plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(df['date'], df['temperature'])
plt.title("Daily Temperature")

plt.subplot(2,1,2)
plt.scatter(df['humidity'], df['temperature'])
plt.title("Humidity vs Temperature")

plt.tight_layout()
plt.savefig("combined_plot.png")
plt.close()


season_map = {
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
}

df['season'] = df['month'].map(season_map)

seasonal_stats = df.groupby('season')['temperature'].mean()
print("\n===== SEASONAL MEAN TEMPERATURE =====")
print(seasonal_stats)


# Save cleaned data
df.to_csv("cleaned_weather.csv", index=False)

# Create text/markdown report
report = """
# Weather Data Visualization Report

## Key Insights
- Daily mean temperature: {:.2f}
- Highest temperature recorded: {:.2f}
- Lowest temperature recorded: {:.2f}
- Monthly mean temperatures:
{}

## Seasonal Average Temperatures
{}

## Generated Visualizations
- daily_temperature.png
- monthly_rainfall.png
- humidity_vs_temp.png
- combined_plot.png
""".format(
    daily_mean,
    daily_max,
    daily_min,
    monthly_mean.to_string(),
    seasonal_stats.to_string()
)

with open("weather_report.txt", "w") as f:
    f.write(report)

print("\n===== REPORT GENERATED: weather_report.txt =====")
print("===== CLEANED CSV SAVED: cleaned_weather.csv =====")
print("===== ALL PLOTS SAVED AS PNG FILES =====")