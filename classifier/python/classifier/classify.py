import pandas as pd

from classifier.utils import tokenize_corpus
from classifier.data_set_constants import *

data_frame = pd.read_csv("../../../data-set/final-data-set.csv")
data_set = data_frame.values

# for id, tweet in enumerate(data_set[:, :]):
#     print(id, tweet[-1])

# for index, tweet in enumerate(data_frame.text):
#     print(index, tweet)

corpus_token = tokenize_corpus(data_set[:, DATA_SET_TEXT])
print(corpus_token)