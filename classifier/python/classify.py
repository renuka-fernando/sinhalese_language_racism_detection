import pandas as pd

data_frame = pd.read_csv("../../data-set/data-set.csv")
data_set = data_frame.values

# for id, tweet in enumerate(data_set[:, -1]):
#     print(id, tweet)

for id, tweet in enumerate(data_frame.text):
    print(id, tweet)