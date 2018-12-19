import logging
import pandas as pd

from classifier.utils import tokenize_corpus, build_dictionary, transform_to_dictionary_values
from classifier.data_set_constants import *

logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s', level=logging.INFO)
data_frame = pd.read_csv("../../../data-set/final-data-set.csv")
data_set = data_frame.values

# for id, tweet in enumerate(data_set[:, :]):
#     print(id, tweet[-1])

# for index, tweet in enumerate(data_frame.text):
#     print(index, tweet)

logging.info("Tokenizing the corpus")
corpus_token = tokenize_corpus(data_set[:, DATA_SET_TEXT])

logging.info("Building the dictionary")
dictionary = build_dictionary(corpus_token)

logging.info("Transforming the corpus to dictionary values")
x_corpus = transform_to_dictionary_values(corpus_token, dictionary)

print(x_corpus)
