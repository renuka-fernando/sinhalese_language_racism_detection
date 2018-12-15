# Sinhalese Language based Offensive Detection

## Requirements
- pymongo
- pandas
- requests_oauthlib
- emoji `pip install emoji`


## Restore Mongo DB with twitter data

### Backup Mongo DB

```bash
mongodump --collection tweets --db db
```

### Restore Mongo DB

```bash
mongod --dbpath data-set/mongo-db
mongorestore dump
```