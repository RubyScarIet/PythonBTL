import pandas as pd
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv('results.csv')
df = df[df['Pos'] != 'GK']  # Remove goalkeepers

# Select 3 representative attack and defense metrics
attack_columns = ['Gls', 'Ast', 'xG']
defense_columns = ['Tkl', 'Int', 'Blocks']

# Function to plot histograms for each statistic
def plot_histogram_for_column(df, column, title, color):
    plt.figure(figsize=(12, 5))
    plt.hist(df[column], bins=30, color=color, edgecolor='black')
    plt.title(title)
    plt.xlabel(f'{title}')
    plt.ylabel('Number of Players')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot histograms for selected attacking metrics
for col in attack_columns:  
    plot_histogram_for_column(df, col, f'{col} Histogram', 'skyblue')

# Plot histograms for selected defensive metrics
for col in defense_columns:  
    plot_histogram_for_column(df, col, f'{col} Histogram', 'lightgreen')
