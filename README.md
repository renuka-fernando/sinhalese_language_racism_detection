# Sinhalese Language based Hate Speech Detection

## 1. Background

Advances in communication technology has brought people to one global position. Among them social media platforms play a major role with granting users freedom to speech by allowing them to freely express their thoughts, beliefs, and opinions. Children, adolescents, adults are spending significant amount of time on various social networking sites to connect with others, to share information, and to pursue common interests. Although this make great opportunities such as learn from others, there are some challenges. Racism, trolling, being exposed to large amounts of offensive online contents are such examples. The rapid growth of race hate speech on social media seems to have big impact on society and goodwill of a country.

Social media is the collective of online communications channels dedicated to community-based input, interaction, content-sharing and collaboration and is a very popular way for people to express their opinions publicly. Forums, microblogging, social networking, social bookmarking, social curation, and wikis are some of different types of social media and “Facebook”, “Twitter”, “Google+”, “Wikipedia”, “LinkedIn”, “Reddit”, “Pinterest” are some examples of popular social media. While social media helps people with connecting each other, sharing knowledge regardless of location, education background, updating information around the world, it also enables the risk of people to being targeted or harassed via offensive language which may severely impact the community in general.

Sri Lanka had a same kind of problem related to social medias in March, 2018 related to an incident happened in Digana, Kandy that occurs due to failure of social media to detect of race speeches and offensive language on comments and posts since they were in Sinhala language. Current tools failed to detect such things and the temporary solution was blocking on Facebook and other social media

## 2. Requirements to Run the Code Setup

- Python 3
- Mongo DB
- pymongo - `pip install pymongo`
- pandas - `pip install pandas`
- requests_oauthlib - `pip install requests_oauthlib`
- emoji - `pip install emoji`

## 3. Restore Mongo DB with Twitter Data

Restore the existing Mongo DB to your environment with running the following script.

```bash
mongod --dbpath data-set/mongo-db
mongorestore dump
```

## 4. Extend the Tweet Data

### 4.1 Run the Mongo DB

Run the following script to run the Mongo DB.

```bash
mongod --dbpath data-set/mongo-db
```

### 4.2 Setup Twitter Keys

Update the configuration file `twitter-api-reader/python/config/twitter-keys.ini` with your Twitter API keys.

```ini
[twitter]
client_key = <your client key>
client_secret = <your client secret>
resource_owner_key = <your resource owner key>
resource_owner_secret = <your resource owner secret>
```

### 4.3 Setup Twitter Search Query

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

- Use `[csv]` section to specifiy the columns that is used to create the csv file.
- Use `[tweets]` section to speicify search query.
  - `query` is used for Standard Twitter Search API. Use `OR` to `AND` and other Tweeter operations to make query.
  - `json_payload` is used for Premium Twitter Search API. This is a JSON. You can specify `fromDate` and `toDate` to find Tweets in the range specified or any other operators that Tweeter API supports. Langauge may be an important operator.
    ```ini
    json_payload = {"query":"උන් lang:si OR උං lang:si OR සමහර lang:si","maxResults":"100","fromDate":"201811050000","toDate":"201812030000"}
    ```

### 4.4 Query with Tweeter

Words used to query is defined in the configurations done in the section **4.3**. Run the following script to run the `tweets_to_mongo.py` file and query with standard Twitter API. Make sure you have an internet connection and have run the Mongo DB as in section **4.1**.

```bash
cd twitter-api-reader/python/twitter && python tweets_to_mongo.py s
```

To use the premium API change the letter `s` with `p` at the end of the script. So it is as following.

```bash
cd twitter-api-reader/python/twitter && python tweets_to_mongo.py p
```

### 4.X. Backup Mongo DB

Backup your data with running following script.

```bash
mongodump --collection tweets --db db
```