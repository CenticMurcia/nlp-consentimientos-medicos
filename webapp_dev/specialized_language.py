class SpecialicedLanguage:

    def __init__(self, language):
        # Store language code in uppercase to read files
        self.language = language.upper()
        self.frequent_tokens = None
        self.medical_tokens = None
        self.legal_tokens = None

        if self.language == 'ES':
            # Legal
            self.legal_tokens = self.__process_lists__(
                '../data/vocab-lists/ES-legal-penal(UTF8).txt')
            # Frequent
            self.frequent_tokens = self.__process_lists__(
                '../data/vocab-lists/ES-10000_tokens_mas_frec_(UTF8).txt')
            # Medical
            self.medical_tokens = self.__process_lists__(
                '../data/vocab-lists/ES-med(UTF8).txt')

        elif self.language == 'CA':
            # Frequent
            self.frequent_tokens = self.__process_lists__(
                '../data/vocab-lists/CA-8000_tokens_mas_frec_(UTF8).txt')
            # Medical
            self.medical_tokens = self.__process_lists__(
                '../data/vocab-lists/CA-med(UTF8).txt')

    @staticmethod
    def __process_lists__(file):
        with open(file, "r") as f:
            content_list = f.read().splitlines()
            return list(map(str.rstrip, content_list))

    def count_legal_language(self, text):
        return sum([text.count(word) for word in self.legal_tokens])

    def count_medical_language(self, text):
        return sum([text.count(word) for word in self.medical_tokens])
