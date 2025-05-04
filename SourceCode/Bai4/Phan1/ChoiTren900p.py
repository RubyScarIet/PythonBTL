import pandas as pd

# Read the dataset
df = pd.read_csv("results.csv")

# Ensure the 'Min' column is numeric
df['Min'] = pd.to_numeric(df['Min'], errors='coerce')

# Filter players who have played more than 900 minutes
filtered_df = df[df['Min'] > 900].copy()

# Sort by player name (ascending)
filtered_df.sort_values(by='Player', inplace=True)

# Reset index to start from 1 and label it 'STT'
filtered_df.reset_index(drop=True, inplace=True)
filtered_df.index = filtered_df.index + 1

# Save the filtered list to CSV
filtered_df.to_csv("ChoiTren900p.csv", index_label="STT")

# Print the number of players saved
print(f"✅ Saved {len(filtered_df)} players to ChoiTren900p.csv.")
