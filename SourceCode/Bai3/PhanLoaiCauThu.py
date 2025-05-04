import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px

# Load dataset
df = pd.read_csv("results.csv")

# Extract stats from 'Nation' to the end
stats = df.loc[:, 'Nation':]

# Clean percentage values and convert to numeric
stats = stats.apply(lambda col: col.astype(str).str.replace('%', '', regex=False))
stats = stats.apply(pd.to_numeric, errors='coerce')

# Fill missing values with 0
stats.fillna(0, inplace=True)

# Normalize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(stats)

# Apply K-means clustering
k = 10
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
df['Cluster'] = labels + 1  # Cluster starts from 1

# Reduce dimensionality for visualization
pca = PCA(n_components=2)
pca_stats = pca.fit_transform(X_scaled)
df['PC1'] = pca_stats[:, 0]
df['PC2'] = pca_stats[:, 1]

# Plot PCA scatter plot with clusters
fig = px.scatter(
    df,
    x='PC1',
    y='PC2',
    color='Cluster',
    hover_data=['Player', 'Squad', 'Pos', 'Age'],
    title=f"K-means Clustering (K={k}, PCA Projection)",
    color_continuous_scale='Viridis'
)

# Customize marker size and layout
fig.update_traces(marker=dict(size=8, opacity=0.7))
fig.update_layout(
    xaxis_title="Principal Component 1",
    yaxis_title="Principal Component 2",
    legend_title="Cluster"
)

# Show the interactive scatter plot
fig.show()
