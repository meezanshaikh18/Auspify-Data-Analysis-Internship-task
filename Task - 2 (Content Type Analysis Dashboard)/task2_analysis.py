import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_csv("Dataset.csv")

# Quick check
print("Dataset shape:", df.shape)
print(df.head())

# Step 2: Count Movies vs TV Shows
content_counts = df["type"].value_counts()
print("\nContent Type Counts:")
print(content_counts)

content_percent = df["type"].value_counts(normalize=True) * 100
print("\nContent Type Percentages:")
print(content_percent.round(2))


# Step 3: Bar chart of content distribution
colors = ["#E50914", "#221F1F"]  # Netflix red & black

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(content_counts.index, content_counts.values, color=colors, width=0.5)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 40, f"{height:,}",
            ha="center", va="bottom", fontsize=11, fontweight="bold")

ax.set_title("Netflix Content Distribution: Movies vs TV Shows", fontsize=14, fontweight="bold")
ax.set_xlabel("Content Type")
ax.set_ylabel("Number of Titles")
ax.set_ylim(0, max(content_counts.values) * 1.15)

plt.tight_layout()
plt.savefig("content_type_bar_chart.png")
plt.show()


# Pie chart of content proportions
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(
    content_counts.values,
    labels=content_counts.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=90,
    explode=[0.03] * len(content_counts),
    textprops={"fontsize": 12, "fontweight": "bold", "color": "white"},
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
)
ax.set_title("Proportion of Movies vs TV Shows on Netflix", fontsize=14, fontweight="bold")

plt.tight_layout()
plt.savefig("content_type_pie_chart.png")
plt.show()


# Step 4: Compare content proportions
n_movies = content_counts.get("Movie", 0)
n_tvshows = content_counts.get("TV Show", 0)
ratio = n_movies / n_tvshows

print(f"\nMovie-to-TV Show ratio: {ratio:.2f} : 1")


# Step 5: Summarize key findings
total_titles = len(df)

summary_lines = [
    "TASK 2 - CONTENT TYPE ANALYSIS DASHBOARD",
    "=" * 45,
    f"Total titles analyzed: {total_titles:,}",
    f"Movies: {n_movies:,} ({content_percent.get('Movie', 0):.1f}%)",
    f"TV Shows: {n_tvshows:,} ({content_percent.get('TV Show', 0):.1f}%)",
    f"Movie-to-TV Show ratio: {ratio:.2f} : 1",
    "",
    "Key Findings:",
    f"- Movies dominate the Netflix catalog, making up {content_percent.get('Movie', 0):.1f}% of all titles.",
    f"- TV Shows account for the remaining {content_percent.get('TV Show', 0):.1f}%, showing Netflix invests",
    "  considerably less in serialized content compared to films.",
    f"- For every TV Show on the platform, there are roughly {ratio:.1f} movies.",
]

summary_text = "\n".join(summary_lines)
print("\n" + summary_text)

with open("task2_summary_findings.txt", "w") as f:
    f.write(summary_text)

print("\nSaved: task2_summary_findings.txt")