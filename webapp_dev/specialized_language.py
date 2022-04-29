#
#     # Frequent
#     self.frequent_tokens = self.__process_lists__(
#         '../data/vocab-lists/ES-10000_tokens_mas_frec_(UTF8).txt')
#
# elif self.language == 'ca':
#     # Frequent
#     self.frequent_tokens = process_lists(
#         '../data/vocab-lists/CA-8000_tokens_mas_frec_(UTF8).txt')


def process_lists(file):
    with open(file, "r") as f:
        content_list = f.read().splitlines()
        return list(map(str.rstrip, content_list))


def count_legal_language(text, language):
    legal_tokens = None
    if language == 'ca':
        return 0
    if language == 'es':
        legal_tokens = process_lists(
            '../data/vocab-lists/ES-legal-penal(UTF8).txt')
    return sum([text.count(word) for word in legal_tokens])


def count_medical_language(text, language):
    medical_tokens = None
    if language == 'ca':
        medical_tokens = process_lists('../data/vocab-lists/CA-med(UTF8).txt')
    if language == 'es':
        medical_tokens = process_lists('../data/vocab-lists/ES-med(UTF8).txt')
    return sum([text.count(word) for word in medical_tokens])
