import pandas as pd

try:
    # Load player data
    df = pd.read_csv('results.csv')

    # Ensure 'Min' column is numeric
    df['Min'] = pd.to_numeric(df['Min'], errors='coerce')

    # Filter players with less than 90 minutes played
    under_90_df = df[df['Min'] < 90]

    if not under_90_df.empty:
        print("⚠️ Players with less than 90 minutes played:")
        print(under_90_df[['Player', 'Min']])
        print(f"\n📊 Total: {len(under_90_df)} players")
    else:
        print("✅ All players have at least 90 minutes played")

except Exception as e:
    print(f"❌ Error reading or processing the file: {e}")
