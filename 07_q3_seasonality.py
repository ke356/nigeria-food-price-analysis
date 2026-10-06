import os
import calendar
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("data/analysis_ready.csv", parse_dates=["date"])

COMMODITIES = ["Maize (white)", "Millet", "Sorghum", "Rice (local)", "Beans (white)"]
FIRST_YEAR, LAST_YEAR = 2017, 2025

d = df[(df["measure"] == "kg")
& (df["commodity"].isin(COMMODITIES))
& (df["year"].between(FIRST_YEAR, LAST_YEAR))].copy()
d["month_start"] = d["date"].dt.to_period("M").dt.to_timestamp()

# 1. National median price per KG for every month (rows = months, columns = commodities)
monthly = (d.groupby(["month_start", "commodity"])["price_per_unit"]
.median().unstack("commodity"))
monthly = monthly.asfreq("MS") # make sure every month exists
monthly = monthly.interpolate(limit=2) # fill gaps of up to 2 months

# 2. Trend = centred 2x12 moving average of LOG prices.
# Logs matter: prices grow by a percentage each year, and logs turn that
# into a straight line, so the moving average tracks it without bias.
log_prices = np.log(monthly)
ma12 = log_prices.rolling(window=12, center=True, min_periods=12).mean()
log_trend = (ma12 + ma12.shift(-1)) / 2 # 2x12 average = truly centred

# 3. Ratio to trend: 1.05 means 5% above trend, 0.95 means 5% below
ratio = np.exp(log_prices - log_trend)

# 4. Average the ratio by calendar month across all years
seasonal = ratio.groupby(ratio.index.month).mean()
seasonal.index = [calendar.month_abbr[m] for m in seasonal.index]

# 5. Consistency: in what % of years was that month above trend?
above = ratio.gt(1).astype(float).where(ratio.notna())
consistency = (above.groupby(above.index.month).mean() * 100).round(0)
consistency.index = seasonal.index

print("Seasonal index (1.00 = trend):")
print(seasonal.round(3))
print("\n% of years each month was above trend:")
print(consistency)

summary = pd.DataFrame({
"peak_month": seasonal.idxmax(),
"peak_%_above_trend": ((seasonal.max() - 1) * 100).round(1),
"lowest_month": seasonal.idxmin(),
"lowest_%_below_trend": ((1 - seasonal.min()) * 100).round(1),
})
print("\nSummary:")
print(summary)
seasonal.round(3).to_csv("outputs/q3_seasonal_index.csv")

# Chart
fig, ax = plt.subplots(figsize=(10, 6))
seasonal.plot(ax=ax, marker="o")
ax.axhline(1.0, color="black", linestyle="--", linewidth=1)
ax.set_title("Seasonal price pattern (1.00 = trend), retail price per KG")
ax.set_ylabel("Seasonal index")
ax.set_xlabel("Month")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("outputs/q3_seasonality.png", dpi=150)
plt.close(fig)
print("\nSaved outputs/q3_seasonality.png")
