# Sinhalese Language based Offensive Detection

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