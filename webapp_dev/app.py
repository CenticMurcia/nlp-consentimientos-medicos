import pandas as pd
import streamlit as st

import data_processing as dp


def show_metrics():
    with st.expander(f"Documento: {uploaded_file.filename}"):
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Caracteres (sin espacios):", value=metrics['total_chars'])
        col2.metric("Palabras:", value=metrics['total_words'])
        col3.metric("Palabras únicas:", value=metrics['total_unique_words'])
        col4.metric("Oraciones:", value=metrics['total_sentences'])
        col1.metric("T. Rápido",
                    value=f"{round(metrics['read_fast_time'], 2)} min")
        col2.metric("T. Medio",
                    value=f"{round(metrics['read_medium_time'], 2)} min")
        col3.metric("T. Lento",
                    value=f"{round(metrics['read_slow_time'], 2)} min")

        # col1.metric("Sustantivos:", value=morpho_count['N'])
        # col2.metric("Sustantivos/Total:",
        #             value=str(round(morpho_count['N']/n_words, 4)*100) + "%")
        # col1.metric("Adjetivos:", value=morpho_count['A'])
        # col2.metric("Adjetivos/Total:",
        # value=round(morpho_count['A']/n_words, 3))
        # col1.metric("Conjunciones:", value=morpho_count['C'])
        # col2.metric("Conjunciones/Total:",
        #             value=round(morpho_count['C']/n_words, 3))
        # col1.metric("Adverbios:", value=morpho_count['R'])
        # col2.metric("Adverbios/Total:",
        # value=round(morpho_count['R']/n_words, 3))
        # col1.metric("Verbos:", value=morpho_count['V'])
        # col2.metric("Verbos/Total:",
        # value=round(morpho_count['V']/n_words, 3))
        # col1.metric("Determinantes:", value=morpho_count['D'])
        # col2.metric("Determinantes/Total:",
        #             value=round(morpho_count['D']/n_words, 3))
        # col1.metric("Preposiciones:", value=morpho_count['P'])
        # col2.metric("Preposiciones/Total:",
        #             value=round(morpho_count['P']/n_words, 3))
        # col1.metric("Puntuación:", value=morpho_count['F'])
        # col2.metric("Puntuación/Total:",
        # value=round(morpho_count['F']/n_words, 3))

    # st.write(morpho_count)


# -------------- #
# --- WEBAPP --- #
# -------------- #


# Browser title, favicon and about section
st.set_page_config(
    page_title="NLP Processor",
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
    selected_lang = st.radio(
        "Seleccione el idioma de los ficheros de entrada",
        ('Español', 'Catalán'))

with file_uploader:
    uploaded_files = st.file_uploader(
        label='Suba los ficheros en esta sección:',
        accept_multiple_files=True,
        type=['txt'])

freeling_results = []
try:
    freeling_results = dp.freeling_processing(
        uploaded_files, selected_lang)
except UnicodeError as exc:
    st.error(f'''{exc}''')

documents_metrics = []

if freeling_results:
    for morphological_analysis, text, filename in freeling_results:
        documents_metrics.append(dp.extract_metrics(morphological_analysis, text,
                                                    filename))

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

    filtered_dataframe = dataframe[selected_features].copy()
    if not selected_features:
        st.dataframe(dataframe[options])
    elif len(selected_features) < 2:
        st.write(filtered_dataframe)
    else:
        filtered_dataframe['name'] = filtered_dataframe.index
        df_to_show = filtered_dataframe.drop('name', axis=1)
        st.write(df_to_show)
        st.download_button('Descargar .csv',
                           data=df_to_show.to_csv().encode('utf-8'),
                           file_name='dataframe.csv')
        st.altair_chart(dp.plot_selection(filtered_dataframe))
