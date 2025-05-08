import pandas as pd
import numpy as np
import csv
import sys

# Ensure CSV field size limit can handle large fields
max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)

# Reading the data from 'results.csv'
print("📂 Reading data from 'results.csv'...")
try:
    df = pd.read_csv('results.csv', engine='python', encoding='utf-8-sig', skip_blank_lines=True)
    # Clean up column names by removing unwanted characters
    df.columns = df.columns.str.strip().str.replace('\n', '').str.replace('\r', '')
    print(f"✅ Successfully read file with {len(df)} records and {len(df.columns)} columns.")
except Exception as e:
    print(f"❌ Error reading file: {e}")
    exit()

# List of required columns to analyze
required_headers = [
    "Age", "MP", "Starts", "Min", "Gls", "Ast", "CrdY", "CrdR", "xG", "xAG", 
    "PrgCs", "PrgPs", "PrgRs", "Gls.1", "Ast.1", "xG.1", "xAG.1", "SoT%", "SoT/90", 
    "G/Sh", "Dist", "Cmp", "Cmp%", "TotDist", "Cmp%.1", "Cmp%.2", "Cmp%.3", 
    "KP", "Pto1/3", "PPA", "CrsPA", "PrgPp", "SCA", "SCA90", "GCA", "GCA90", 
    "Tkl", "TklW", "Attd", "Lostd", "Blocks", "Sh", "Pass", "Int", "Touches", 
    "Def Pen", "Def 3rd", "Mid 3rd", "Att 3rd", "Att Pen", "Attp", "Succ%", 
    "Tkld%", "Carries", "PrgDist", "PrgCp", "Cto1/3", "CPA", "Mis", "Dis", 
    "Rec", "PrgRp", "Fls", "Fld", "Off", "Crs", "Recov", "Won", "Lostm", 
    "Won%", "GA90", "Save%", "CS%", "Save%.1"
]

# Check if all required columns are present in the data
missing_headers = [col for col in required_headers if col not in df.columns]
if missing_headers:
    print(f"⚠️ Missing {len(missing_headers)} required headers.")
else:
    print("✅ All required headers are present.")

# Drop irrelevant columns such as 'Player', 'Nation', 'Pos'
cols_to_drop = ['Player', 'Nation', 'Pos']
df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True, errors='ignore')

# Normalize 'Age' column: converting age ranges (e.g., '22-150') into numeric values
if 'Age' in df.columns:
    print("🔄 Normalizing 'Age' column...")

    def convert_age(x):
        if pd.isna(x):
            return 0.0
        if isinstance(x, str) and '-' in x:
            try:
                years, days = map(int, x.split('-'))
                return years + days / 365  # Convert range to average age
            except:
                return 0.0
        try:
            return float(x)
        except:
            return 0.0

    df['Age'] = df['Age'].apply(convert_age)

# Identify numeric columns in the dataset
numeric_cols = [col for col in required_headers if col in df.columns]
print(f"📊 Preparing to compute statistics for {len(numeric_cols)} columns.")

# Clean data by converting non-numeric or 'N/A' values to 0.0
print("🧹 Cleaning data (N/A → 0.0)...")
df[numeric_cols] = df[numeric_cols].apply(lambda x: pd.to_numeric(x, errors='coerce')).fillna(0.0)

# DataFrame to store calculated statistics
result_df = pd.DataFrame()

# Function to compute median, mean, and standard deviation for each metric
def calculate_stats(data, team_name):
    stats = {'Team': team_name}
    for col in numeric_cols:
        stats[f'Median of {col}'] = data[col].median()
        stats[f'Mean of {col}'] = data[col].mean()
        stats[f'Std of {col}'] = data[col].std()
    return stats

# Calculate global statistics across all players
print("🔍 Computing overall statistics...")
result_df = pd.concat([result_df, pd.DataFrame([calculate_stats(df, 'all')])], ignore_index=True)

# Calculate statistics for each team
if 'Squad' in df.columns:
    print("🏟️ Computing stats per team...")
    for team in df['Squad'].unique():
        team_df = df[df['Squad'] == team]
        team_stats = calculate_stats(team_df, team)
        result_df = pd.concat([result_df, pd.DataFrame([team_stats])], ignore_index=True)

# Save the results to a new CSV file
output_file = 'results2.csv'
print(f"💾 Saving results to '{output_file}'...")
try:
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Saved successfully with {len(result_df)} rows and {len(result_df.columns)} columns.")
except Exception as e:
    print(f"❌ Error saving file: {e}")

print("✅ Finished!")
