import streamlit as st
import requests
from unicodedata import normalize
import data_processing as dp


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
