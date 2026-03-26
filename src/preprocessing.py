import pandas as pd
from sklearn.preprocessing import StandardScaler

def clean_genomics_data(df, gene_list):
    """Filters data for specific genes and scales the values."""
    X = df[gene_list]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return pd.DataFrame(X_scaled, columns=gene_list)