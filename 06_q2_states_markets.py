import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("data/analysis_ready.csv", parse_dates=["date"])

COMMODITY = "Rice (local)" # change this and rerun to test other commodities
MIN_OBS = 6 # ignore a state/market with fewer rows than this in a year
FIRST_YEAR, LAST_YEAR = 2017, 2025

d = df[(df["commodity"] == COMMODITY)
& (df["measure"] == "kg")
& (df["year"].between(FIRST_YEAR, LAST_YEAR))]

# A. Which states are most expensive in the latest year?
latest = d[d["year"] == LAST_YEAR]
state_rank = (latest.groupby("state")["price_per_unit"]
.agg(median_price="median", n="count")
.query("n >= @MIN_OBS")
.sort_values("median_price", ascending=False)
.round(0))
print(f"States ranked by median {COMMODITY} price per KG in {LAST_YEAR}:")
print(state_rank)

# B. Which markets are most and least expensive?
market_rank = (latest.groupby(["state", "market"])["price_per_unit"]
.agg(median_price="median", n="count")
.query("n >= @MIN_OBS")
.sort_values("median_price", ascending=False)
.round(0))
print("\nTop 10 most expensive markets:")
print(market_rank.head(10))
print("\n10 cheapest markets:")
print(market_rank.tail(10))

# C. Has the gap between states widened over time?
yearly_state = (d.groupby(["year", "state"])["price_per_unit"]
.agg(median_price="median", n="count")
.reset_index()
.query("n >= @MIN_OBS"))

gap = yearly_state.groupby("year")["median_price"].agg(
highest="max", lowest="min", average="mean", spread="std", n_states="count")
gap["gap_naira"] = gap["highest"] - gap["lowest"]
gap["ratio"] = gap["highest"] / gap["lowest"]
gap["variation_%"] = gap["spread"] / gap["average"] * 100

top_idx = yearly_state.groupby("year")["median_price"].idxmax()
gap["most_expensive_state"] = yearly_state.loc[top_idx].set_index("year")["state"]

print("\nGap between states over time:")
print(gap[["n_states", "highest", "lowest", "gap_naira", "ratio",
"variation_%", "most_expensive_state"]].round(2))
gap.round(2).to_csv("outputs/q2_state_gap_by_year.csv")

# Charts
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
state_rank["median_price"].sort_values().plot.barh(ax=axes[0], color="#2a6f97")
axes[0].set_title(f"{COMMODITY}: median price per KG by state, {LAST_YEAR} (NGN)")
axes[0].set_xlabel("Naira per KG")

gap["variation_%"].plot(ax=axes[1], marker="o", color="#c1121f")
axes[1].set_title("How different are state prices? (variation %)")
axes[1].set_ylabel("Variation between states (%)")
axes[1].set_xlabel("Year")
axes[1].grid(alpha=0.3)
fig.tight_layout()
fig.savefig("outputs/q2_state_prices.png", dpi=150)
plt.close(fig)
print("\nSaved outputs/q2_state_prices.png")
