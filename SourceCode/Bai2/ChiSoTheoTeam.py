import pandas as pd

# Load player data from CSV
df = pd.read_csv('results.csv')

# Define non-statistic columns
non_stat_cols = ['Player', 'Nation', 'Squad', 'Pos']

# Identify numeric columns by attempting conversion
numeric_cols = []
for col in df.columns:
    if col in non_stat_cols:
        continue
    try:
        pd.to_numeric(df[col].replace('N/a', 0.0), errors='raise')
        numeric_cols.append(col)
    except Exception:
        continue

# Clean and convert numeric columns
df[numeric_cols] = df[numeric_cols].replace('N/a', 0.0).astype(float)

# Calculate average stats per team
squad_avg = df.groupby('Squad')[numeric_cols].mean(numeric_only=True)

# Save to output CSV
output_path = 'ChiSoTeam.csv'
squad_avg.to_csv(output_path, encoding='utf-8-sig')

print(f"✅ Saved average team stats to {output_path}")
