import streamlit
import requests

#Archivo a ser enviado
files = {'file': open('../data/SP - January - 2021 - Txt files/4111_OR_ES.txt', 'rb')}
#Parámetros
params = {'outf': 'tagged', 'format': 'json', 'lang': 'es'}
#Enviar petición
url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
r = requests.post(url, files=files, params=params)
#Convertir de formato json
obj = r.json()

# Ejemplo, obtener todos los lemas
# for sentence in obj:
#     for word in sentence:
#         print(word)


