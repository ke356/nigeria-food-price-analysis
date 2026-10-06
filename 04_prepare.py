import pandas as pd

df = pd.read_csv("data/cleaned_food_prices.csv", parse_dates=["date"])
print("Rows at start:", len(df))

# 1. Keep retail prices only (what a normal buyer pays)
df = df[df["pricetype"] == "Retail"].copy()
print("Rows after keeping Retail:", len(df))

# 2. Split the unit text into a number and a measure
# "2.7 KG" -> 2.7 and "KG" | "KG" -> (no number) and "KG" | "100 L" -> 100 and "L"
parts = df["unit"].str.strip().str.upper().str.extract(r"^([\d.]*)\s*(KG|L)$")
df["quantity"] = pd.to_numeric(parts[0].replace("", "1"), errors="coerce")
df["measure"] = parts[1].map({"KG": "kg", "L": "litre"})

# 3. Drop units we can't convert (for example "100 Tubers")
bad = df[df["quantity"].isna()]
print("Rows dropped (unit can't be converted):", len(bad))
print(bad["unit"].value_counts().head(10))
df = df.dropna(subset=["quantity"])

# 4. Price per 1 KG (or per 1 litre)
df["price_per_unit"] = df["price"] / df["quantity"]
df["usd_per_unit"] = df["usdprice"] / df["quantity"]

# 5. Sanity check
print("\nMedian price per unit by commodity:")
print(df.groupby(["commodity", "measure"])["price_per_unit"].median().round(0))

df.to_csv("data/analysis_ready.csv", index=False)
print("\nSaved data/analysis_ready.csv with", len(df), "rows")
