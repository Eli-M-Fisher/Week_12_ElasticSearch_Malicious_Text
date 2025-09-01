# Week_12_ElasticSearch_Malicious_Text

# General Summary

This is a **monolithic** system of FastAPI and Elasticsearch, whose function is to:

- Load a text file of tweets
- Index them into Elastic with appropriate fields
- Process the data: I identify sentiment and then identify weapons from texts (using ElasticSearch).
- Delete irrelevant texts.
- Then we open an external API with 2 endpoints that allow queries on the data we processed

---

# Software process details

## 1. Loading the data

- There is a CSV file: `tweets_injected.csv` with the fields:
- `TweetID` (which is the unique identifier)

- `CreateDate` (the date the tweet was created)

- `Antisemitic` (0/1 antisemitic classification or not

- `text` (the literal content itself)
- Then using `data_loader.py` we load the file and upload the data to the Elastic index: `tweets_index`.
- The mapping (`INDEX_MAPPING`) ensures that each field is defined correctly (date, keyword, text, etc.).

---

## 2. Data processing stage

- Performed by `processor.py`:

1. **Sentiment Analysis**: For each text, `positive / neutral / negative` are calculated Using the `TextBlob` library.
2. **Weapon Detection**:

- There is a list of weapons (`weapon_list.txt`).
- We perform a `multi_match` query on Elastic to find which words from the list appear in each text.
- Then we update the documents with a new field: `weapons`.
3. **Deletion**: If a document is

- Not antisemitic (`Antisemitic=0`)
- And also does not contain a weapon
- And the sentiment is positive/neutral
Then the document is deleted from the index (because it is not relevant).

---

## 3. API Exposure

In `routes.py` there are two endpoints:

1. **`/antisemitic-weapons`**
According to the requirement, it returns all documents that are antisemitic **and have at least one weapon**.
And even if `process` has not been performed yet, it returns a message `"Data not processed yet."`.

2. **`/multi-weapons`**
This returns all documents that have **at least two weapons** in them.
Here too, if `process` was not executed, returns an appropriate message

---

## 4. Containers and running

- There are two Dockerfiles:

- One for the FastAPI application (the monolith API).
- And one I made for running Elasticsearch.
- There is also `docker-compose.yml` that saves both together in a local environment.
- There are scripts (`scripts/`) that allow you to run locally or deploy
---

# We actually did

- A single service for the monolith
- Correct use of Elasticsearch for indexing, searching and text processing, and not Python directly
- Of course there is a logical separation: loading, processing, API.
- Correct principles: neat file structure, use of config, code separation, basic documentation according to the requirement..