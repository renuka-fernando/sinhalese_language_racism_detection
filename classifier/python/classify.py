from subprocess import Popen, PIPE
import pandas as pd

data_frame = pd.read_csv("../../data-set/data-set.csv")
data_set = data_frame.values

for id, tweet in enumerate(data_set[:,-1]):
    if "ේ" + "්" in tweet:
        print(id, tweet)

tokenizer_cmd = ['java','SinhalaTokenizer', '1', '2', '3', '4']
tokenizer = Popen(tokenizer_cmd, stdin=PIPE, stdout=PIPE)
tok_text, _ = tokenizer.communicate(" අමාත්‍යාංශ ලේකම් එච්. එම්. ගුණසේකර මහතා හා Renuka ඔහු අමාත්‍යාංශයට කැඳවා පරීක්‌ෂා කර තිබේ".encode("utf-8"))
print(tok_text.decode("utf-8", "ignore"))