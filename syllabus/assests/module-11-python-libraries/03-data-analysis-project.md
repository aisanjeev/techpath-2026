# Data Analysis — Complete IPL Project with Pandas

**Module 11 — Python Libraries | Real-World Data Project**

---

## Why This Matters

> "Python Developer" and "Python + Data Analysis Developer" are two different salaries. The second one pays Rs 15,000-25,000 more per year. This project teaches you to analyze real data, make charts, and present insights — the skills that create that salary gap.

---

## Project: IPL Cricket Data Analysis

We'll analyze IPL match data and build insights — the kind of work data analysts do at companies like Dream11, CRED, and Swiggy.

### Step 1: Setup

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (12, 6)
matplotlib.rcParams['font.size'] = 12
```

### Step 2: Create Sample Dataset

```python
# In real work, you'd read from CSV: pd.read_csv("ipl_data.csv")
# Here we create sample data for practice

data = {
    "match_id": list(range(1, 21)),
    "season": [2023]*10 + [2024]*10,
    "team1": ["CSK","MI","RCB","KKR","DC","CSK","MI","RCB","KKR","DC",
              "CSK","MI","RCB","KKR","DC","CSK","MI","RCB","KKR","DC"],
    "team2": ["MI","RCB","KKR","DC","CSK","RCB","KKR","DC","CSK","MI",
              "MI","RCB","KKR","DC","CSK","RCB","KKR","DC","CSK","MI"],
    "winner": ["CSK","MI","RCB","KKR","CSK","CSK","KKR","RCB","CSK","MI",
               "MI","MI","RCB","DC","CSK","CSK","MI","KKR","CSK","DC"],
    "city": ["Chennai","Mumbai","Bangalore","Kolkata","Delhi",
             "Chennai","Mumbai","Bangalore","Kolkata","Delhi"]*2,
    "toss_winner": ["CSK","RCB","RCB","KKR","DC","CSK","MI","DC","CSK","MI",
                    "MI","MI","KKR","DC","DC","RCB","MI","RCB","KKR","DC"],
    "player_of_match": ["Dhoni","Rohit","Kohli","Russell","Pant",
                         "Jadeja","Bumrah","Faf","Iyer","SKY",
                         "Rohit","Hardik","Maxwell","Narine","Axar",
                         "Gaikwad","Surya","Kohli","Russell","Pant"],
    "team1_score": [185,167,203,178,156,192,145,210,168,177,
                    198,155,187,201,172,189,211,176,195,163],
    "team2_score": [170,172,195,162,148,188,152,198,173,169,
                    205,148,190,195,168,182,203,181,188,170],
    "venue": ["Chepauk","Wankhede","Chinnaswamy","Eden Gardens","Arun Jaitley",
              "Chepauk","Wankhede","Chinnaswamy","Eden Gardens","Arun Jaitley"]*2
}

df = pd.DataFrame(data)
print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print(df.head())
```

### Step 3: Explore the Data

```python
# Basic info
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Unique values
print(f"Seasons: {df['season'].unique()}")
print(f"Teams: {df['winner'].unique()}")
print(f"Cities: {df['city'].nunique()} unique cities")
```

### Step 4: Analysis & Insights

#### Insight 1: Which team wins the most?

```python
wins = df['winner'].value_counts()
print("Total Wins:")
print(wins)

# Chart
colors = ['#FFD700', '#004BA0', '#E42E2E', '#3A225D', '#0078BC']
wins.plot(kind='bar', color=colors, edgecolor='black', linewidth=0.5)
plt.title('Total Wins by Team', fontweight='bold', fontsize=16)
plt.xlabel('Team')
plt.ylabel('Wins')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('wins_by_team.png', dpi=150)
plt.show()
```

> 🖼️ **IMAGE:** A bar chart showing IPL team wins — CSK with the most wins in gold color, MI in blue, RCB in red, KKR in purple, DC in blue — clean design with team abbreviations on x-axis, title "Total Wins by Team"
> `ipl-wins-by-team-chart.png`

#### Insight 2: Does winning the toss help?

```python
# Compare toss winner vs match winner
df['toss_win_match_win'] = df['toss_winner'] == df['winner']
toss_impact = df['toss_win_match_win'].value_counts()

percentage = (toss_impact[True] / len(df)) * 100
print(f"Toss winner won the match: {percentage:.1f}% of the time")

