import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def process_pca(dataframe):
    x = StandardScaler.fit_transform(dataframe.values)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x)
    return pd.DataFrame(data=principal_components,
                        columns=['principal component 1', 'principal component 2'])
