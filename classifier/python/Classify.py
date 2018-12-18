import pandas as pd
import DataSetConstants

data_frame = pd.read_csv("../../data-set/final-data-set.csv")
data_set = data_frame.values

for id, tweet in enumerate(data_set[:, :]):
    print(id, tweet[-1])

# for index, tweet in enumerate(data_frame.text):
#     print(index, tweet)
