import logging
import time

import grequests
import requests
import streamlit as st

from data_processing import transform_language, read_file


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
    requests_list = []
    strings = []

    for uploaded_file in files:
        try:
            string_data = read_file(uploaded_file)
        except UnicodeError:
            raise UnicodeError(f'''File **{uploaded_file.name}** is not
                    encoded in UTF-8 or Latin-1''')

        request = create_freeling_request(document=string_data,
                                          filename=uploaded_file.name,
                                          language=language,
                                          async_req=True)
        strings.append(string_data)
        names.append(uploaded_file.name)
        requests_list.append(request)

    # Collection containing an object for every file the
    # morphological_analysis. Transforming it to a json...
    with st.spinner('Procesando ficheros en freeling...'):
        time1 = time.perf_counter()
        morphological_analysis = grequests.imap(requests_list, size=10,
                                                exception_handler=handler)
        morphological_jsons = [clean_json(element.json()) for element
                               in morphological_analysis]
    time2 = time.perf_counter()
    logging.info(time2-time1)
    return zip(morphological_jsons, strings, names)


def handler(request, exception):
    print(exception)
    print(request)


def connect_server():
    retries = 0
    server_up = False
    while not server_up and retries < 5:
        request = create_freeling_request(
            document='Test',
            language='es')
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


def create_freeling_request(document, filename='4088.txt', language='es',
                            async_req=False):
    logging.info(f"Cache miss -> create_freeling_requests()")

    language = transform_language(language)
    request_data = {'username': st.secrets['api_username'],
                    'password': st.secrets['api_passwd'],
                    'filename': filename,
                    'text_input': document,
                    'language': language,
                    'output': 'json',
                    'interactive': '1'}

    url = 'http://frodo.lsi.upc.edu:8080/TextWS/textservlet/ws/processQuery/morpho'
    if async_req:
        r = grequests.post(url, files=request_data)
    else:
        r = requests.post(url, files=request_data)
    return r


def clean_json(json_file):
    return [sentence['tokens'] for paragraph in json_file['paragraphs'] for
            sentence in paragraph['sentences']]
