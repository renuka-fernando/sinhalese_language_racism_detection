# Sinhalese Language based Hate Speech Detection

## Background

Advances in communication technology has brought people to one global position. Among them social media platforms play a major role with granting users freedom to speech by allowing them to freely express their thoughts, beliefs, and opinions. Children, adolescents, adults are spending significant amount of time on various social networking sites to connect with others, to share information, and to pursue common interests. Although this make great opportunities such as learn from others, there are some challenges. Racism, trolling, being exposed to large amounts of offensive online contents are such examples. The rapid growth of race hate speech on social media seems to have big impact on society and goodwill of a country.

Social media is the collective of online communications channels dedicated to community-based input, interaction, content-sharing and collaboration and is a very popular way for people to express their opinions publicly. Forums, microblogging, social networking, social bookmarking, social curation, and wikis are some of different types of social media and “Facebook”, “Twitter”, “Google+”, “Wikipedia”, “LinkedIn”, “Reddit”, “Pinterest” are some examples of popular social media. While social media helps people with connecting each other, sharing knowledge regardless of location, education background, updating information around the world, it also enables the risk of people to being targeted or harassed via offensive language which may severely impact the community in general.

Sri Lanka had a same kind of problem related to social medias in March, 2018 related to an incident happened in Digana, Kandy that occurs due to failure of social media to detect of race speeches and offensive language on comments and posts since they were in Sinhala language. Current tools failed to detect such things and the temporary solution was blocking on Facebook and other social media

## Requirements

- pymongo
- pandas
- requests_oauthlib
- emoji `pip install emoji`


## Restore Mongo DB with Twitter Data

### Backup Mongo DB

```bash
mongodump --collection tweets --db db
```

### Restore Mongo DB

```bash
mongod --dbpath data-set/mongo-db
mongorestore dump
```