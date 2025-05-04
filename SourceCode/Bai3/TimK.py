import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv("results.csv")

# Extract statistics starting from the 'Nation' column onward
stats = df.loc[:, 'Nation':]

# Remove percentage symbols and convert to numeric values
stats = stats.apply(lambda col: col.astype(str).str.replace('%', '', regex=False))
stats = stats.apply(pd.to_numeric, errors='coerce')
stats = stats.dropna(axis=1, how='all')
stats.fillna(0.00, inplace=True)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(stats)

# Evaluate inertia for a range of cluster numbers
inertia = []
K = range(2, 78)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Plot the Elbow method result
plt.figure(figsize=(10, 6))
plt.plot(K, inertia, 'bo-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (Within-cluster Sum of Squares)')
plt.title('Elbow Method – Choosing the Optimal Number of Clusters')
plt.grid(True)
plt.xticks(range(5, 80, 5))
plt.show()
