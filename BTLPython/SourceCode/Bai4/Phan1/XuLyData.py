import pandas as pd

# Function to remove specified columns from the dataset
def XoaHeader(columns_to_remove, input_file, output_file):
    df = pd.read_csv(input_file)
    print("📌 Before removal:", df.columns.tolist())

    # Loop through columns to remove and drop them if they exist
    for col in columns_to_remove:
        if col in df.columns:
            df.drop(columns=col, inplace=True)
            print(f"🗑️ Removed column: {col}")
        else:
            print(f"⚠️ Column not found: {col}")

    # Save the modified dataset to a new CSV file
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Saved the new file to: {output_file}")

# Function to rename a column in the dataset
def DoiTen(clo_1, clo_2, input_file, output_file):
    df = pd.read_csv(input_file)
    print("📌 Before renaming:", df.columns.tolist())

    if clo_1 in df.columns:
        df.rename(columns={clo_1: clo_2}, inplace=True)
        print(f"📝 Renamed column '{clo_1}' to '{clo_2}'")
    else:
        print(f"⚠️ Column not found: {clo_1}")

    # Save the modified dataset to a new CSV file
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Saved the new file to: {output_file}")

# Function to normalize player names by removing squad names from the player column
def ChuanHoaTen(input_file, output_file):
    df = pd.read_csv(input_file)
    print("📌 Before normalizing Player:", df[['Player', 'Squad']].head())

    if 'Player' in df.columns and 'Squad' in df.columns:
        # Strip squad name from the player name if found
        df['Player'] = df.apply(lambda row: str(row['Player']).split(str(row['Squad']))[0].strip() if str(row['Squad']) in str(row['Player']) else str(row['Player']).strip(), axis=1)
        print("✅ Removed Squad from Player")
    else:
        print("⚠️ 'Player' or 'Squad' column not found in data")

    # Save the modified dataset to a new CSV file
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Saved the data to: {output_file}")

# Function to further normalize player names by removing repeated characters
def ChuanHoaTen2(input_file, output_file):
    df = pd.read_csv(input_file)
    print("📌 Before normalizing Player:", df['Player'].head())

    if 'Player' in df.columns:
        def ThoiTaChiaDoi(s):
            s = str(s).strip()
            length = len(s)
            for i in range(1, length // 2 + 1):
                if length % i == 0:
                    substring = s[:i]
                    if substring * (length // i) == s:
                        return substring
            return s

        # Apply the function to remove repeating characters in player names
        df['Player'] = df['Player'].apply(ThoiTaChiaDoi)
        print("✅ Removed repeating parts in Player")
    else:
        print("⚠️ 'Player' column not found in data")

    # Save the modified dataset to a new CSV file
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Saved the data to: {output_file}")

# Function to normalize squad names according to a predefined mapping
def ChuanHoaSquad(input_file, output_file):
    df = pd.read_csv(input_file)
    print("📌 Before normalizing Squad:", df['Squad'].unique())

    if 'Squad' in df.columns:
        SquadMapping = {
            'Arsenal': 'Arsenal',
            'Aston Villa': 'Aston Villa',
            "B'mouth": 'Bournemouth',
            'Brentford': 'Brentford',
            'Brighton': 'Brighton',
            'Chelsea': 'Chelsea',
            'C. Palace': 'Crystal Palace',
            'Everton': 'Everton',
            'Fulham': 'Fulham',
            'Ipswich Town': 'Ipswich Town',
            'Liverpool': 'Liverpool',
            'Leicester': 'Leicester City',
            'Man Utd': 'Manchester Utd',
            'Man City': 'Manchester City',
            'Newcastle Utd.': 'Newcastle Utd',
            'Nottingham': "Nott'ham Forest",
            'Southampton': 'Southampton',
            'Tottenham': 'Tottenham',
            'West Ham United': 'West Ham',
            'Wolverhampton': 'Wolves'
        }

        # Apply the mapping to normalize the squad names
        df['Squad'] = df['Squad'].apply(lambda x: SquadMapping.get(str(x).strip(), x))
        print("✅ Normalized Squad names")
    else:
        print("⚠️ 'Squad' column not found in data")

    # Save the modified dataset to a new CSV file
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Saved the data to: {output_file}")
