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


@st.cache(show_spinner=False)
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


def count_nouns(noun_tags):
    nouns = {}
    nouns['noun_counts'] = len(noun_tags)
    nouns['common_noun_count'] = sum_words(1, 'C', noun_tags)
    nouns['proper_noun_count'] = sum_words(1, 'P', noun_tags)
    nouns['person_noun_count'] = sum_words(4, 'S', noun_tags)
    nouns['location_noun_count'] = sum_words(4, 'G', noun_tags)
    nouns['organization_noun_count'] = sum_words(4, 'O', noun_tags)
    nouns['other_noun_count'] = sum_words(4, 'V', noun_tags)

    return nouns


def count_adjectives(adjective_tags):
    adjectives = {}
    adjectives['adjectives_total'] = len(adjective_tags)
    adjectives['ordinal_adjectives'] = sum_words(1, 'O', adjective_tags)
    adjectives['calificative_adjectives'] = sum_words(1, 'Q', adjective_tags)
    adjectives['possesive_adjectives'] = sum_words(1, 'P', adjective_tags)

    return adjectives


def count_conjuctions(conjunction_tags):
    conjuctions = {}
    conjuction_total = len(conjunction_tags)
    coordinative_conjuctions = sum_words(1, 'C', conjunction_tags)
    subordinates_conjuctions = sum_words(1, 'S', conjunction_tags)

    return conjuctions


def count_adverbs(adverb_tags):
    adverbs = {}
    adverbs['adverbs_total'] = len(adverb_tags)
    adverbs['negative_adverbs'] = sum_words(1, 'N', adverb_tags)
    adverbs['general_adverbs'] = sum_words(1, 'G', adverb_tags)

    return adverbs


def count_verbs(verb_tags):
    verbs = {}
    # TODO Finish counting of verbs
    verbs['verbs_total'] = len(verb_tags)
    verbs['main_verbs'] = sum_words(1, 'M', verb_tags)
    verbs['auxiliary_verbs'] = sum_words(1, 'A', verb_tags)
    verbs['semiauxiliary_verbs'] = sum_words(1, 'S', verb_tags)
    verbs['indicative_verbs'] = sum_words(2, 'I', verb_tags)
    verbs['subjunctive_verbs'] = sum_words(2, 'S', verb_tags)
    verbs['imperative_verbs'] = sum_words(2, 'M', verb_tags)
    verbs['participle_verbs'] = sum_words(2, 'P', verb_tags)
    verbs['gerund_verbs'] = sum_words(2, 'G', verb_tags)
    verbs['infinitive_verbs'] = sum_words(2, 'N', verb_tags)
    verbs['present_verbs'] = sum_words(3, 'P', verb_tags)
    verbs['imperfect_verbs'] = sum_words(3, 'I', verb_tags)
    verbs['future_verbs'] = sum_words(3, 'F', verb_tags)
    verbs['past_verbs'] = sum_words(3, 'S', verb_tags)
    verbs['conditional_verbs'] = sum_words(3, 'c', verb_tags)

    return verbs


def count_determiners(determiner_tags):
    determiners = {}
    determiners['determiner_total'] = len(determiner_tags)
    determiners['articles_determiners'] = sum_words(1, 'A', determiner_tags)
    determiners['demostrative_determiners'] = sum_words(
        1, 'D', determiner_tags)
    determiners['undefined_determiners'] = sum_words(1, 'I', determiner_tags)
    determiners['possesive_determiners'] = sum_words(1, 'P', determiner_tags)
    determiners['interrogative_determiners'] = sum_words(
        1, 'T', determiner_tags)
    determiners['exclamative_determiners'] = sum_words(1, 'E', determiner_tags)

    return determiners


def count_pronouns(pronoun_tags):
    pronouns = {}
    pronouns['pronouns_total'] = len(pronoun_tags)
    pronouns['fp_pronouns'] = sum_words(2, '1', pronoun_tags)
    pronouns['sp_pronouns'] = sum_words(2, '2', pronoun_tags)
    pronouns['tp_pronouns'] = sum_words(2, '3', pronoun_tags)

    return pronouns


def morphological_metrics(document):
    """Extracts the number of nouns, verbs, adjectives, etc"""

    # Get all tags
    i1 = perf_counter()
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

    morpho_count = (nouns | adjectives | conjuctions |
                    adverbs | verbs | determiners | pronouns)

    i2 = perf_counter()
    print(f"Tiempo de procesamiento morfologico: {i2-i1:0.6f}")
    st.write(morpho_count)
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
