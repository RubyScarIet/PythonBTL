import pandas as pd
import os
import XuLyData as XL  # Import custom data processing module

# List of all CSV files to be processed
FILE_LIST = [
    "stats_standard.csv",
    "stats_shooting.csv",
    "stats_possession.csv",
    "stats_passing.csv",
    "stats_misc.csv",
    "stats_keeper.csv",
    "stats_gca.csv",
    "stats_defense.csv",
]

# Define column rename mapping to avoid name collisions
COLUMN_RENAME_MAPPING = [
    ("stats_misc.csv", "stats_misc.csv", "Lost", "Lostm"),
    ("stats_standard.csv", "stats_standard.csv", "PrgC", "PrgCs"),
    ("stats_standard.csv", "stats_standard.csv", "PrgP", "PrgPs"),
    ("stats_standard.csv", "stats_standard.csv", "PrgR", "PrgRs"),
    ("stats_passing.csv", "stats_passing.csv", "PrgP", "PrgPp"),
    ("stats_passing.csv", "stats_passing.csv", "1/3", "Pto1/3"),
    ("stats_defense.csv", "stats_defense.csv", "Lost", "Lostd"),
    ("stats_defense.csv", "stats_defense.csv", "Att", "Attd"),
    ("stats_possession.csv", "stats_possession.csv", "Att", "Attp"),
    ("stats_possession.csv", "stats_possession.csv", "PrgC", "PrgCp"),
    ("stats_possession.csv", "stats_possession.csv", "1/3", "Cto1/3"),
    ("stats_possession.csv", "stats_possession.csv", "PrgR", "PrgRp"),
]

# Define headers to retain for each group
HeaderGroups = {
    'standard': ["Player", "Nation", "Squad", "Pos", "Age", "MP", "Starts", "Min",
                 "Gls", "Ast", "CrdY", "CrdR", "xG", "xAG", "PrgCs", "PrgPs", "PrgRs",
                 "Gls.1", "Ast.1", "xG.1", "xAG.1"],
    'shooting': ["Player", "Squad", "SoT%", "SoT/90", "G/Sh", "Dist"],
    'passing': ["Player", "Squad", "Cmp", "Cmp%", "TotDist", "Cmp%.1", "Cmp%.2", "Cmp%.3",
                "KP", "Pto1/3", "PPA", "CrsPA", "PrgPp"],
    'gca': ["Player", "Squad", "SCA", "SCA90", "GCA", "GCA90"],
    'defense': ["Player", "Squad", "Tkl", "TklW", "Attd", "Lostd", "Blocks", "Sh", "Pass", "Int"],
    'possession': ["Player", "Squad", "Touches", "Def Pen", "Def 3rd", "Mid 3rd", "Att 3rd", "Att Pen",
                   "Attp", "Succ%", "Tkld%", "Carries", "PrgDist", "PrgCp", "Cto1/3", "CPA", "Mis", "Dis", "Rec", "PrgRp"],
    'misc': ["Player", "Squad", "Fls", "Fld", "Off", "Crs", "Recov", "Won", "Lostm", "Won%"],
    'goalkeeping': ["Player", "Squad", "GA90", "Save%", "CS%", "Save%.1"]
}

# Map each group name to its corresponding CSV filename
FileMap = {
    'standard': 'stats_standard.csv',
    'shooting': 'stats_shooting.csv',
    'passing': 'stats_passing.csv',
    'gca': 'stats_gca.csv',
    'defense': 'stats_defense.csv',
    'possession': 'stats_possession.csv',
    'misc': 'stats_misc.csv',
    'goalkeeping': 'stats_keeper.csv'
}

print("🔄 Starting data merging process...")

# Sort files, remove duplicate headers, and rename conflicting columns
XL.sort_and_renumber(FILE_LIST)
XL.clean_duplicate_headers(FILE_LIST)
XL.rename_columns(COLUMN_RENAME_MAPPING)

try:
    # Load base stats from standard file
    std_df = pd.read_csv('stats_standard.csv')
    
    # Ensure required columns exist
    required_columns = ['PrgCs', 'PrgPs', 'PrgRs']
    for col in required_columns:
        if col not in std_df.columns:
            print(f"⚠️ Column {col} not found. Skipping...")

    # Standardize minutes and position format
    std_df = XL.clean_minutes_column(std_df)
    std_df = XL.normalize_pos_column(std_df)

    # Filter players with total minutes > 90
    player_total_min = std_df.groupby('Player')['Min'].sum()
    valid_players = player_total_min[player_total_min > 90].index.tolist()
    std_df = std_df[(std_df['Player'].isin(valid_players)) & (std_df['Min'] > 90)]

    # Select standard columns only
    base_df = std_df[HeaderGroups['standard']].copy()

    print(f"✅ Found {len(base_df)} players with more than 90 minutes.")
except Exception as e:
    print(f"❌ Error processing 'stats_standard.csv': {e}")
    exit()

# Merge all remaining data groups into base_df
for group, headers in HeaderGroups.items():
    if group == 'standard':
        continue  # Already handled

    file = FileMap[group]
    print(f"\n📄 Processing file: {file}")

    if not os.path.exists(file):
        print(f"⚠️ File not found: {file}. Skipping...")
        continue

    try:
        df = pd.read_csv(file)
        df = XL.clean_minutes_column(df)
        df = XL.normalize_pos_column(df)

        # Filter rows by minimum minutes and valid players
        if 'Min' in df.columns:
            df = df[df['Min'] > 90]
        df = df[df['Player'].isin(base_df['Player'])]

        # Keep relevant headers only
        df = df[headers].copy()

        # Merge with base dataframe on Player and Squad
        base_df = pd.merge(base_df, df, on=["Player", "Squad"], how="left")

    except Exception as e:
        print(f"❌ Error merging {file}: {e}")

try:
    # Replace missing object-type values with 'Na'
    for col in base_df.select_dtypes(include=['object']).columns:
        base_df[col] = base_df[col].fillna("Na")

    # Export the final merged result to CSV
    base_df.to_csv("results.csv", index=False, encoding='utf-8-sig')

    print(f"\n✅ Final dataset saved: results.csv")
    print(f"👥 Total unique players: {base_df['Player'].nunique()}")
    print(f"📊 Total rows: {len(base_df)}")
    print(f"📌 Sample players: {base_df['Player'].drop_duplicates().head(5).tolist()} ...")

except Exception as e:
    print(f"❌ Error saving results: {e}")