#coding:utf-8

import json

# pprint library is used to make the output look more pretty.
from pprint import pprint
from pymongo import MongoClient


# Connect to MongoDB.
client = MongoClient("mongodb+srv://simplon:pMTPbkx4SEILUfam@cluster0.nqjp5.mongodb.net/business?retryWrites=true&w=majority")
db = client.smart_tweet_maxime
collection_xbox_tweet = db["xbox_tweet"]


# Import data.
with open("xbox_tweet.json") as f:
    file_data = json.load(f)

collection_xbox_tweet.insert_many(file_data)
client.close()


# Delete database & collection.
# db.xbox_tweet.drop()