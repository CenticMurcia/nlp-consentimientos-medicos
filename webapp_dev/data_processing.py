from time import perf_counter
from unicodedata import normalize

import requests
import streamlit as st

import data_processing as dp


@st.cache(show_spinner=False)
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
    i1 = perf_counter()
    url = "http://www.corpus.unam.mx/servicio-freeling/analyze.php"
    r = requests.post(url, files=files, params=params)
    # Response to json
    obj = r.json()
    i2 = perf_counter()
    print(f"Freeling time processing for document: {i2-i1:0.5f}")

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


def sum_words(index, char, iterator):
    """Sums the number of elements in an iterator given the
    letter to take into account

    index: int
    char: string
    iterator: iterable
    """
    return sum(1 for word in
               filter(lambda tag: tag[index] == char, iterator))


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

    # Nouns
    nouns_count = len(noun_tags)
    common_noun_count = sum_words(1, 'C', noun_tags)
    proper_noun_count = sum_words(1, 'P', noun_tags)
    person_noun_count = sum_words(4, 'S', noun_tags)
    location_noun_count = sum_words(4, 'G', noun_tags)
    organization_noun_count = sum_words(4, 'O', noun_tags)
    other_noun_count = sum_words(4, 'V', noun_tags)

    # Adjectives
    adjectives_total = len(adjective_tags)
    ordinal_adjectives = sum_words(1, 'O', adjective_tags)
    calificative_adjectives = sum_words(1, 'Q', adjective_tags)
    possesive_adjectives = sum_words(1, 'P', adjective_tags)

    # Conjuctions
    conjuction_total = len(conjunction_tags)
    coordinative_conjuctions = sum_words(1, 'C', conjunction_tags)
    subordinates_conjuctions = sum_words(1, 'S', conjunction_tags)

    # Adverbs
    adverbs_total = len(adverb_tags)
    negative_adverbs = sum_words(1, 'N', adverb_tags)
    general_adverbs = sum_words(1, 'G', adverb_tags)

    # Verbs
    verbs_total = len(verb_tags)
    negative_verbs = sum_words(1, 'N', verb_tags)
    general_verbs = sum_words(1, 'G', verb_tags)

    # Determiner
    determiner_total = len(determiner_tags)
    articles_determiners = sum_words(1, 'A', determiner_tags)
    demostrative_determiners = sum_words(1, 'D', determiner_tags)
    undefined_determiners = sum_words(1, 'I', determiner_tags)
    possesive_determiners = sum_words(1, 'P', determiner_tags)
    interrogative_determiners = sum_words(1, 'T', determiner_tags)
    exclamative_determiners = sum_words(1, 'E', determiner_tags)

    # Pronouns
    pronouns_total = len(pronoun_tags)
    fp_pronouns = sum_words(2, '1', pronoun_tags)
    sp_pronouns = sum_words(2, '2', pronoun_tags)
    th_pronouns = sum_words(2, '3', pronoun_tags)

    i2 = perf_counter()
    print(f"Tiempo de procesamiento morfologico: {i2-i1:0.6f}")
    return morpho_count


def read_file(file):
    # Read the files as 'utf-8' or 'latin-1'
    string_data = None
    try:
        string_data = file.getvalue().decode('utf-8')
    except UnicodeDecodeError:
        print('File is not UTF-8. Trying with Latin-1...')

        try:
            string_data = file.getvalue().decode('latin-1')
        except UnicodeDecodeError:
            raise UnicodeError('File is not encoded as UTF-8 or Latin-1')

    # Chars can be codified as 'a´' o 'á'
    # Freeling takes 'a´' as separated characters and
    # break words because of this
    string_data = dp.normalize("NFC", string_data)
    return string_data
