import pandas as pd

# Read data from CSV files
df_transfers = pd.read_csv("GiaTriCauThu.csv", encoding='utf-8-sig')
df_played = pd.read_csv("ChoiTren900p.csv", on_bad_lines='skip')

# Clean column names
df_transfers.columns = df_transfers.columns.str.strip()
df_played.columns = df_played.columns.str.strip()

# Check if 'ETV' column exists in df_transfers
if 'ETV' not in df_transfers.columns:
    raise ValueError("ETV column not found in GiaTriCauThu.csv")

# Merge datasets without modifying player names
merged = pd.merge(
    df_played[['Player', 'Squad']], 
    df_transfers[['Player', 'ETV']],
    on='Player',  # Matching on exact 'Player' names
    how='left'
)

# Check for any player names that did not match
unmatched_players = merged[merged['ETV'].isna()]['Player']
if not unmatched_players.empty:
    print(f"⚠️ These player names did not match (missing ETV):")
    print(unmatched_players)

# Separate players missing ETV
missing_etv = merged[merged['ETV'].isna()]
if not missing_etv.empty:
    # Drop the 'ETV' column from the missing players
    missing_etv = missing_etv.drop(columns=['ETV'])
    # Save missing players to 'Thieu.csv' without the 'ETV' column
    missing_etv.to_csv("Thieu.csv", index=False, encoding='utf-8-sig')
    print(f"⚠️ {len(missing_etv)} players are missing ETV values. Saved to Thieu.csv without ETV column.")

# Keep only players with ETV
result = merged.dropna(subset=['ETV'])

# Add index
result.insert(0, 'STT', range(1, len(result) + 1))

# Save result to 'ETV.csv'
result.to_csv("ETV.csv", index=False, encoding='utf-8-sig')
print(f"✅ Processed data for {len(result)} players with ETV.")
print("First 5 rows of the result:")
print(result.head())
