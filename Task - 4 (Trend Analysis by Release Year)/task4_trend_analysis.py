import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("Dataset.csv")

# Quick check
print(df.shape)
print(df.head())
print(df['release_year'].describe())

# Organize by release year — sort and check range
df = df.sort_values('release_year')
print("Year range:", df['release_year'].min(), "-", df['release_year'].max())


# Step 2: Calculate yearly content releases
yearly_counts = df.groupby('release_year').size().reset_index(name='count')
print(yearly_counts.tail(15))  # most recent years are usually most interesting

# Optional: split by type (Movie vs TV Show) too — useful for later steps
yearly_by_type = df.groupby(['release_year', 'type']).size().unstack(fill_value=0)
print(yearly_by_type.tail(15))


# Step 3: Identify growth and decline trends

# Year-over-year % change in total releases
yearly_counts['pct_change'] = yearly_counts['count'].pct_change() * 100
print(yearly_counts.tail(15))

# Peak year
peak_year = yearly_counts.loc[yearly_counts['count'].idxmax()]
print("\nPeak release year:", int(peak_year['release_year']), "with", int(peak_year['count']), "titles")

# Recent trend (last 5 years, excluding partial 2021 if needed)
recent = yearly_counts[yearly_counts['release_year'] >= 2017]
print("\nRecent years trend:\n", recent)

# Growth phase vs decline phase (simple rule: compare each year to previous)
yearly_counts['trend'] = yearly_counts['pct_change'].apply(
    lambda x: 'Growth' if x > 0 else ('Decline' if x < 0 else 'Flat')
)
print("\n", yearly_counts.tail(10)[['release_year', 'count', 'pct_change', 'trend']])



# Step 4: Create trend visualizations

sns.set_style("whitegrid")

# --- Chart 1: Overall yearly trend (line chart) ---
plt.figure(figsize=(12, 6))
plt.plot(yearly_counts['release_year'], yearly_counts['count'], marker='o', color='#E50914', linewidth=2)
plt.axvline(x=2018, color='gray', linestyle='--', alpha=0.6, label='Peak Year (2018)')
plt.title('Netflix Content Releases by Year (1925–2021)', fontsize=14, fontweight='bold')
plt.xlabel('Release Year')
plt.ylabel('Number of Titles')
plt.legend()
plt.tight_layout()
plt.savefig('output/charts/yearly_trend.png', dpi=150)
plt.show()

# --- Chart 2: Recent years trend (zoomed in, more readable) ---
recent_plot = yearly_counts[yearly_counts['release_year'] >= 2007]
plt.figure(figsize=(12, 6))
plt.plot(recent_plot['release_year'], recent_plot['count'], marker='o', color='#E50914', linewidth=2)
plt.title('Netflix Content Releases (2007–2021)', fontsize=14, fontweight='bold')
plt.xlabel('Release Year')
plt.ylabel('Number of Titles')
plt.xticks(recent_plot['release_year'], rotation=45)
plt.tight_layout()
plt.savefig('output/charts/recent_trend.png', dpi=150)
plt.show()

# --- Chart 3: Movie vs TV Show trend (grouped) ---
yearly_by_type_recent = yearly_by_type[yearly_by_type.index >= 2007]
yearly_by_type_recent.plot(kind='bar', stacked=False, figsize=(14, 6), color=['#E50914', '#221f1f'])
plt.title('Movies vs TV Shows Released by Year (2007–2021)', fontsize=14, fontweight='bold')
plt.xlabel('Release Year')
plt.ylabel('Number of Titles')
plt.legend(title='Type')
plt.tight_layout()
plt.savefig('output/charts/movie_vs_tvshow_trend.png', dpi=150)
plt.show()

print("\nCharts saved to output/charts/")



# Step 5: Interpret business patterns

summary = f"""
NETFLIX CONTENT TREND ANALYSIS - SUMMARY
==========================================

1. Overall Growth Pattern:
   - Content releases were minimal before 2000, then grew sharply from 2007 onward.
   - Titles grew from just {yearly_counts[yearly_counts.release_year==2007]['count'].values[0]} in 2007
     to a peak of {int(peak_year['count'])} in {int(peak_year['release_year'])} — 
     roughly a 13x increase in 11 years.

2. Peak & Decline:
   - {int(peak_year['release_year'])} was the peak year for content releases.
   - From 2019–2021, releases declined year-over-year (-10.1%, -7.5%, -37.9%).
   - The 2021 drop is sharp partly because the dataset likely doesn't capture 
     the full year (data collection cutoff mid-2021).

3. Movies vs TV Shows:
   - Movies have historically dominated Netflix's catalog.
   - However, TV Shows grew faster in recent years: TV Show releases rose from 
     14 (2007) to 436 (2020), while Movies fell from a 2017 high of 767 down to 
     277 by 2021.
   - This suggests a strategic shift toward TV Show content in recent years, 
     likely due to higher viewer retention/binge-watching value.

4. Business Insight:
   - Netflix's aggressive content expansion (2015-2018) aligns with its global 
     subscriber growth push during that period.
   - The recent slowdown may reflect a shift toward quality over quantity, 
     tighter content budgets, or incomplete recent-year data.
   - The rising TV Show share indicates increasing investment in serialized 
     content to boost engagement and reduce churn.
"""

print(summary)

with open('output/summary.txt', 'w') as f:
    f.write(summary)

print("Summary saved to output/summary.txt")