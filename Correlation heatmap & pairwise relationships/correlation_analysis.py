import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load a sample dataset
print("Loading 'mpg' dataset from seaborn...")
df = sns.load_dataset("mpg")

# Compute Pearson correlations between numeric features
numeric_df = df.select_dtypes(include=[np.number])
corr_matrix = numeric_df.corr(method="pearson")

print("\n--- Pearson Correlation Matrix ---")
print(corr_matrix)

# Visualize as heatmap (mask upper triangle, annotate values)
plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)

sns.heatmap(
    corr_matrix,
    mask=mask,
    cmap=cmap,
    vmax=1.0,
    vmin=-1.0,
    center=0,
    annot=True,
    fmt=".2f",
    square=True,
    linewidths=0.5,
    cbar_kws={"shrink": 0.5},
)
plt.title("Correlation Heatmap of Numeric Features", fontsize=16)
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=300)
print("\nSaved correlation heatmap to 'correlation_heatmap.png'")

# Use pairplots / scatter matrix for key variable pairs
key_vars = ["mpg", "displacement", "horsepower", "weight"]
print(f"\nCreating pairplot for key variables: {key_vars}")
sns.pairplot(df[key_vars].dropna(), diag_kind="kde", corner=True)
plt.suptitle("Pairplot of Key Variables", y=1.02)
plt.savefig("pairplot.png", dpi=300)
print("Saved pairplot to 'pairplot.png'")

# Summarize strongest positive/negative relationships
lower_tri = corr_matrix.where(np.tril(np.ones(corr_matrix.shape), k=-1).astype(bool))
stacked_corr = lower_tri.unstack().dropna()
sorted_corr = stacked_corr.sort_values()

print("\n--- Strongest Negative Relationships ---")
for pair, val in sorted_corr.head(3).items():
    print(f"{pair[0]} & {pair[1]}: {val:.4f}")

print("\n--- Strongest Positive Relationships ---")
for pair, val in sorted_corr.tail(3)[::-1].items():
    print(f"{pair[0]} & {pair[1]}: {val:.4f}")
