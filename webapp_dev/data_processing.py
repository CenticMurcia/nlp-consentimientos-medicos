import json
import time
import unicodedata

import altair as alt
import grequests
import requests
import streamlit as st

import legibilidad


def create_freeling_request(document='4111_OR_ES.txt', language='es',
                            batch=False):
    print(f"Cache miss -> create_freeling_requests()")
    if language == 'Español':
        language = 'es'
    elif language == 'Inglés':
        language = 'en'
    elif language == 'Francés':
        language = 'fr'
    elif language == 'Alemán':
        language = 'de'
    elif language == 'Portugués':
        language = 'pt'
    else:
        language = 'ca'

    request_data = {'username': st.secrets['api_username'],
                    'password': st.secrets['api_passwd'],
                    'text_input': document,
                    'language': language,
                    'output': 'json',
                    'interactive': '1'}

    url = 'http://frodo.lsi.upc.edu:8080/TextWS/textservlet/ws/processQuery/morpho'
    if batch:
        r = grequests.post(url, files=request_data)
    else:
        r = requests.post(url, files=request_data, timeout=15)
    return r


@st.experimental_memo(show_spinner=False)
def extract_metrics(freeling, text, filename):
    print(f"Cache miss -> extract_metrics()")
    """Returns all the requested metrics for a text"""
    metrics = {'name': filename}
    # General Metrics

    # - Number of sentences in text
    words = [words for sentence in freeling for words in sentence]
    metrics['total_sentences'] = len(freeling)

    # -Number of chars in text
    metrics['total_chars'] = sum([len(word['form']) for word in words])
    # - Number of syllables on text
    metrics['total_syllables'] = legibilidad.count_all_syllables(text)
    # - Number of words in text (tokens)
    metrics['total_words'] = len(words)
    # - Number of words per types in text
    metrics['total_unique_words'] = len(set([word['form'] for word in words]))
    # Time to read
    metrics['read_fast_time'] = metrics['total_words'] / 350
    metrics['read_medium_time'] = metrics['total_words'] / 250
    metrics['read_slow_time'] = metrics['total_words'] / 150

    # Fernandez Huerta Index
    metrics['fernandez_huerta'] = legibilidad.fernandez_huerta(text)

    # Comprehensibility index
    metrics['gutierrez'] = legibilidad.gutierrez(text)

    # Morphological metrics
    metrics = metrics | morphological_metrics(freeling)
    return metrics


def sum_words(index, char, iterator):
    """Sums the number of elements in an iterator given the
    letter to take into account

    index: int
    char: string
    iterator: iterable
    """
    return sum(1 for _ in filter(lambda tag: tag[index] == char, iterator))


def count_nouns(noun_tags):
    nouns = {'noun_counts': len(noun_tags),
             'common_noun_count': sum_words(1, 'C', noun_tags),
             'proper_noun_count': sum_words(1, 'P', noun_tags),
             'person_noun_count': sum_words(4, 'S', noun_tags),
             'location_noun_count': sum_words(4, 'G', noun_tags),
             'organization_noun_count': sum_words(4, 'O', noun_tags),
             'other_noun_count': sum_words(4, 'V', noun_tags)}

    return nouns


def count_adjectives(adjective_tags):
    adjectives = {'adjectives_total': len(adjective_tags),
                  'ordinal_adjectives': sum_words(1, 'O', adjective_tags),
                  'calificative_adjectives': sum_words(1, 'Q', adjective_tags),
                  'possesive_adjectives': sum_words(1, 'P', adjective_tags)}

    return adjectives


def count_conjuctions(conjunction_tags):
    conjuctions = {'conjuction_total': len(conjunction_tags),
                   'coordinative_conjuctions': sum_words(1, 'C',
                                                         conjunction_tags),
                   'subordinates_conjuctions': sum_words(1, 'S',
                                                         conjunction_tags)}

    return conjuctions


def count_adverbs(adverb_tags):
    adverbs = {'adverbs_total': len(adverb_tags),
               'negative_adverbs': sum_words(1, 'N', adverb_tags),
               'general_adverbs': sum_words(1, 'G', adverb_tags)}

    return adverbs


def count_verbs(verb_tags):
    verbs = {'verbs_total': len(verb_tags),
             'main_verbs': sum_words(1, 'M', verb_tags),
             'auxiliary_verbs': sum_words(1, 'A', verb_tags),
             'semiauxiliary_verbs': sum_words(1, 'S', verb_tags),
             'indicative_verbs': sum_words(2, 'I', verb_tags),
             'subjunctive_verbs': sum_words(2, 'S', verb_tags),
             'imperative_verbs': sum_words(2, 'M', verb_tags),
             'participle_verbs': sum_words(2, 'P', verb_tags),
             'gerund_verbs': sum_words(2, 'G', verb_tags),
             'infinitive_verbs': sum_words(2, 'N', verb_tags),
             'present_verbs': sum_words(3, 'P', verb_tags),
             'imperfect_verbs': sum_words(3, 'I', verb_tags),
             'future_verbs': sum_words(3, 'F', verb_tags),
             'past_verbs': sum_words(3, 'S', verb_tags),
             'conditional_verbs': sum_words(3, 'c', verb_tags)}

    return verbs


def count_determiners(determiner_tags):
    determiners = {'determiner_total': len(determiner_tags),
                   'articles_determiners': sum_words(1, 'A', determiner_tags),
                   'demostrative_determiners': sum_words(1, 'D',
                                                         determiner_tags),
                   'undefined_determiners': sum_words(1, 'I', determiner_tags),
                   'possesive_determiners': sum_words(1, 'P', determiner_tags),
                   'interrogative_determiners': sum_words(1, 'T',
                                                          determiner_tags),
                   'exclamative_determiners': sum_words(1, 'E',
                                                        determiner_tags)}

    return determiners


