import asyncio
import logging
import time
import json
import aiohttp
import requests
import streamlit as st

from data_processing import read_file


@st.experimental_memo(show_spinner=False)
def freeling_processing(files, language):
    logging.info(f"Cache miss -> freeling_processing()")
    """Recieves a collection of files and creates async requests to the
    freeling API. Returns a list of tuples with a json object containig the
    morphological analysis and the original name of file.

    :param files: a collection of texts
    :param selected_language: language in which process the text (es, cat)
    """
    # First try to connect to the server
    with st.spinner('Conectando al servidor freeling. Esto podría '
                    'tardar unos segundos...'):
        connect_server()

    names = []
    strings = []

    for uploaded_file in files:
        try:
            string_data = read_file(uploaded_file)
        except UnicodeError:
            raise UnicodeError(f'''File **{uploaded_file.name}** is not
                    encoded in UTF-8 or Latin-1''')

        strings.append(string_data)
        names.append(uploaded_file.name)
    # Collection containing an object for every file the
    # morphological_analysis. Transforming it to a json...
    with st.spinner('Procesando ficheros en freeling...'):
        morphological_analysis = asyncio.run(freeling_requests(strings, names,
                                                               language))
        morphological_jsons = [clean_json(json.loads(element)) for element
                               in morphological_analysis]
    return zip(morphological_jsons, strings, names)


def get_tasks(session: aiohttp.ClientSession, files, language):
    tasks = []
    url = 'http://frodo.lsi.upc.edu:8080/TextWS/textservlet/ws/processQuery/morpho'
    for document, filename in files:
        data = aiohttp.FormData()

        data.add_field('username', st.secrets['api_username'])
        data.add_field('password', st.secrets['api_passwd'])
        data.add_field('filename', filename, filename=filename)
        data.add_field('text_input', document)
        data.add_field('language', language)
        data.add_field('output', 'json')
        data.add_field('interactive', '1')

        tasks.append(session.post(url, data=data))
    return tasks


async def freeling_requests(strings, filenames, language='es'):
    logging.info(f"Cache miss -> create_freeling_requests()")
    timeout = aiohttp.ClientTimeout()
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = get_tasks(session, zip(strings, filenames), language)
        responses = await asyncio.gather(*tasks)
        results = []
        for response in responses:
            results.append(await response.text())
    return results


def clean_json(json_file):
    return [sentence['tokens'] for paragraph in json_file['paragraphs'] for
            sentence in paragraph['sentences']]


def connect_server():
    retries = 0
    server_up = False
    while not server_up and retries < 5:
        request = check_server()
        if not request:
            retries += 1
            time.sleep(20)
        else:
            server_up = True

    if not server_up:
        raise Exception(
            f'El servidor de Freeling no está disponible '
            f'en este momento. No es posible procesar '
            f'los ficheros. Inténtelo de nuevo más tarde.')


def check_server():
    request_data = {'username': st.secrets['api_username'],
                    'password': st.secrets['api_passwd'],
                    'filename': 'File',
                    'text_input': 'Test',
                    'language': 'es',
                    'output': 'json',
                    'interactive': '1'}
    url = 'http://frodo.lsi.upc.edu:8080/TextWS/textservlet/ws/processQuery/morpho'
    resp = requests.post(url, files=request_data)
    return resp
