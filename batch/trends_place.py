#coding:utf-8

import tweepy
import json

import smart_tweet_keys as stk

# Connection to the Twitter API.
keys = stk.Settings()
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


trends_paris = api.trends_place(615702)         # WOEID from Paris.


# Indicates the volume of tweets for the chosen hashtag.
for dictionnary in trends_paris:
    for trends in dictionnary['trends']:
        if trends['name'] == "#xboxseriess":    # We choose the hashtag here.
            print(trends['tweet_volume'])


# Indicates trending topics for the city of Paris.
for dictionnary in trends_paris:
    for trends in dictionnary['trends']:
            print(trends['name'])