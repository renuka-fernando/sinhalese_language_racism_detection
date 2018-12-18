from preprocessing.sinhalese_tokenizer import tokenize


def tokenize_corpus(corpus: list) -> list:
    return [tokenize(text) for text in corpus]
