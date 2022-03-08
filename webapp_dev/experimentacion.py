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


@st.cache
def extract_metrics(document):

    # - Número de letras en el texto
    n_chars = sum([len(word['token'])
                  for phrase in document for word in phrase])
    # - Número de sílabas en el texto
    # Nope
    # - Número de palabras en el texto (tokens)
    n_words = len([word for phrase in document for word in phrase])
    # - Número de palabras unicas en el texto (Tipos)
    n_unique_words = len(set([word['token']
                         for phrase in document for word in phrase]))
    # - Número de frases en el texto (oraciones)
    n_phrases = len([phrase for phrase in document])
    return n_chars, n_words, n_unique_words, n_phrases


@st.cache
def morphological_metrics(document):
    """Extracts the number of nouns, verbs, adjectives, etc"""

    morpho_count = {
        'N': 0,    # Nouns
        'A': 0,    # Adjectives
        'C': 0,    # Conjuctions
        'R': 0,    # Adverbs
        'V': 0,    # Verbs
        'D': 0,    # Determinants
        'P': 0,    # Pronouns
        'F': 0     # Punctuation
    }

    # Iterate the json and check the first letter (type)
    # of each word detected by Freeling. Then count on that
    # category
    for phrase in document:
        for word in phrase:
            if word['tag'][0] in morpho_count:
                morpho_count[word['tag'][0]] += 1
    return morpho_count


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

    col1, col2, col3, col4 = st.columns(4)

    n_chars, n_words, n_unique_words, n_phrases = extract_metrics(document)
    morpho_count = morphological_metrics(document)
    col1.metric("Caracteres (sin espacios):", value=n_chars)
    col2.metric("Palabras:", value=n_words)
    col3.metric("Palabras únicas:", value=n_unique_words)
    col4.metric("Oraciones:", value=n_phrases)
    col1.write(morpho_count)
