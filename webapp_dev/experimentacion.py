import streamlit as st
import altair as alt
import data_processing as dp

def show_metrics():
    st.header(f"Documento: {uploaded_file.name}")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Caracteres (sin espacios):", value=n_chars)
    col2.metric("Palabras:", value=n_words)
    col3.metric("Palabras únicas:", value=n_unique_words)
    col4.metric("Oraciones:", value=n_phrases)
    col1.metric("T. Rápido", value=str(round(n_words/350, 2)) + ' min')
    col2.metric("T. Medio", value=str(round(n_words/250, 2)) + ' min')
    col3.metric("T. Lento", value=str(round(n_words/150, 2)) + ' min')
    col1.metric("Sustantivos:", value=morpho_count['N'])
    col2.metric("Sustantivos/Total:",
                value=str(round(morpho_count['N']/n_words, 4)*100) + "%")
    col1.metric("Adjetivos:", value=morpho_count['A'])
    col2.metric("Adjetivos/Total:", value=round(morpho_count['A']/n_words, 3))
    col1.metric("Conjunciones:", value=morpho_count['C'])
    col2.metric("Conjunciones/Total:",
                value=round(morpho_count['C']/n_words, 3))
    col1.metric("Adverbios:", value=morpho_count['R'])
    col2.metric("Adverbios/Total:", value=round(morpho_count['R']/n_words, 3))
    col1.metric("Verbos:", value=morpho_count['V'])
    col2.metric("Verbos/Total:", value=round(morpho_count['V']/n_words, 3))
    col1.metric("Determinantes:", value=morpho_count['D'])
    col2.metric("Determinantes/Total:",
                value=round(morpho_count['D']/n_words, 3))
    col1.metric("Preposiciones:", value=morpho_count['P'])
    col2.metric("Preposiciones/Total:",
                value=round(morpho_count['P']/n_words, 3))
    col1.metric("Puntuación:", value=morpho_count['F'])
    col2.metric("Puntuación/Total:", value=round(morpho_count['F']/n_words, 3))
    # st.write(morpho_count)

#--------------#
#### WEBAPP ####
#--------------#

# Browser title, favicon and about section
st.set_page_config(
    page_title="NLP Processor",
    page_icon="📘",
    layout="wide",
    menu_items={
        'About': "Developed by CENTIC. For bugs and help, [mail us](mailto:centic@centic.es)"
    }
)


st.title('CENTIC WTF')
st.write("""Esta herramienta tiene la intención de facilitar el análisis de textos
        mediante técnicas de procesamiento del lenguaje natural.""")

col1, space, col2 = st.columns([1, 0.5, 3])
# Language selection
with col1:
    slctd_lang = st.radio(
        "Seleccione el idioma de los ficheros de entrada",
        ('Español', 'Catalán'))
with col2:
    uploaded_files = st.file_uploader(
        label='Tus ficheros aquí',
        accept_multiple_files=True,
        type=['txt'])

# Loop for every uploaded file
for uploaded_file in uploaded_files:
    string_data = dp.read_file(uploaded_file)

    with st.spinner('Procesando texto en Freeling...'):
        document = dp.freeling_processing(
            document=string_data, language=slctd_lang)


    n_chars, n_words, n_unique_words, n_phrases = dp.extract_metrics(document)
    morpho_count = dp.morphological_metrics(document)
    st.write(document[:][0])

    #show_metrics()
