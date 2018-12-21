import json
from configparser import ConfigParser

from bson import json_util
from pandas.io.json import json_normalize
from pymongo import MongoClient

config_parser = ConfigParser()
config_parser.read('../config/reader-config.ini', encoding='utf-8')

mongo_client = MongoClient(config_parser.get('mongo', 'host'), int(config_parser.get('mongo', 'port')))
tweets = mongo_client[config_parser.get('mongo', 'db')][config_parser.get('mongo', 'collection')]
data = tweets.find({})

# load MongoDB data as JSON data and flatten using json_normalize
sanitized = json.loads(json_util.dumps(data))

# replace new line with space
for i, j in enumerate(sanitized):
    j['text'] = '"' + j['text'].strip().replace("\n", " ") + '"'

normalized = json_normalize(sanitized)
normalized.to_csv(
    path_or_buf="../../../data-set/data-set.csv",
    columns=[column.strip() for column in config_parser.get('csv', 'columns').split(',')],
    encoding="utf-8",
    index_label="instance_id"
)

for i, j in enumerate(sanitized):
    print(i, j['id'], j['user']['screen_name'], j['truncated'], j['text'])
