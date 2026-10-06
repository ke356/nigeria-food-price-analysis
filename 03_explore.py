import pandas as pd

df = pd.read_csv("data/cleaned_food_prices.csv", parse_dates=["date"])

# 1. How far back does the data go, and how much data per year?
print("Date range:", df["date"].min(), "to", df["date"].max())
print("\nRows per year:")
print(df["year"].value_counts().sort_index())

# 2. Are prices retail, wholesale, or both?
print("\nPrice types:")
print(df["pricetype"].value_counts())

# 3. Is everything in Naira?
print("\nCurrency:")
print(df["currency"].value_counts())

# 4. Coverage: how many states and markets?
print("\nStates:", df["state"].nunique(), "| Markets:", df["market"].nunique())

# 5. Which commodities have the most data?
print("\nTop 15 commodities:")
print(df["commodity"].value_counts().head(15))

# 6. Which units does each top commodity use?
top = df["commodity"].value_counts().head(10).index
print("\nUnits per commodity:")
print(df[df["commodity"].isin(top)].groupby(["commodity", "unit"]).size())

# 7. Sanity check on prices
print("\nPrice summary:")
print(df["price"].describe())
print("Rows with price <= 0:", (df["price"] <= 0).sum())
