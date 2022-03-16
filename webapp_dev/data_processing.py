import streamlit as st
import requests
from unicodedata import normalize
import data_processing as dp
from time import perf_counter


@st.cache
def freeling_processing(document='4111_OR_ES.txt',
                        language='Español'):
    # File to send
    file = document
    files = {'file': file}
    # Parameters
    if language == 'Español':
        language = 'es'
    else:
        language = 'cat'
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

    # -Number of chars in text
    n_chars = sum([len(word['token'])
                  for phrase in document for word in phrase])
    # - Number of syllables on text
    # Nope
    # - Number of words in text (tokens)
    n_words = len([word for phrase in document for word in phrase])
    # - Number of words per types in text
    n_unique_words = len(set([word['token']
                         for phrase in document for word in phrase]))
    # - Number of sentences in text
    n_phrases = len([phrase for phrase in document])
    return n_chars, n_words, n_unique_words, n_phrases


def example(index, char, iterator):
    return sum(1 for _ in filter(lambda tag: tag[index] == char, iterator))

def morphological_metrics(document):
    """Extracts the number of nouns, verbs, adjectives, etc"""

    # Get all tags
    morpho_count = {}
    i1 = perf_counter()
    elements = []
    for phrase in document:
        elements += phrase

    tags = list(map(lambda word: word['tag'], elements))

    # Filter by categories
    noun_tags = list(filter(lambda tag: tag[0] == 'N', tags))
    adjective_tags = list(filter(lambda tag: tag[0] == 'A', tags))
    conjunction_tags = list(filter(lambda tag: tag[0] == 'C', tags))
    adverb_tags = list(filter(lambda tag: tag[0] == 'R', tags))
    verb_tags = list(filter(lambda tag: tag[0] == 'V', tags))
    determiner_tags = list(filter(lambda tag: tag[0] == 'D', tags))
    pronoun_tags = list(filter(lambda tag: tag[0] == 'P', tags))

    nouns_count = len(noun_tags)
    common_noun_count = sum(1 for _ in filter(lambda tag: tag[1] == 'C', noun_tags))
    proper_noun_count = sum(1 for _ in filter(lambda tag: tag[1] == 'P', noun_tags))
    i2 = perf_counter()
    print(f"Tiempo de procesamiento morfologico: {i2-i1:0.6f}")
    return morpho_count


def read_file(file):
    # Read the files as 'utf-8' or 'latin-1'
    string_data = None
    try:
        string_data = file.getvalue().decode('utf-8')
    except UnicodeDecodeError:
        print('File is not UTF-8. Trying with Latin-1')

        try:
            string_data = file.getvalue().decode('latin-1')
        except:
            print('File encoding is not supported')

    # Chars can be codified as 'a´' o 'á'
    # Let's transform all of them to "á", because Freeling takes 'a´'
    # as separated chars and break words because of this
    string_data = dp.normalize("NFC", string_data)
    return string_data
