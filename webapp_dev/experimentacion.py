from io import StringIO
import streamlit as st
import requests


def freeling_processing(document = '4111_OR_ES.txt',
                        directory = '../data/SP - January - 2021 - Txt files',
                        language = 'es'):
    #Archivo a ser enviado
    file = open(f'{directory}/{document}','rb')
    files = {'file': file}
    #Parámetros
    params = {'outf': 'tagged', 'format': 'json', 'lang': language}
    #Enviar petición
    url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
    r = requests.post(url, files=files, params=params)
    #Convertir de formato json
    obj = r.json()

    # Cerramos el fichero
    file.close()

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

uploaded_files = st.file_uploader(label= 'Tus ficheros aquí', accept_multiple_files=True, on_change=example_callback)

for uploaded_file in uploaded_files:
    string_data = uploaded_file.read()
    st.write('Fichero leido con éxito :sunglasses:')




