import json
from configparser import ConfigParser

from bson import json_util
from pandas.io.json import json_normalize
from pymongo import MongoClient

config = ConfigParser()
config.read('./config/reader-config.ini')

mongo_client = MongoClient(config.get('mongo', 'host'), int(config.get('mongo', 'port')))
tweets = mongo_client.db.tweets
data = tweets.find({})

# load MongoDB data as JSON data and flatten using json_normalize
sanitized = json.loads(json_util.dumps(data))
normalized = json_normalize(sanitized)

normalized.to_csv(path_or_buf="../../data-set/data-set.csv", columns=['id','user.id', 'text'], encoding="utf-8", index_label="instance_id")

for i, j in enumerate(sanitized):
    print(i, j['text'])
