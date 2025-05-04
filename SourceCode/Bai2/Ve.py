import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset from 'results.csv'
df = pd.read_csv("results.csv")

skip_headers = ['Player', 'Nation', 'Squad', 'Pos']

# Replacing missing values with 0.00
df.replace("N/a", 0.00, inplace=True)

# Function to normalize age from 'years-days' format to float
def normalize_age(age_str):
    try:
        if isinstance(age_str, str) and '-' in age_str:
            years, days = map(int, age_str.split('-'))
            return round(years + days / 365, 2)
        return float(age_str)
    except:
        return 0.0

# Apply age normalization if 'Age' column exists
if 'Age' in df.columns:
    print("Normalizing 'Age' column ...")
    df['Age'] = df['Age'].apply(normalize_age)

# Generate histograms for all numeric columns
print("Generating histograms for statistics ...")
for col in df.columns:
    if col in skip_headers:
        continue
    try:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        print(f"Plotting: {col}")
        plt.hist(df[col], bins=30, color='skyblue', edgecolor='black')
        plt.title(f"Histogram: {col}")
        plt.xlabel(col)
        plt.ylabel("Number of Players")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        # Skip columns that cause errors during numeric conversion or plotting
        print(f"Skipping column {col} due to error: {e}")

# Bar chart for number of players by position
if 'Pos' in df.columns:
    print("Plotting: Number of players by position")
    pos_counts = df['Pos'].value_counts()
    plt.bar(pos_counts.index, pos_counts.values, color='orange', edgecolor='black')
    plt.title("Number of Players by Position")
    plt.xlabel("Position")
    plt.ylabel("Number of Players")
    plt.tight_layout()
    plt.show()

# Process complete
print("Chart generation complete.")
