import pandas as pd
import streamlit as st

import data_processing
import machine_learning

# -------------- #
# --- WEBAPP --- #
# -------------- #


# Browser title, favicon and about section
st.set_page_config(
    page_title="Natural Language Processor",
    page_icon="📘",
    layout="wide",
    menu_items={
        'About': '''Developed by CENTIC.
                    For bugs and help, [mail us](mailto:centic@centic.es)'''
    }
)

st.title(f'Analizador morfosintáctico')
st.write(f"""Herramienta para el análisis de consentimientos médicos para la
             determinación de su legibilidad y comprensibilidad desarrollada por
             el Centro tecnológico de las Tecnologías de la Información y la
             Comunicación de Murcia (CENTIC).""")

lang, space, file_uploader = st.columns([1, 0.5, 3])
# Language selection
with lang:
    selected_lang = st.selectbox(
        "Seleccione el idioma de los ficheros de entrada",
        ('Español', 'Catalán', 'Inglés', 'Portugués', 'Francés', 'Alemán'),
        index=0)

# Files
with file_uploader:
    uploaded_files = st.file_uploader(
        label='Suba los ficheros en esta sección:',
        accept_multiple_files=True,
        type=['txt'])

freeling_results = []
if uploaded_files:
    try:
        freeling_results = data_processing.freeling_processing(
            uploaded_files, selected_lang)
    except UnicodeError as exc:
        st.error(f'{exc}')
    except Exception as exc:
        st.error(f'{exc}')

documents_metrics = []

if freeling_results:
    with st.spinner(f'Extrayendo métricas...'):
        documents_metrics = [
            data_processing.extract_metrics(morphological_analysis,
                                            text,
                                            filename,
                                            selected_lang) for
            morphological_analysis, text, filename in freeling_results]

if documents_metrics:
    dataframe = pd.DataFrame.from_records(documents_metrics)
    dataframe.set_index('name', drop=False, inplace=True)
    options = list(dataframe.columns)
    options.remove('name')

    selected_features = st.multiselect(
        "Seleccione las variables a comparar",
        options,
        default=[
            "total_sentences",
            "total_words",
        ],
        help=(f'Seleccione las características que quiere visualizar.'
              f' Por ahora solo se soportan __2 variables simultáneas.__'),
    )

    if not selected_features:
        df_show = dataframe[options]
    else:
        df_show = dataframe[selected_features].copy()

    st.dataframe(df_show)
    st.download_button('Descargar .csv',
                       data=df_show.to_csv().encode('utf-8'),
                       file_name='dataframe.csv')

    # Plot if enough selected features and files
    if len(selected_features) > 1:
        df_show['name'] = df_show.index
        st.altair_chart(data_processing.plot_selection(df_show))
    if df_show.shape[0] > 1:
        st.header('Análisis de componentes principales')
        tsne = machine_learning.process_tsne(dataframe[options])
        pca, components = machine_learning.get_pca(dataframe[options])

        pca_col, space, components_col = st.columns([10, 1, 10])
        with pca_col:
            st.subheader('Clúster de componentes principales')
            st.dataframe(pca, height=200)
            st.download_button('Descargar .csv',
                               data=pca.to_csv().encode('utf-8'),
                               file_name='pca.csv')
            st.altair_chart(data_processing.plot_pca(pca),
                            use_container_width=False)

        with components_col:
            st.subheader(f'Peso de cada característica en cada '
                         f'componente principal')
            st.dataframe(components, height=200)
            st.download_button('Descargar .csv',
                               data=components.to_csv().encode('utf-8'),
                               file_name='pca.csv')
            selected_component = st.selectbox(
                "Seleccione la componente a desglosar",
                range(1, len(components.columns) + 1),
                index=0)
            st.altair_chart(
                data_processing.plot_components(components,
                                                selected_component),
                use_container_width=True)

        st.subheader('TSNE')
        st.altair_chart(data_processing.plot_pca(tsne))

    else:
        st.write(f"Necesitas al menos 2 ficheros y 2 variables a comparar para"
                 f"mostrar la representación gráfica y el PCA.")
else:
    st.stop()
