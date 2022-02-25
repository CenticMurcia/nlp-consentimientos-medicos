import streamlit as st
import requests
from unicodedata import normalize


@st.cache
def freeling_processing(document='4111_OR_ES.txt',
                        language='es'):
    # File to send
    file = document
    files = {'file': file}
    # Parameters
    params = {'outf': 'tagged', 'format': 'json', 'lang': language}
    # Send request
    url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
    r = requests.post(url, files=files, params=params)
    # Response to json
    obj = r.json()

    # Return morphological info
    return obj


def extract_metrics(document):

    col1, col2, col3, col4 = st.columns(4)
    # - Número de letras en el texto
    n_chars = sum([len(word['token'])
                  for phrase in document for word in phrase])
    col1.metric("Número de letras/caracteres (sin espacios):", value=n_chars)
    # - Número de sílabas en el texto
    # Nope
    # - Número de palabras en el texto (tokens)
    n_words = len([word for phrase in document for word in phrase])
    col2.metric("Número de palabras:", value=n_words)
    # - Número de palabras unicas en el texto (Tipos)
    n_unique_words = len(set([word['token']
                         for phrase in document for word in phrase]))
    col3.metric("Número de palabras únicas:", value=n_unique_words)
    # - Número de frases en el texto (oraciones)
    n_phrases = len([phrase for phrase in document])
    col4.metric("Número de oraciones:", value=n_phrases)


def morphological_metrics(document):
    """Extracts the number of nouns, verbs, adjectives, etc"""


#--------------#
#### WEBAPP ####
#--------------#
def example_callback():
    print('TEST')


st.title('CENTIC FTW')

uploaded_files = st.file_uploader(
    label='Tus ficheros aquí', accept_multiple_files=True, on_change=example_callback, type=['txt'])


for uploaded_file in uploaded_files:
    # Read the files as 'utf-8' or 'latin-1'
    string_data = None
    try:
        string_data = uploaded_file.getvalue().decode('utf-8')
    except UnicodeDecodeError:
        print('File is not UTF-8. Trying with Latin-1')

        try:
            string_data = uploaded_file.getvalue().decode('latin-1')
        except:
            print('File encoding is not supported')


    # Chars can be codified as 'a´' o 'á'
    # Let's transform all of them to "á", because Freeling takes 'a´'
    # as separated chars and break words because of this
    string_data = normalize("NFC", string_data)

    st.header(f"Documento: {uploaded_file.name}")
    # Inform the user of success read
    # st.success('Fichero leido con éxito :sunglasses:')

    with st.spinner('Procesando texto en Freeling...'):
        document = freeling_processing(document=string_data, language='es')
    #st.json(document[0])

    extract_metrics(document)
