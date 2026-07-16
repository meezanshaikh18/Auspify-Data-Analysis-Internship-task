import pandas as pd

# ==========================================
# Task 1: Netflix Data Cleaning & Preparation
# ==========================================

# Step 1: Load the dataset
df = pd.read_csv("Dataset.csv")

print("=" * 50)
print("NETFLIX DATA CLEANING")
print("=" * 50)

print(f"\nDataset Shape: {df.shape}")

print("\nFirst 5 Rows:")
print(df.head())

# ==========================================
# Step 2: Check Missing Values
# ==========================================

print("\nMissing Values Per Column:")
print(df.isnull().sum())

# ==========================================
# Step 3: Check 'Not Given' Values
# ==========================================

print("\n'Not Given' Count Per Column:")
for col in df.columns:
    count = (df[col] == "Not Given").sum()
    if count > 0:
        print(f"{col}: {count}")

# ==========================================
# Step 4: Check Duplicate Records
# ==========================================

print("\nDuplicate Check:")
print("Fully Duplicate Rows :", df.duplicated().sum())
print("Duplicate show_id    :", df["show_id"].duplicated().sum())

# Remove duplicate rows (if any)
df.drop_duplicates(inplace=True)

# ==========================================
# Step 5: Handle Missing Values
# ==========================================

# Replace "Not Given" with "Unknown"
df.replace("Not Given", "Unknown", inplace=True)

# Replace actual missing values (NaN)
df.fillna("Unknown", inplace=True)

# ==========================================
# Step 6: Standardize Data
# ==========================================

# Remove extra spaces
text_columns = ["country", "rating", "type"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# Standardize Country
df["country"] = df["country"].str.title()

# Standardize Rating
df["rating"] = df["rating"].str.upper()

# Standardize Type while preserving "TV Show"
df["type"] = df["type"].replace({
    "TV Show": "TV Show",
    "Movie": "Movie",
    "tv show": "TV Show",
    "movie": "Movie"
})

# ==========================================
# Step 7: Split Duration Column
# ==========================================

df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(int)

df["duration_unit"] = (
    df["duration"]
    .str.extract(r"([A-Za-z]+)")
    .iloc[:, 0]
)

print("\nSample of Duration Columns:")
print(df[["type", "duration", "duration_value", "duration_unit"]].head())

# ==========================================
# Step 8: Verify Cleaning
# ==========================================

print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nRemaining 'Not Given' Values:")
remaining = False

for col in df.columns:
    count = (df[col] == "Not Given").sum()
    if count > 0:
        print(f"{col}: {count}")
        remaining = True

if not remaining:
    print("No 'Not Given' values remaining.")

print(f"\nFinal Dataset Shape: {df.shape}")

# ==========================================
# Step 9: Export Cleaned Dataset
# ==========================================

df.to_csv("Netflix_Cleaned.csv", index=False)

print("\n✅ Cleaned dataset exported successfully as 'Netflix_Cleaned.csv'")

print("\nTask 1 Completed Successfully!")