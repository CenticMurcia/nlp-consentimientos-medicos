import streamlit as st
import requests
from unicodedata import normalize


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
    #st.write(document[0][0])
    # - Número de letras en el texto
    n_chars = sum([len(word['token']) for phrase in document for word in phrase])
    st.write(f"Número de letras/caracteres (sin espacios): {n_chars}")
    # - Número de sílabas en el texto
    # Nope
    # - Número de palabras en el texto (tokens)
    n_words = len([word for phrase in document for word in phrase])
    st.write(f"Número de palabras: {n_words}")
    # - Número de palabras unicas en el texto (Tipos)
    n_unique_words = len(set([word['token']
                         for phrase in document for word in phrase]))
    st.write(f"Número de palabras únicas: {n_unique_words}")
    # - Número de frases en el texto (oraciones)
    n_phrases = len([phrase for phrase in document])
    st.write(f"Número de oraciones: {n_phrases}")

    #


def morphological_metrics(document):
    pass


#--------------#
#### WEBAPP ####
#--------------#
def example_callback():
    print('TEST')


st.title('CENTIC FTW')

uploaded_files = st.file_uploader(
    label='Tus ficheros aquí', accept_multiple_files=True, on_change=example_callback, type=['txt'])

for uploaded_file in uploaded_files:
    # Read the files as 'utf-8'
    string_data = uploaded_file.getvalue().decode('utf-8')

    # Chars can be codified as 'a´' o 'á'
    # Let's transform all of them to "á", because Freeling takes 'a´'
    # as separated chars and break words because of this
    string_data = normalize("NFC", string_data)

    # Inform the user of success read
    st.success('Fichero leido con éxito :sunglasses:')

    with st.spinner('Procesando texto en Freeling...'):
        document = freeling_processing(document=string_data, language='es')

    
    extract_metrics(document)
