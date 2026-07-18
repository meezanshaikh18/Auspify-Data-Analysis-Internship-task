import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('Dataset.csv')

# ---- STEP 1: Extract and clean country information ----

# Check how many rows have missing country values
print("Missing country values:", df['country'].isna().sum())

# Drop rows with no country info (only for this country-based analysis)
df_country = df.dropna(subset=['country']).copy()

# Split multi-country cells like "United States, India" into a list
df_country['country'] = df_country['country'].str.split(', ')

# Explode: turn each country in the list into its own row
df_exploded = df_country.explode('country')

# Remove any leading/trailing spaces
df_exploded['country'] = df_exploded['country'].str.strip()

print("Rows before exploding:", len(df_country))
print("Rows after exploding:", len(df_exploded))


# ---- STEP 2: Calculate content count by country ----
country_counts = df_exploded['country'].value_counts()

print("\nTotal unique countries:", country_counts.shape[0])
print("\nTop 15 countries by content count:")
print(country_counts.head(15))


# ---- STEP 3: Identify top content-producing countries ----

# Remove "Not Given" - it's a placeholder, not a real country
country_counts_clean = country_counts.drop('Not Given', errors='ignore')

# Get top 10 countries
top_10_countries = country_counts_clean.head(10)

print("\nTop 10 content-producing countries (excluding 'Not Given'):")
print(top_10_countries)

# Calculate each top country's share of total content
total_content = country_counts_clean.sum()
top_10_share = (top_10_countries / total_content * 100).round(2)

print("\nTop 10 countries - % share of total content:")
print(top_10_share)


# ---- STEP 4: Create charts and rankings ----

import os
os.makedirs('output', exist_ok=True)

sns.set_style("whitegrid")

# --- Chart 1: Bar chart of top 10 countries ---
plt.figure(figsize=(10, 6))
sns.barplot(x=top_10_countries.values, y=top_10_countries.index, palette="viridis")
plt.title("Top 10 Netflix Content-Producing Countries", fontsize=14, fontweight='bold')
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig('output/top_10_countries_bar.png', dpi=150)
plt.show()

# --- Chart 2: Pie chart of top 10 share ---
plt.figure(figsize=(8, 8))
plt.pie(top_10_countries.values, labels=top_10_countries.index, autopct='%1.1f%%', startangle=90)
plt.title("Top 10 Countries - Share of Netflix Content", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/top_10_countries_pie.png', dpi=150)
plt.show()

print("\nCharts saved in the 'output' folder.")


# ---- STEP 5: Generate business insights ----

print("\n" + "="*50)
print("BUSINESS INSIGHTS - COUNTRY-WISE CONTENT ANALYSIS")
print("="*50)

print(f"\n1. Netflix content spans {country_counts_clean.shape[0]} countries.")
print(f"2. The United States is the dominant content source, contributing "
      f"{top_10_share['United States']}% of all titles.")
print(f"3. India is the second-largest contributor at {top_10_share['India']}%, "
      f"reflecting Netflix's strong investment in the Indian market.")
print(f"4. The top 3 countries (US, India, UK) together account for "
      f"{top_10_share[:3].sum():.2f}% of total content.")
print(f"5. The remaining {country_counts_clean.shape[0]-10} countries contribute "
      f"the rest, showing a 'long tail' of smaller international content sources.")