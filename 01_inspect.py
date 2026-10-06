import pandas as pd

path = "data/raw/data/wfp_food_prices_nga.csv"
df = pd.read_csv(path, skiprows=[1]) # skip the HXL tag row
df["date"] = pd.to_datetime(df["date"])

print("Shape:", df.shape)
print("\nDate range:", df["date"].min(), "to", df["date"].max())
print("\nColumns and types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isna().sum())
print("\nCategories:")
print(df["category"].value_counts())
print("\nTop 15 commodities:")
print(df["commodity"].value_counts().head(15))
print("\nStates:", df["admin1"].nunique())
print("Markets:", df["market"].nunique())
print("\nPrice types:")
print(df["pricetype"].value_counts())
print("\nSample rows:")
print(df.head(10))