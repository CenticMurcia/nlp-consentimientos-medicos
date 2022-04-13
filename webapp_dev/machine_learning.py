import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler


def extract_pca_metrics(dataframe):
    x = StandardScaler().fit_transform(dataframe.values)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x)
    return principal_components, pca.components_


def get_pca(dataframe):
    principal_components, components = extract_pca_metrics(dataframe)

    components_df = pd.DataFrame(data=components,
                                 columns=dataframe.columns,
                                 index=[f'Componente {i}' for i in range(1, len(
                                     components) + 1)])
    components_df.reset_index(inplace=True)
    components_df = components_df.melt(id_vars=['index'])
    components_df.sort_values(by=['index', 'value'], inplace=True,
                              ascending=[True, False])

    pca_df = pd.DataFrame(data=principal_components,
                          columns=[f'Componente {i}' for i in range(1, len(
                              components) + 1)])
    dataframe = dataframe.reset_index(level=0)
    pca_df = pd.concat([pca_df, dataframe['name']], axis=1)
    pca_df.set_index('name', inplace=True)

    return pca_df, components_df


def process_tsne(dataframe):
    x = StandardScaler().fit_transform(dataframe.values)
    tsne = TSNE(n_components=2, learning_rate='auto').fit_transform(x)