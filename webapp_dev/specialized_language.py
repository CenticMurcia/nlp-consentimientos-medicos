import collections
import re


def process_lists(file):
    with open(file, "r") as f:
        content_list = f.read().splitlines()
        return list(map(str.rstrip, content_list))


def count_legal_language(text, language):
    if language == 'es':
        legal_tokens = process_lists(
            './data/vocab-lists/ES-legal-penal(UTF8).txt')
    else:
        return 0
    return sum(1 for word in legal_tokens for _ in
               re.finditer(r'\b%s\b' % re.escape(word), text, re.IGNORECASE))


def count_medical_language(text, language):
    if language == 'ca':
        medical_tokens = process_lists('./data/vocab-lists/CA-med(UTF8).txt')
    elif language == 'es':
        medical_tokens = process_lists('./data/vocab-lists/ES-med(UTF8).txt')
    else:
        return 0
    return sum(1 for word in medical_tokens for _ in
               re.finditer(r'\b%s\b' % re.escape(word), text, re.IGNORECASE))


def count_most_common(text, language):
    if language == 'ca':
        most_common_tokens = process_lists(
            './data/vocab-lists/CA-8000_tokens_mas_frec_(UTF8).txt')
    elif language == 'es':
        most_common_tokens = process_lists(
            './data/vocab-lists/ES-10000_tokens_mas_frec_(UTF8).txt')
    else:
        return 0

    text_words = collections.Counter(re.split(r'\W+', text.lower()))
    # 1K
    count_1k = sum(filter(None, (text_words.get(word) for word in
                                 most_common_tokens[:1000])))
    # count_1k = sum(1 for word in most_common_tokens[:1000] for _ in
    #                re.finditer(r'\b%s\b' % re.escape(word), text,
    #                            re.IGNORECASE))

    # 1k 5k
    count_1k_5k = sum(filter(None, (text_words.get(word) for word in
                                    most_common_tokens[1000:5000])))
    # 5k  ...
    count_5k_10k = sum(filter(None, (text_words.get(word) for word in
                                     most_common_tokens[5000:])))

    return count_1k, count_1k_5k, count_5k_10k
