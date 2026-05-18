import pandas as pd
import numpy as np

# ── 1. Load raw data ──────────────────────────────────────────
df = pd.read_csv("Data/Bengaluru_House_Data.csv")
print("✅ Raw data loaded!")
print(f"   Shape: {df.shape}")
print(f"\nFirst look at data:\n{df.head()}")
print(f"\nColumn names: {list(df.columns)}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# ── 2. Drop columns we don't need ────────────────────────────
df.drop(columns=["area_type", "availability", "society", "balcony"], inplace=True)
print("\n✅ Unnecessary columns dropped!")

# ── 3. Drop rows with missing values ─────────────────────────
df.dropna(inplace=True)
print(f"✅ Missing values removed! Shape now: {df.shape}")

# ── 4. Clean the 'size' column (e.g. "2 BHK" → 2) ───────────
df["bhk"] = df["size"].apply(lambda x: int(x.split(" ")[0])
                              if str(x).split(" ")[0].isdigit() else None)
df.drop(columns=["size"], inplace=True)
df.dropna(subset=["bhk"], inplace=True)
df["bhk"] = df["bhk"].astype(int)
print("✅ BHK column cleaned!")

# ── 5. Clean 'total_sqft' (handle ranges like "1000-1200") ───
def convert_sqft(x):
    try:
        # If it's a range like "1000-1200", take the average
        if "-" in str(x):
            parts = str(x).split("-")
            return (float(parts[0]) + float(parts[1])) / 2
        return float(x)
    except:
        return None

df["total_sqft"] = df["total_sqft"].apply(convert_sqft)
df.dropna(subset=["total_sqft"], inplace=True)
print("✅ Square footage cleaned!")

# ── 6. Remove outliers ────────────────────────────────────────
# ── 6. Remove outliers (stronger version) ────────────────────
# Remove price per sqft outliers (most reliable method)
df["price_per_sqft"] = df["price"] * 100000 / df["total_sqft"]

def remove_price_outliers(df):
    cleaned = []
    for location in df["location"].unique():
        loc_df = df[df["location"] == location]
        if len(loc_df) >= 5:  # only apply to locations with enough data
            mean = loc_df["price_per_sqft"].mean()
            std  = loc_df["price_per_sqft"].std()
            loc_df = loc_df[
                (loc_df["price_per_sqft"] > mean - std) &
                (loc_df["price_per_sqft"] < mean + std)
            ]
        cleaned.append(loc_df)
    return pd.concat(cleaned, ignore_index=True)

df = remove_price_outliers(df)

# Also remove houses where bathrooms > bhk + 2 (data errors)
df = df[df["bath"] <= df["bhk"] + 2]

# Cap prices at 99th percentile (remove ultra-luxury outliers)
price_cap = df["price"].quantile(0.99)
df = df[df["price"] <= price_cap]

print(f"✅ Outliers removed! Final shape: {df.shape}")

# ── 7. Clean location names (group rare ones as 'Other') ─────
df["location"] = df["location"].apply(lambda x: x.strip())
location_counts = df["location"].value_counts()
rare_locations  = location_counts[location_counts <= 10].index
df["location"]  = df["location"].apply(
    lambda x: "Other" if x in rare_locations else x)
print(f"✅ Locations cleaned! Unique locations: {df['location'].nunique()}")

# ── 8. Save cleaned data ──────────────────────────────────────
df.to_csv("Data/cleaned_data.csv", index=False)
print(f"\n🎉 Cleaned data saved to Data/cleaned_data.csv!")
print(f"   Final shape: {df.shape}")
print(f"\nCleaned data preview:\n{df.head()}")