def count_pronouns(pronoun_tags):
    pronouns = {'pronouns_total': len(pronoun_tags),
                'fp_pronouns': sum_words(2, '1', pronoun_tags),
                'sp_pronouns': sum_words(2, '2', pronoun_tags),
                'tp_pronouns': sum_words(2, '3', pronoun_tags)}

    return pronouns


def morphological_metrics(document):
    """Extracts the number of nouns, verbs, adjectives, etc"""
    # For reference, check
    # https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-es/

    # Get all tags
    elements = [word for sentence in document for word in sentence]
    tags = list(map(lambda word: word['tag'], elements))

    # Filter by categories
    noun_tags = list(filter(lambda tag: tag[0] == 'N', tags))
    adjective_tags = list(filter(lambda tag: tag[0] == 'A', tags))
    conjunction_tags = list(filter(lambda tag: tag[0] == 'C', tags))
    adverb_tags = list(filter(lambda tag: tag[0] == 'R', tags))
    verb_tags = list(filter(lambda tag: tag[0] == 'V', tags))
    determiner_tags = list(filter(lambda tag: tag[0] == 'D', tags))
    pronoun_tags = list(filter(lambda tag: tag[0] == 'P', tags))

    # Nouns
    nouns = count_nouns(noun_tags)

    # Adjectives
    adjectives = count_adjectives(adjective_tags)

    # Conjuctions
    conjuctions = count_conjuctions(conjunction_tags)

    # Adverbs
    adverbs = count_adverbs(adverb_tags)

    # Verbs
    verbs = count_verbs(verb_tags)

    # Determiner
    determiners = count_determiners(determiner_tags)

    # Pronouns
    pronouns = count_pronouns(pronoun_tags)

    morpho_count = {**nouns, **adjectives, **conjuctions, **adverbs, **verbs,
                    **determiners, **pronouns}
    return morpho_count


def read_file(file):
    # Read the files as 'utf-8' or 'latin-1'
    try:
        string_data = file.getvalue().decode('utf-8')
    except UnicodeDecodeError:
        try:
            string_data = file.getvalue().decode('latin-1')
        except UnicodeDecodeError:
            raise UnicodeError('File is not encoded as UTF-8 or Latin-1')

    # Chars can be codified as 'a´' o 'á'
    # Freeling takes 'a´' as separated characters and
    # break words because of this
    string_data = unicodedata.normalize("NFC", string_data)
    return string_data


def clean_json(json_file):
    return [sentence['tokens'] for paragraph in json_file['paragraphs'] for
            sentence in paragraph['sentences']]


@st.experimental_memo(show_spinner=False, ttl=60 * 60 * 3)
def freeling_processing(files, selected_language='es'):
    print(f"Cache miss -> freeling_processing()")
    """Recieves a collection of files and creates async requests to the
    freeling API. Returns a list of tuples with a json object containig the
    morphological analysis and the original name of file.

    :param files: a collection of texts
    :param selected_language: language in which process the text (es, cat)
    """
    names = []
    requests_list = []
    strings = []
    server_not_up = True
    retries = 0
    for uploaded_file in files:
        try:
            string_data = read_file(uploaded_file)
        except UnicodeError:
            raise UnicodeError(f'''File **{uploaded_file.name}** is not
                    encoded in UTF-8 or Latin-1''')

        with st.spinner('Conectando al servidor freeling...'):
            if server_not_up:
                while server_not_up and retries < 5:
                    request = create_freeling_request(document=string_data,
                                                      language=selected_language)
                    if 500 <= request.status_code <= 600:
                        retries += 1
                        time.sleep(15)
                    else:
                        server_not_up = False

                if server_not_up:
                    raise Exception(
                        f'El servidor de Freeling no está disponible '
                        f'en este momento. No es posible procesar '
                        f'los ficheros. Inténtelo de nuevo más tarde.')

        request = create_freeling_request(document=string_data,
                                          language=selected_language,
                                          batch=True)
        strings.append(string_data)
        names.append(uploaded_file.name)
        requests_list.append(request)

    # Collection containing an object for every file the
    # morphological_analysis. Transforming it to a json...
    with st.spinner('Procesando ficheros en freeling...'):
        morphological_analysis = grequests.map(requests_list)

        morphological_jsons = [clean_json(json.loads(element.text)) for element
                               in morphological_analysis]
    return zip(morphological_jsons, strings, names)


def plot_selection(data):
    graphic = (alt.Chart(data).encode(
        x=data.columns[0],
        y=data.columns[1],
        tooltip=['name', data.columns[0], data.columns[1]]
    ).mark_circle(opacity=0.5,
                  size=50,
                  color='red',
                  ).interactive())
    return graphic


def plot_pca(data):
    data.reset_index(level=0, inplace=True, drop=False)
    graphic = (alt.Chart(data).encode(
        x=data.columns[1],
        y=data.columns[2],
        tooltip=['name', data.columns[1], data.columns[2]]
    ).mark_circle(opacity=0.5,
                  size=50,
                  color='red',
                  ).interactive())
    return graphic


def plot_components(data, component: int = 1):
    data = data.transpose()
    data.reset_index(inplace=True)
    data = data.melt(id_vars=['index'])
    data.sort_values(by=['index', 'value'], inplace=True,
                     ascending=[True, False])
    data = data[data['index'] == f'Componente {component}']
    graphic = (alt.Chart(data).mark_bar(color='red', opacity=0.5).encode(
        x='value',
        y=alt.Y('variable', sort='-x'),
        tooltip=['value']
    ).interactive())
    return graphic
