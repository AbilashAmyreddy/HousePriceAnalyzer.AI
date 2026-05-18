import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Load cleaned data ─────────────────────────────────────────
df = pd.read_csv("Data/cleaned_data.csv")
print(f"✅ Data loaded! Shape: {df.shape}")
print(f"\nBasic Statistics:\n{df.describe()}")

# ── Style settings ────────────────────────────────────────────
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# ══════════════════════════════════════════════════════════════
# CHART 1 — Price Distribution
# "How are house prices spread out?"
# ══════════════════════════════════════════════════════════════
plt.figure()
sns.histplot(df["price"], bins=50, kde=True, color="steelblue")
plt.title("Chart 1: House Price Distribution (in Lakhs)", fontsize=14)
plt.xlabel("Price (Lakhs)")
plt.ylabel("Number of Houses")
plt.tight_layout()
plt.savefig("Data/chart1_price_distribution.png")
plt.show()
print("✅ Chart 1 saved!")

# ══════════════════════════════════════════════════════════════
# CHART 2 — Area vs Price
# "Do bigger houses cost more?"
# ══════════════════════════════════════════════════════════════
plt.figure()
sns.scatterplot(data=df[df["price"] < 500],  # filter extreme outliers for clarity
                x="total_sqft", y="price",
                hue="bhk", palette="viridis", alpha=0.6)
plt.title("Chart 2: Area vs Price (colored by BHK)", fontsize=14)
plt.xlabel("Total Area (sqft)")
plt.ylabel("Price (Lakhs)")
plt.tight_layout()
plt.savefig("Data/chart2_area_vs_price.png")
plt.show()
print("✅ Chart 2 saved!")

# ══════════════════════════════════════════════════════════════
# CHART 3 — BHK vs Average Price
# "Which BHK type is most expensive on average?"
# ══════════════════════════════════════════════════════════════
plt.figure()
bhk_price = df.groupby("bhk")["price"].mean().reset_index()
sns.barplot(data=bhk_price, x="bhk", y="price", palette="Blues_d")
plt.title("Chart 3: Average Price by BHK", fontsize=14)
plt.xlabel("Number of BHK")
plt.ylabel("Average Price (Lakhs)")
plt.tight_layout()
plt.savefig("Data/chart3_bhk_vs_price.png")
plt.show()
print("✅ Chart 3 saved!")

# ══════════════════════════════════════════════════════════════
# CHART 4 — Correlation Heatmap
# "Which features are most related to price?"
# ══════════════════════════════════════════════════════════════
plt.figure()
corr = df[["total_sqft", "bath", "bhk", "price"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Chart 4: Correlation Heatmap", fontsize=14)
plt.tight_layout()
plt.savefig("Data/chart4_correlation.png")
plt.show()
print("✅ Chart 4 saved!")

# ══════════════════════════════════════════════════════════════
# CHART 5 — Top 10 Most Expensive Locations
# "Which areas in Bengaluru are priciest?"
# ══════════════════════════════════════════════════════════════
plt.figure(figsize=(12, 5))
top_locations = (df.groupby("location")["price"]
                   .mean()
                   .sort_values(ascending=False)
                   .head(10)
                   .reset_index())
sns.barplot(data=top_locations, x="location", y="price", palette="Reds_d")
plt.title("Chart 5: Top 10 Most Expensive Locations", fontsize=14)
plt.xlabel("Location")
plt.ylabel("Average Price (Lakhs)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("Data/chart5_top_locations.png")
plt.show()
print("✅ Chart 5 saved!")

print("\n🎉 All 5 charts generated and saved to the Data folder!")
print("These charts will also be shown inside our app later.")