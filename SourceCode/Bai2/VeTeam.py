import pandas as pd
import matplotlib.pyplot as plt

# Load player statistics from the CSV file
df = pd.read_csv("results.csv")

# Columns to exclude from numerical processing
skip_headers = ['Player', 'Nation', 'Squad', 'Pos']

# Replace invalid values labeled as "N/a" with 0.00
df.replace("N/a", 0.00, inplace=True)

# Function to normalize age from the "years-days" format to float (e.g., "20-200" → 20.55)
def normalize_age(age_str):
    try:
        if isinstance(age_str, str) and '-' in age_str:
            y, d = map(int, age_str.split('-'))
            return round(y + d / 365, 2)
        return float(age_str)
    except:
        return 0.0

# Normalize the 'Age' column if it exists in the dataset
if 'Age' in df.columns:
    df['Age'] = df['Age'].apply(normalize_age)

# Convert all numeric columns to float, excluding non-numeric identifiers
for col in df.columns:
    if col not in skip_headers:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

# Identify numeric columns to be used in plotting
numeric_columns = [col for col in df.columns if col not in skip_headers]

# Get the list of all unique teams from the 'Squad' column
teams = sorted(df['Squad'].dropna().unique())

# For each team, generate a histogram for every numeric statistic
for team in teams:
    team_df = df[df['Squad'] == team]
    print(f"Team: {team} - Number of players: {len(team_df)}")

    for col in numeric_columns:
        values = team_df[col].dropna()
        if values.nunique() <= 1:
            continue  # Skip columns with no variation in data

        # Plot histogram for the current team's statistic
        plt.figure(figsize=(8, 5))
        plt.hist(values, bins=10, alpha=0.75, color='steelblue', edgecolor='black')
        plt.title(f"{team} - Distribution of: {col}")
        plt.xlabel(col)
        plt.ylabel("Number of Players")
        plt.tight_layout()
        plt.show()
