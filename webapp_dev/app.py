import streamlit as st
import data_processing as dp
import pandas as pd
import altair as alt


def show_metrics():
    with st.expander(f"Documento: {uploaded_file.name}"):
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


def plot_selection(dataframe):
    graphic = (alt.Chart(dataframe).mark_circle(size=60).encode(
        x=dataframe.columns[1],
        y=dataframe.columns[2],
        # color='Origin',
        tooltip=['name', dataframe.columns[0], dataframe.columns[1]]
    ).interactive())
    return graphic


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

st.title(f'CENTIC WTF! :book: :tada:')
st.write(f"""Esta herramienta tiene la intención de facilitar el análisis de
            textos mediante técnicas de procesamiento del lenguaje natural.""")

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

documents = []
# Loop for every uploaded file
for uploaded_file in uploaded_files:
    try:
        string_data = dp.read_file(uploaded_file)
    except UnicodeError:
        st.error(f'''File **{uploaded_file.name}** is not
                encoded in UTF-8 or Latin-1''')
        continue

    with st.spinner(f'''Procesando fichero **{uploaded_file.name}**
                    con Freeling...'''):
        document = dp.freeling_processing(
            document=string_data, language=selected_lang)

    documents.append(dp.extract_metrics(document, uploaded_file.name))

if documents:
    dataframe = pd.DataFrame.from_records(documents)
    with st.expander('Dataframe de documentos'):
        st.write(dataframe)

    with st.expander('Gráficos'):
        select_features = st.multiselect(
            "Select Python packages to compare",
            dataframe.columns,
            default=[
                "name",
                "total_sentences",
                "total_words",
            ],
            help='Seleccione las características que quiere visualizar',
        )

        selected_features = dataframe[select_features]

        st.write(selected_features)

        if not select_features:
            st.stop()

        x = plot_selection(selected_features)
        st.altair_chart(x)
    # st.write(metrics)

    # st.write(document[:][0])

    # show_metrics()
