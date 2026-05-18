import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, ShuffleSplit, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import warnings
warnings.filterwarnings("ignore")

# ── 1. Load cleaned data ──────────────────────────────────────
df = pd.read_csv("Data/cleaned_data.csv")
print(f"✅ Data loaded! Shape: {df.shape}")

# ── 2. Add price_per_sqft as extra feature ───────────────────
# This is the most powerful real estate feature
df["price_per_sqft"] = df["price"] * 100000 / df["total_sqft"]

# ── 3. Log-transform price ────────────────────────────────────
# Real estate prices are "skewed" — log makes them more normal
# This dramatically helps regression models
df["log_price"] = np.log1p(df["price"])

# ── 4. One-Hot Encode locations ───────────────────────────────
df_encoded = pd.get_dummies(df, columns=["location"], drop_first=True)
print(f"✅ Encoded! Total columns: {df_encoded.shape[1]}")

# ── 5. Features and Target ────────────────────────────────────
# Drop original price and log_price from features
drop_cols = ["price", "log_price", "price_per_sqft"]
X = df_encoded.drop(columns=drop_cols)
y = df_encoded["log_price"]  # ← predicting log(price), convert back later

print(f"\n📊 Features used: {X.shape[1]}")
print(f"   → total_sqft, bath, bhk + {X.shape[1]-3} location columns")

# ── 6. Split data ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

print(f"\n✅ Split: {X_train.shape[0]} train | {X_test.shape[0]} test")

# ── 7. Compare Models ─────────────────────────────────────────
print(f"\n⏳ Comparing models (this takes ~15 seconds)...")

models = {
    "Linear Regression"   : LinearRegression(),
    "Random Forest"       : RandomForestRegressor(
                                n_estimators=200,
                                max_depth=15,
                                min_samples_split=5,
                                random_state=42),
    "Gradient Boosting"   : GradientBoostingRegressor(
                                n_estimators=200,
                                learning_rate=0.1,
                                max_depth=5,
                                random_state=42)
}

best_model = None
best_score = -999
best_name  = ""

for name, m in models.items():
    cv     = ShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
    scores = cross_val_score(m, X, y, cv=cv, scoring="r2")
    avg    = scores.mean()
    print(f"\n   {name}")
    print(f"   CV R² : {scores.round(2)} → Avg: {avg:.2f}")
    if avg > best_score:
        best_score = avg
        best_model = m
        best_name  = name

print(f"\n🏆 Best Model: {best_name} (CV R² = {best_score:.2f})")

# ── 8. Train & Evaluate Best Model ───────────────────────────
print(f"\n⏳ Training final {best_name}...")
best_model.fit(X_train, y_train)

# Predict and convert back from log scale
y_pred_log = best_model.predict(X_test)
y_pred     = np.expm1(y_pred_log)      # reverse of log1p
y_actual   = np.expm1(y_test)

r2  = r2_score(y_actual, y_pred)
mae = mean_absolute_error(y_actual, y_pred)

print(f"\n📈 Final Performance (in actual Lakhs):")
print(f"   R² Score       : {r2:.2f}")
print(f"   Mean Abs Error : ₹{mae:.2f} Lakhs")
print(f"   (Predictions off by ₹{mae:.2f}L on average)")

# ── 9. Test Prediction ────────────────────────────────────────
print(f"\n🏠 Test: Whitefield | 1500 sqft | 2 bath | 3 BHK")
test_row = pd.DataFrame(
    columns=X.columns,
    data=np.zeros((1, len(X.columns))))

test_row["total_sqft"] = 1500
test_row["bath"]       = 2
test_row["bhk"]        = 3

loc_col = "location_Whitefield"
if loc_col in test_row.columns:
    test_row[loc_col] = 1

pred_log  = best_model.predict(test_row)[0]
predicted = np.expm1(pred_log)
print(f"   Predicted Price: ₹{predicted:.2f} Lakhs")

# ── 10. Save everything ───────────────────────────────────────
pickle.dump(best_model,                     open("model.pkl",    "wb"))
pickle.dump(list(X.columns),               open("columns.pkl",  "wb"))
pickle.dump(list(df["location"].unique()), open("locations.pkl","wb"))

print(f"\n🎉 All files saved!")
print(f"   model.pkl | columns.pkl | locations.pkl")