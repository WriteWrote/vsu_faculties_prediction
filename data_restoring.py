stoppunkt = None
stemmer = None
stopwords = None
nlp = None

N_DIM = 25

def read_lines(path: str):
    lines = []
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
    file.close()
    return lines


def clean_with_isalpha(word):
    return "".join(c for c in word if c.isalpha())


def clean_chinese(text):
    return "".join(c for c in text if "A" <= c <= "Z" or "a" <= c <= "z" or "А" <= c <= "Я" or "а" <= c <= "я")


def clean_bag_of_words(unit):
    global i
    unit_words = unit
    i = i + 1
    try:
        unit_words = [w.lower() for w in unit_words]
        unit_words = [clean_with_isalpha(w) for w in unit_words]
        unit_words = [clean_chinese(w) for w in unit_words]
        unit_words = [w for w in unit_words if len(w) > 2]
        unit_words = [[token.lemma_ for token in nlp(w)] for w in unit_words]
        unit_words = [stemmer.stem(w[0]) for w in unit_words]
    except Exception:
        print('catched exception with: ' + str(i))
    print(len(unit_words))
    return unit_words


def vectorize(word, model):
    try:
        return model.wv[word]
    except Exception as e:
        print(word)
        return [0] * 25


def vectorize_words_bag(word_list, model):
    word_vectors = []

    try:
        word_vectors = [vectorize(word, model) for word in word_list if word in model.wv]
    except Exception:
        print('catched exception with: ' + str(word_list))

    return word_vectors


def sum_word_vectors(word_vectors):
    if len(word_vectors) == 0:
        return [0] * N_DIM
    return sum(word_vectors) / len(word_vectors)


def process_group_names(full_data: list, word2vec):
    result = []
    [result.extend(group[1].split(" ")) for group in full_data]
    result = clean_bag_of_words(result)
    result = vectorize_words_bag(result, word2vec)
    result = sum_word_vectors(result)
    return result