# Pie chart
labels = ['Toss Winner Won', 'Toss Winner Lost']
sizes = [toss_impact[True], toss_impact[False]]
colors_pie = ['#22c55e', '#ef4444']

plt.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 14})
plt.title('Does Winning the Toss Help?', fontweight='bold', fontsize=16)
plt.tight_layout()
plt.savefig('toss_impact.png', dpi=150)
plt.show()
```

#### Insight 3: Average scores by venue

```python
# Combine both team scores for each venue
venue_scores = df.groupby('venue')[['team1_score', 'team2_score']].mean()
venue_scores['avg_total'] = (venue_scores['team1_score'] + venue_scores['team2_score']) / 2

venue_scores['avg_total'].sort_values().plot(
    kind='barh', color='#6366f1', edgecolor='black', linewidth=0.5
)
plt.title('Average Score by Venue', fontweight='bold')
plt.xlabel('Average Score')
plt.tight_layout()
plt.savefig('scores_by_venue.png', dpi=150)
plt.show()
```

#### Insight 4: Season-wise performance comparison

```python
season_wins = df.groupby(['season', 'winner']).size().unstack(fill_value=0)
season_wins.plot(kind='bar', width=0.8)
plt.title('Wins by Team — Season Comparison', fontweight='bold')
plt.xlabel('Season')
plt.ylabel('Wins')
plt.legend(title='Team', bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('season_comparison.png', dpi=150)
plt.show()
```

#### Insight 5: Player of the Match leaderboard

```python
top_players = df['player_of_match'].value_counts().head(5)

top_players.plot(kind='barh', color=['#FFD700', '#C0C0C0', '#CD7F32', '#6366f1', '#64748b'])
plt.title('Most Player of the Match Awards', fontweight='bold')
plt.xlabel('Awards')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top_players.png', dpi=150)
plt.show()
```

### Step 5: Generate the Report

```python
# Create a summary report
report = f"""
{'='*50}
       IPL DATA ANALYSIS REPORT
{'='*50}

Period: {df['season'].min()} - {df['season'].max()}
Total Matches Analyzed: {len(df)}

KEY FINDINGS:
─────────────
1. Most Successful Team: {df['winner'].value_counts().index[0]} ({df['winner'].value_counts().values[0]} wins)

2. Toss Impact: Toss winner won {percentage:.1f}% of matches
   → {'Significant advantage' if percentage > 55 else 'Minimal advantage'}

3. Highest Scoring Venue: {venue_scores['avg_total'].idxmax()} (Avg: {venue_scores['avg_total'].max():.0f})

4. Top Performer: {df['player_of_match'].value_counts().index[0]} ({df['player_of_match'].value_counts().values[0]} awards)

5. Average Match Score: {df[['team1_score', 'team2_score']].values.mean():.0f}

RECOMMENDATIONS:
────────────────
• Teams should focus on batting when playing at {venue_scores['avg_total'].idxmax()}
• Toss {'matters significantly' if percentage > 55 else 'has limited impact'} — strategy matters more
• {df['winner'].value_counts().index[0]} shows the most consistent performance

{'='*50}
"""

print(report)

# Save report to file
with open("ipl_analysis_report.txt", "w") as f:
    f.write(report)

print("Report saved to ipl_analysis_report.txt")
```

---

## Skills This Project Proves in an Interview

| Skill | What You Did |
|-------|-------------|
| **Data loading** | Created/loaded DataFrame |
| **Data exploration** | .info(), .describe(), .isnull() |
| **Data cleaning** | Handled missing values, data types |
| **Aggregation** | groupby, value_counts, mean |
| **Visualization** | Bar, pie, horizontal bar charts |
| **Insight extraction** | Drew business conclusions from data |
| **Report generation** | Formatted text report with findings |
| **File I/O** | Saved charts as PNG, report as TXT |

---

## Alternative Project Ideas (Pick One and Build)

| Project | Data Source | Analysis |
|---------|------------|----------|
| **E-commerce Sales** | Create CSV with 1000 orders | Revenue trends, top products, customer segments |
| **Student Performance** | Create CSV with 200 students | Subject-wise analysis, pass/fail patterns |
| **Weather Data** | Download from Kaggle | Temperature trends, rainfall patterns |
| **Movie Ratings** | IMDB dataset (Kaggle) | Genre popularity, rating distribution |
| **COVID Data** | India COVID data (public) | State-wise trends, recovery rates |
