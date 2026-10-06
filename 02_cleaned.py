import pandas as pd

path = "data/raw/data/wfp_food_prices_nga.csv" # use your working path
df = pd.read_csv(path, skiprows=[1])
df["date"] = pd.to_datetime(df["date"])

# Keep only the columns we need
df = df[["date", "admin1", "market", "category", "commodity",
"unit", "pricetype", "currency", "price", "usdprice"]]

# Rename for clarity
df = df.rename(columns={"admin1": "state"})

# Remove duplicates and rows with no price
df = df.drop_duplicates()
df = df.dropna(subset=["price"])

# Time features for later analysis
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# Check the result
print(df.shape)
print(df.isna().sum())
print(df.groupby("commodity")["price"].count().sort_values(ascending=False).head(15))

# Save the cleaned file
df.to_csv("data/cleaned_food_prices.csv", index=False)