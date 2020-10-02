#coding:utf-8

import json
import tweepy

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from pymongo import MongoClient

import smart_tweet_keys as stk


"""
This script allows you to:
- Retrieve tweets using the Twitter API.
- Analyze the text of tweets with the sentiment analysis of Microsoft Azure.
- Insert this data in MongoDB database.
"""


# Connection to the Twitter API.
keys = stk.Settings()
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# Connection to Microsoft Azure.
endpoint = keys.AZURE_ENDPOINT
api_version = '?api-version=2020-06-30'
headers = {'Content-Type': 'application/json', 'api-key': keys.AZURE_KEY}


# Connection to our MongoDB database.
client = MongoClient("mongodb+srv://simplon:pMTPbkx4SEILUfam@cluster0.nqjp5.mongodb.net/business?retryWrites=true&w=majority")
db = client.smart_tweet_maxime
collection_xbox_tweet = db["xbox_tweet"]


# Authentication for the link with Microsoft Azure.
def authenticate_client():
    ta_credential = AzureKeyCredential(keys.AZURE_KEY)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client        

client = authenticate_client()


# Retrieving tweets by hashtag.
dico_tweet = []
texte = []

for tweet in tweepy.Cursor(api.search,  q = "#XboxSeriesS", lang = "fr").items(10):    
    if tweet.retweeted == False:
        temp = {}
        tempSentiment = {}
        tempConfidence = {}
        temp['ID'] = tweet.id
        temp['Texte'] = tweet.text
        temp['Date'] = tweet.created_at.strftime("%Y-%d-%m")
        temp['Auteur'] = tweet.user.screen_name
        texte.append(tweet.text)
        response = client.analyze_sentiment(texte)
        tempSentiment['Sentiment Score'] = response[0].sentiment
        temp['Sentiment'] = tempSentiment
        tempConfidence['Score Positif'] = response[0].confidence_scores.positive
        tempConfidence['Score Neutre'] = response[0].confidence_scores.neutral
        tempConfidence['Score Negatif'] = response[0].confidence_scores.negative
        temp['Confidence Scores'] = tempConfidence
        dico_tweet.append(temp)


# Display of dictionary content and tweets identifiers.
# pprint("contenu : " + str(dico_tweet))
# for i in collection_xbox_tweet.find():
#     for j in dico_tweet:
#         # print("collection_xbox_tweet : " + str(i["ID"]) + "    dico_tweet : " + str(j["ID"]))
#         if (i["ID"] == j["ID"]):
#             print(i["ID"])


"""
Below are two ways to retrieve tweets.
Either directly in the database or in a JSON file.
"""


# Insertion in database.
collection_xbox_tweet.insert_many(dico_tweet)
client.close()


# Storage of tweets in a JSON file.
# with open('xbox_tweet.json', 'w') as json_file:
    # json.dump(dico_tweet, json_file)
