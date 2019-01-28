# Sinhalese Language based Hate Speech Detection

## 1. Background

Advances in communication technology has brought people to one global position. Among them social media platforms play a major role with granting users freedom to speech by allowing them to freely express their thoughts, beliefs, and opinions. Children, adolescents, adults are spending significant amount of time on various social networking sites to connect with others, to share information, and to pursue common interests. Although this make great opportunities such as learn from others, there are some challenges. Racism, trolling, being exposed to large amounts of offensive online contents are such examples. The rapid growth of race hate speech on social media seems to have big impact on society and goodwill of a country.

Social media is the collective of online communications channels dedicated to community-based input, interaction, content-sharing and collaboration and is a very popular way for people to express their opinions publicly. Forums, microblogging, social networking, social bookmarking, social curation, and wikis are some of different types of social media and “Facebook”, “Twitter”, “Google+”, “Wikipedia”, “LinkedIn”, “Reddit”, “Pinterest” are some examples of popular social media. While social media helps people with connecting each other, sharing knowledge regardless of location, education background, updating information around the world, it also enables the risk of people to being targeted or harassed via offensive language which may severely impact the community in general.

Sri Lanka had a same kind of problem related to social medias in March, 2018 related to an incident happened in Digana, Kandy that occurs due to failure of social media to detect of race speeches and offensive language on comments and posts since they were in Sinhala language. Current tools failed to detect such things and the temporary solution was blocking on Facebook and other social media

## 2. Requirements to Run the Code Setup

- [Python 3](https://www.python.org/download/releases/3.0/)
- [TensorFlow](https://github.com/tensorflow/tensorflow)
- [Keras](https://github.com/keras-team/keras)
- [Mongo DB](https://github.com/mongodb/mongo)
- Pymongo - `pip install pymongo`
- Pandas - `pip install pandas`
- Requests Oauthlib - `pip install requests_oauthlib`
- Emoji - `pip install emoji`

## 3. Extend the Tweet Data

### 3.1 Run the Mongo DB

Run the Mongo DB with following script.

```bash
mongod --dbpath data-set/mongo-db
```
Restore the existing Mongo DB to your environment with running the following script. But this is optional.

```bash
mongorestore [root directory]/data-set/dump
```

### 3.2 Setup Twitter Keys

Update the configuration file `twitter-api-reader/python/config/twitter-keys.ini` with your Twitter API keys.

```ini
[twitter]
client_key = <your client key>
client_secret = <your client secret>
resource_owner_key = <your resource owner key>
resource_owner_secret = <your resource owner secret>
```

### 3.3 Setup Twitter Search Query

Update the configuration file `twitter-api-reader/python/config/reader-config.ini` with Mongo DB host, port, database name and the collection name.

```ini
[mongo]
host = localhost
port = 27017
db = db
collection = tweets

[csv]
columns = id, user.id, created_at, text

[tweets]
query = බැගින් OR බැඟින් OR රකින්න OR නියමයි OR අදහස OR මුලු OR මුළු OR අධික OR පනින්න OR එයලව OR ආවාහම OR හට OR මෙන්
json_payload = {"query":"උන් OR උං OR සමහර OR අතරින් OR නැත්තම් OR මතකය","fromDate":"201803010000","toDate":"201805010000"}
```

- Use `[csv]` section to specify the columns that is used to create the csv file.
- Use `[tweets]` section to specify search query.
  - `query` is used for Standard Twitter Search API. Use `OR` to `AND` and other Tweeter operations to make query.
  - `json_payload` is used for Premium Twitter Search API. This is a JSON. You can specify `fromDate` and `toDate` to find Tweets in the range specified or any other operators that Tweeter API supports. Language may be an important operator.
    ```ini
    json_payload = {"query":"උන් lang:si OR උං lang:si OR සමහර lang:si","maxResults":"100","fromDate":"201811050000","toDate":"201812030000"}
    ```

### 3.4 Query with Tweeter

Words used to query is defined in the configurations done in the section **3.3**. Run the following script to run the `tweets_to_mongo.py` file and query with standard Twitter API. Make sure you have an internet connection and have run the Mongo DB as in section **3.1**.

```bash
cd twitter-api-reader/python/twitter; python tweets_to_mongo.py s
```

To use the premium API change the letter `s` with `p30` or `pf` at the end of the script.

- `p30` - To retrieve Tweets within 30 days.
- `pf` - To retrive any Tweet (Full Archive).

example:

```bash
cd twitter-api-reader/python/twitter; python tweets_to_mongo.py p30
```

### 3.5 Create CSV from Mongo DB

You can create a CSV file from the specified Database and Collection in the configuration file mentioned in the section **3.3**. Run the following script to create the CSV file.

```bash
cd twitter-api-reader/python/twitter; python mongo_to_csv.py
```

The created file can be found as `[root directory]/data-set/data-set.csv`. You can import this file to a spread sheet program and manually label tweets. The [**Excel file (xlsx)**](data-set/final-data-set.xlsx) used in this project can be found [here](data-set/final-data-set.xlsx). The exported CSV file from this program can be used for training the model.

Place the final CSV file as `[root directory]/data-set/final-data-set.csv`. This is used to train the model.

### 3.6. Backup Mongo DB

You can backup collected tweets by running following script.

```bash
mongodump --collection tweets --db db
```

## 4. Run the Model

### 4.1. Training the Model

Run the following script to train the model. This will start training the model. Make sure the final CSV file has been placed as `[root directory]/data-set/final-data-set.csv`.

```bash
cd classifier/python/classifier; python classify.py
```

This will create an h5 file that contains the model in a directory `[root directory]/classifier/python/classifier/results_x`.

### 4.2. Build Results

Run the following script to validate the model. This will use the final results directory to validate the model, create files associate with scores in the same directory.

```bash
cd classifier/python/classifier; python validate.py
```