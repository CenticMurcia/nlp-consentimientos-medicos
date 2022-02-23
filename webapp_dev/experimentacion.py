from io import StringIO
from bs4 import UnicodeDammit
import streamlit as st
import requests
from unicodedata import normalize


def freeling_processing(document = '4111_OR_ES.txt',    
                        language = 'es'):
    #Archivo a ser enviado
    file = document
    files = {'file': file}
    #Parámetros
    params = {'outf': 'tagged', 'format': 'json', 'lang': language}
    #Enviar petición
    url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
    r = requests.post(url, files=files, params=params)
    #Convertir de formato json
    obj = r.json()

    # Devolvemos el diccionario con la info morfológica
    return obj

    # Ejemplo para mostrar toda la información del procesado de freeling
    # for sentence in obj:
    #     for word in sentence:
    #         print(word)
#--------------#
#### WEBAPP ####
#--------------#
def example_callback():
    print('TEST')


st.title('Título de muestra')

uploaded_files = st.file_uploader(label= 'Tus ficheros aquí', accept_multiple_files=True, on_change=example_callback, type=['txt'] )

for uploaded_file in uploaded_files:
    string_data = uploaded_file.getvalue()
    dammit = UnicodeDammit(string_data)
    string_data = string_data.decode('utf-8')
    # ESTA LINEA ME HA LLEVADO 3 HORAS PARA SABER QUE FALLABA
    # Los caracteres vienen separados por su codigo individual, de forma
    # que los acentos vienen codificados como a´ en vez de á. UN DRAMA
    string_data = normalize("NFC", string_data)

    st.warning(dammit.original_encoding)
    st.write('Fichero leido con éxito :sunglasses:')
    st.write(string_data)
    obj = freeling_processing(document=string_data, language='es')
    st.write(obj[0])




