import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("data/analysis_ready.csv", parse_dates=["date"])

STAPLES = ["Rice (imported)", "Rice (local)", "Maize (white)", "Millet",
"Sorghum", "Beans (white)", "Beans (red)", "Yam", "Groundnuts"]
FIRST_YEAR, LAST_YEAR = 2017, 2025

# Keep: price per KG, our staples, full years only
d = df[(df["measure"] == "kg")
& (df["commodity"].isin(STAPLES))
& (df["year"].between(FIRST_YEAR, LAST_YEAR))]

# Coverage check: rows per commodity per year
print("Rows per commodity per year:")
print(d.pivot_table(index="commodity", columns="year", values="price", aggfunc="count"))

# Yearly median price per KG (rows = years, columns = commodities)
ngn = d.pivot_table(index="year", columns="commodity", values="price_per_unit", aggfunc="median")
usd = d.pivot_table(index="year", columns="commodity", values="usd_per_unit", aggfunc="median")

# Index: first year = 100, so different commodities can share one chart
price_index = ngn / ngn.loc[FIRST_YEAR] * 100
basket = price_index.mean(axis=1) # average of all staples
basket_change = basket.loc[LAST_YEAR] - 100

summary = pd.DataFrame({
f"naira_{FIRST_YEAR}": ngn.loc[FIRST_YEAR],
f"naira_{LAST_YEAR}": ngn.loc[LAST_YEAR],
"naira_change_%": (ngn.loc[LAST_YEAR] / ngn.loc[FIRST_YEAR] - 1) * 100,
"usd_change_%": (usd.loc[LAST_YEAR] / usd.loc[FIRST_YEAR] - 1) * 100,
})
summary["vs_basket_pts"] = summary["naira_change_%"] - basket_change
summary = summary.sort_values("naira_change_%", ascending=False).round(1)

print("\nBasket average change:", round(basket_change, 1), "%")
print("\nPrice change per KG, sorted fastest to slowest:")
print(summary)
summary.to_csv("outputs/q1_price_change_summary.csv")

# Chart
fig, ax = plt.subplots(figsize=(10, 6))
price_index.plot(ax=ax, marker="o", linewidth=1.5)
basket.plot(ax=ax, color="black", linestyle="--", linewidth=3, label="Basket average")
ax.set_title(f"Staple food prices in Nigeria, retail price per KG ({FIRST_YEAR} = 100)")
ax.set_ylabel("Price index")
ax.set_xlabel("Year")
ax.legend(fontsize=8, ncol=2)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("outputs/q1_price_index.png", dpi=150)
plt.close(fig)
print("\nSaved outputs/q1_price_index.png")
