#coding:utf-8

import json
import requests

from pprint import pprint
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import smart_tweet_keys as stk


# Connection to Microsoft Azure.
keys = stk.Settings()
endpoint = keys.AZURE_ENDPOINT
api_version = '?api-version=2020-06-30'
headers = {'Content-Type': 'application/json', 'api-key': keys.AZURE_KEY}


# Authentication of the connection with Microsoft Azure.
def authenticate_client():
    ta_credential = AzureKeyCredential(keys.AZURE_KEY)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()


# Sentiment analysis.
dico_sentiment_tweet = []

def sentiment_analysis(client):
    with open('xbox_tweet.json') as json_data:
        data = json.load(json_data)
        
        for tweet in data:
            tweetlist = [tweet['Texte']]
            response = client.analyze_sentiment(documents = tweetlist)[0]
            temp = {}
            temp['Sentiment'] = response.sentiment
            temp['Score Positif'] = response.confidence_scores.positive
            temp['Score Neutre'] = response.confidence_scores.neutral
            temp['Score Negatif'] = response.confidence_scores.negative
            dico_sentiment_tweet.append(temp)

sentiment_analysis(client)


# Retrieving tweets in a JSON file.
with open('xbox_tweet_sentiment.json', 'w') as json_file:
    json.dump(dico_sentiment_tweet, json_file)



