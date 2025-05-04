import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Function to calculate score based on age
def AgeScore(age):
    if pd.isna(age):
        return 0.0
    if isinstance(age, str) and '-' in age:
        age = age.split('-')[0]
    try:
        age = int(age)
    except ValueError:
        return 0.0
    if age <= 18: return 1.0
    elif age <= 21: return 0.9
    elif age <= 24: return 0.8
    elif age <= 27: return 0.6
    elif age <= 30: return 0.4
    elif age <= 33: return 0.2
    else: return 0.1

# Function to calculate score based on playing time
def TimeScore(minutes):
    if pd.isna(minutes):
        return 0.0
    try:
        minutes = float(minutes)
    except ValueError:
        return 0.0
    if minutes < 900: return 0.2
    elif minutes < 1500: return 0.4
    elif minutes < 2000: return 0.6
    elif minutes < 2500: return 0.8
    else: return 1.0

# Function to calculate performance score
def PerformanceScore(row):
    pos = row['Pos']
    score = 0
    if not isinstance(pos, str) or pos.strip() == '':
        return 0.0
    if 'GK' in pos:
        score += row.get('GA90', 0) * 0.5
        score += row.get('Save%', 0) * 0.6
        score += row.get('CS%', 0) * 0.4
        score += row.get('Save%.1', 0) * 0.3
    if 'DF' in pos:
        score += row.get('Tkl', 0) * 0.5
        score += row.get('TklW', 0) * 0.4
        score += row.get('Attd', 0) * 0.3
        score += row.get('Lostd', 0) * -0.2
        score += row.get('Blocks', 0) * 0.5
        score += row.get('Sh', 0) * 0.3
        score += row.get('Pass', 0) * 0.2
        score += row.get('Int', 0) * 0.4
    if 'MF' in pos:
        score += row.get('Cmp', 0) * 0.4
        score += row.get('Cmp%', 0) * 0.3
        score += row.get('TotDist', 0) * 0.2
        score += row.get('Cmp%.1', 0) * 0.3
        score += row.get('Cmp%.2', 0) * 0.2
        score += row.get('Cmp%.3', 0) * 0.2
        score += row.get('KP', 0) * 0.4
        score += row.get('Pto1/3', 0) * 0.3
        score += row.get('PPA', 0) * 0.3
        score += row.get('CrsPA', 0) * 0.2
        score += row.get('PrgPp', 0) * 0.5
    if 'FW' in pos:
        score += row.get('Gls', 0) * 0.6
        score += row.get('Ast', 0) * 0.5
        score += row.get('CrdY', 0) * -0.1
        score += row.get('CrdR', 0) * -0.2
        score += row.get('xG', 0) * 0.7
        score += row.get('xAG', 0) * 0.6
        score += row.get('PrgCs', 0) * 0.3
        score += row.get('PrgPs', 0) * 0.3
        score += row.get('PrgRs', 0) * 0.3
    return round(score / len(pos.split('-')) if '-' in pos else score, 2)

# Normalize percentage columns
def NormalizePercentage(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col] / 100
    return df

# Min-max normalization for selected columns
def NormalizeMinMax(df, columns):
    scaler = MinMaxScaler()
    valid_cols = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    if not valid_cols:
        print("No valid columns found for normalization.")
        return df
    df[valid_cols] = scaler.fit_transform(df[valid_cols])
    return df

# Load data
df = pd.read_csv('ChoiTren900p.csv')

# Normalize percentage columns
columns_percent = ['Save%', 'SoT%', 'Cmp%', 'CS%', 'Won%', 'Save%.1']
df = NormalizePercentage(df, columns_percent)

# Columns to normalize using min-max
columns_minmax = [
    'TotDist', 'Pass', 'Cmp', 'Sh', 'Tkl', 'TklW', 'Attd', 'Lostd', 'Blocks', 'Int',
    'Cmp%.1', 'Cmp%.2', 'Cmp%.3', 'KP', 'Pto1/3', 'PPA', 'CrsPA', 'PrgPp',
    'Gls', 'Ast', 'CrdY', 'CrdR', 'xG', 'xAG', 'PrgCs', 'PrgPs', 'PrgRs',
    'GA90'
]
columns_minmax = [col for col in columns_minmax if col in df.columns]
df = NormalizeMinMax(df, columns_minmax)

# Fill NaN with 0 in selected columns
for col in columns_minmax + columns_percent:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Calculate auxiliary scores
df['Age_Score'] = df['Age'].apply(AgeScore)
df['Time_Score'] = df['Min'].apply(TimeScore)

# Calculate performance score
df['Performance_Score'] = df.apply(PerformanceScore, axis=1)

# Calculate overall rating (DanhGia) based on a threshold (e.g., 0.5)
df['DanhGia'] = (df['Performance_Score'] + df['Age_Score'] + df['Time_Score']) / 3
df['DanhGia'] = df['DanhGia'].apply(lambda x: 1 if x >= 0.8 else 0)

# Save the result
df_result = df[['Player', 'Nation', 'Squad', 'Pos', 'Age_Score', 'Time_Score', 'Performance_Score', 'DanhGia']]
df_result.to_csv('DataDanhGia.csv', index=False)
print(df_result.head())
