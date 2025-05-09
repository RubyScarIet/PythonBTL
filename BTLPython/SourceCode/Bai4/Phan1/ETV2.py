import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz

# Read data
df_etv = pd.read_csv('ETV.csv')
df_gt = pd.read_csv('GiaTriCauThu.csv')
df_thieu = pd.read_csv('Thieu.csv')

# Clean column names
df_etv.columns = df_etv.columns.str.strip()
df_gt.columns = df_gt.columns.str.strip()
df_thieu.columns = df_thieu.columns.str.strip()

# Generate CheckLan2.csv by subtracting ETV from GiaTriCauThu
df_checklan2 = pd.merge(df_gt, df_etv[['Player', 'Squad']], on=['Player', 'Squad'], how='left', indicator=True)
df_checklan2 = df_checklan2[df_checklan2['_merge'] == 'left_only'].drop(columns=['_merge'])
df_checklan2.to_csv('CheckLan2.csv', index=False, encoding='utf-8-sig')

print(f"🔍 Total rows in CheckLan2.csv: {len(df_checklan2)}")
print(f"📋 Total rows in Thieu.csv: {len(df_thieu)}")

# Matching process
matches = []
matched_players = set()
checked_players = {}

for index, thieu_row in df_thieu.iterrows():
    player_thieu = thieu_row['Player']
    squad_thieu = thieu_row['Squad']
    if player_thieu in matched_players:
        continue

    best_match = None
    for _, check_row in df_checklan2.iterrows():
        player_check = check_row['Player']
        squad_check = check_row['Squad']
        score = fuzz.partial_ratio(player_thieu.lower(), player_check.lower())

        if score >= 55 and squad_thieu == squad_check:
            # Check if already exists in df_etv
            already_exists = (
                ((df_etv['Player'] == player_check) & (df_etv['Squad'] == squad_check)).any()
            )
            if not already_exists:
                best_match = (player_check, squad_check, player_thieu, squad_thieu, score)
            break
        if score < 55 and player_thieu not in matched_players:
            checked_players[player_thieu] = score

    if best_match:
        matches.append(best_match)
        matched_players.add(player_thieu)
        if player_thieu in checked_players:
            del checked_players[player_thieu]
    
    if (index + 1) % 50 == 0 or (index + 1) == len(df_thieu):
        print(f"✅ Processed {index + 1}/{len(df_thieu)} rows in Thieu.csv...")

# Save matches to ETV2.csv
matches_df = pd.DataFrame(matches, columns=['Player', 'Squad', 'Player_Thieu', 'Squad_Thieu', 'Similarity'])
matches_df.to_csv('ETV2.csv', index=False)

print(f"\n✅ Matched successfully: {len(matches_df)} players.")
print(f"⚠️ Players checked but not matched: {len(checked_players)}")

# Merge with GiaTriCauThu.csv to get ETV
merged_etv2 = pd.merge(
    matches_df,
    df_gt[['Player', 'Squad', 'ETV']],
    on=['Player', 'Squad'],
    how='left'
)

# Get the original Player name from CheckLan2.csv, not Player_Thieu
df_etv2_final = merged_etv2[['Player', 'Squad_Thieu', 'ETV']].rename(
    columns={'Squad_Thieu': 'Squad'}
)

# Combine with original ETV.csv to avoid duplicates
combined_etv = pd.concat([df_etv[['Player', 'Squad', 'ETV']], df_etv2_final], ignore_index=True)
combined_etv.drop_duplicates(subset=['Player', 'Squad'], keep='first', inplace=True)

# Sort and reassign index
combined_etv = combined_etv.sort_values(by='Player').reset_index(drop=True)
combined_etv.insert(0, 'STT', range(1, len(combined_etv) + 1))

# Save final result
combined_etv.to_csv('ETV.csv', index=False, encoding='utf-8-sig')

print(f"\n📦 Total rows in final ETV.csv: {len(combined_etv)}")
