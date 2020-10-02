from pymongo import MongoClient
from configuration.resources import MONGODB_PASSWORD, MONGODB_SERVER, MONGODB_USER
import time

"""
   Copy data from one collection to another collection and remove duplicates entries
"""


CONNECTION_STRING = str.format("mongodb+srv://{}:{}@{}/business?retryWrites=true&w=majority", MONGODB_USER, MONGODB_PASSWORD, MONGODB_SERVER )
FROM = 'tweets'
TO = 'tweets_prod'
__client = MongoClient(CONNECTION_STRING)
ids = __client.get_database('smart_tweets').get_collection(FROM).find({}).distinct('tweet_id')

print(len(ids))

i = 0
for id in ids:
    tweet = __client.get_database('smart_tweets').get_collection(FROM).find_one({'tweet_id': id})
    __client.get_database('smart_tweets').get_collection(TO).insert_one(tweet)
    i += 1
    print(i)
    time.sleep(1)

print(i)