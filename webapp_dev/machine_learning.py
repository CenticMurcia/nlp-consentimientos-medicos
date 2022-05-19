import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import streamlit as st


@st.experimental_memo(show_spinner=False)
def extract_pca_metrics(dataframe):
    x = StandardScaler().fit_transform(dataframe.values)
    pca = PCA(n_components=min([dataframe.shape[0], dataframe.shape[1], 10]))
    principal_components = pca.fit_transform(x)
    components = pca.components_
    explained_variance = pca.explained_variance_ratio_*100
    return principal_components, components, explained_variance


@st.experimental_memo(show_spinner=False)
def get_pca(dataframe):
    principal_components, components, explained_variance = extract_pca_metrics(
        dataframe)
    components_df = pd.DataFrame(data=components, columns=dataframe.columns,
                                 index=[f'Componente {i}' for i in
                                        range(1, len(components) + 1)])

    components_df = components_df.transpose()

    components_df.columns = [f'{c} ({v:.3f}%)' for c, v in zip(components_df,
                                                        explained_variance)]

    pca_df = pd.DataFrame(data=principal_components,
                          columns=[f'Componente {i}' for i in
                                   range(1, len(components) + 1)])
    dataframe = dataframe.reset_index(level=0)
    pca_df = pd.concat([pca_df, dataframe['name']], axis=1)
    pca_df.set_index('name', inplace=True)

    return pca_df, components_df


@st.experimental_memo(show_spinner=False)
def process_tsne(dataframe):
    x = StandardScaler().fit_transform(dataframe.values)
    tsne = TSNE(n_components=2, learning_rate='auto', init='pca',
                n_jobs=-1).fit_transform(x)
    tsne_df = pd.DataFrame(data=tsne,
                           columns=[f'Componente {i}' for i in range(1, 3)])
    dataframe = dataframe.reset_index(level=0)
    tsne_df = pd.concat([tsne_df, dataframe['name']], axis=1)
    return tsne_df
