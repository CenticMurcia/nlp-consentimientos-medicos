import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def process_pca(dataframe):
    x = StandardScaler().fit_transform(dataframe.values)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x)
    pca_df = pd.DataFrame(data=principal_components,
                          columns=['Componente principal 1',
                                   'Componente principal 2'])
    dataframe = dataframe.reset_index(level=0)
    pca_df = pd.concat([pca_df, dataframe['name']], axis=1)
    pca_df.set_index('name', inplace=True)
    return pca_df
