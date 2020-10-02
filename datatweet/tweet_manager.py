###################################################
#@author: Diem Bui
#@Date: 08/09/2020
###################################################


import tweepy
import json
import requests
import pandas as pd
from datatweet.tweet import SentTweet
from database.db_access import DatabaseManager as db
from configuration.resources import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRRET, SENTIMENT_ENDPOINT_URL, SUBSCRIPTION_KEY
import matplotlib.pyplot as plt
import os



class TweetCollection:

    def __init__(self
                , consumer_key
                , consumer_secret
                , access_token
                , access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.tweet_api = self._get_tweet_api()

    def _get_tweet_api(self):
        
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        return api
    
    

    def get_tweet_by_product(self, product_name):

        list_tweet = []
        keyword = "#" + product_name
        for tweet in self.tweet_api.search(q=keyword 
                                    #, lang="en"
                                    , include_entities=True
                                    , result_type='recent'
                                    , count = 200
                                   ):

            list_tweet.append(SentTweet(str(tweet.id)
                                    , tweet.text
                                    , tweet.user.name
                                    , tweet.user.screen_name
                                    , tweet.user.location
                                    ,  tweet.metadata['iso_language_code']
                                    , tweet.entities
                                    , tweet.created_at))
        return list_tweet


class TweetSentimentPrediction:

    def __init__(self, list_tweet, subscription_key, endpoint_url):
        self.list_tweet = list_tweet
        self.subcription_key = subscription_key
        self.endpoint_url = endpoint_url
    
    def get_header(self):
        return {"Ocp-Apim-Subscription-Key": self.subcription_key}

    def get_sentiment(self, response):
        """get sentiment score of tweet

        Args:
            documents (json): a json with structure: {"documents": []
                                                        "errors", []
                                                        ,"modelVersion" : []}
        Return a json object with structure:
            {sentiment": "positive"
            , "confidenceScores": 
            {
                "positive": 1.0,
                "neutral": 0.0,
                "negative": 0.0
            }}
        """
#        print(response)

        sentiment = {"sentiment_score" : response["sentiment"]
                    , "confidence_scores" : response["confidenceScores"]}
        return sentiment



    def create_documents(self):
        """
        ["documents": []
        , "documents" : []]
        """
        """
        list_document = []
        

        for tweet in self.list_tweet:
            list_document.append(tweet.to_json_azure())
        
        return {"documents": list_document}

        """

        list_documents = []
        documents = []
        start = 0
        end = 0
        c_tweet = len(self.list_tweet)

        if (c_tweet <= end):
            for tweet in self.list_tweet:
                documents.append(tweet.to_json_azure())
                list_documents.append({"documents" : documents})
        else: # number of tweet is greater 10
            while (end < c_tweet):
                
                start = end
                end += 10
                documents = []

                if (end > c_tweet):
                    end = c_tweet

                for tweet in self.list_tweet[start:end]:
                    documents.append(tweet.to_json_azure())

                list_documents.append({"documents" : documents})

        return list_documents

        

    def predict(self):
        """
        return a List <SentTweet> with sentiment updated
        """
        # send 10 documents maixum to the Azure server
        list_documents = self.create_documents()
        list_repsonse = []
        for documents in list_documents:
            response = requests.post(self.endpoint_url
                                , headers=self.get_header()
                                , json=documents)
            jsresponse =  response.json()
            for value in jsresponse['documents']:
                list_repsonse.append(value)

        for tweet, resp in zip(self.list_tweet, list_repsonse):
            tweet.update_sentiment(self.get_sentiment(resp))
        
        return self.list_tweet

    

class TweetLoader:

    def __init__(self, product='#XboxSeriesS'):
        self.product = product



    def export_timeseries_chart(self):
        pipeline = [

            {
            "$project":
            
            {
                "date" : "$created_at"
                , "sentiment": "$sentiment.sentiment_score",
                "score" : {

                                    "$switch": {
                                        "branches": [
                                            { "case": {"$eq": ["$sentiment.sentiment_score", "positive"] } , "then": "$sentiment.confidence_scores.positive" },
                                            { "case": {"$eq": ["$sentiment.sentiment_score", "negative"] }, "then":  "$sentiment.confidence_scores.negative" },
                                            { "case": {"$eq": ["$sentiment.sentiment_score", "neutral"] }, "then":  "$sentiment.confidence_scores.neutral" }
                                
                                        ],
                                                                                
                                        "default": {"$max": ["$sentiment.confidence_scores.positive" , "$sentiment.confidence_scores.negative" , "$sentiment.confidence_scores.neutral"]} 

                                    }
                }

            


                }#project
            }]
                    
        ts_sentiment = db.getInstance().get_tweet_collection().aggregate(pipeline)

        # use set() to remove the duplication
        set_tweet_sent = set()
                                
        for row in ts_sentiment:
            set_tweet_sent.add((row['date'], row['sentiment'], row['score']))

        list_date = []
        list_sent_pos = []
        list_sent_neg = []
        list_sent_neu = []

        for date, sent, score in set_tweet_sent:
            if sent == 'mixed':
                continue
            list_date.append(str(date))
            if (sent == 'positive'):
                list_sent_pos.append(score)
                list_sent_neu.append(0)
                list_sent_neg.append(0)
            elif (sent == 'negative'):
                list_sent_pos.append(0)
                list_sent_neu.append(0)
                list_sent_neg.append(score)
            else:
                list_sent_pos.append(0)
                list_sent_neu.append(score)
                list_sent_neg.append(0)


        df_ts_sent = pd.DataFrame(data = {'positive' : list_sent_pos
                                        , 'negative' : list_sent_neg
                                        , 'neutral' : list_sent_neu }
                                , index = list_date )
        

        df_ts_sent.plot(figsize=(50, 20), linestyle=' ', marker='X', color=['green', 'red', 'blue'])
        plt.legend('')

        plt.savefig(os.getcwd() + '/dataviz/app/base/static/assets/images/timeseries_sent.png')


    def load_data(self):
        # test first 5 most recent tweets
        list_tweet = TweetCollection(CONSUMER_KEY, CONSUMER_SECRRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET).get_tweet_by_product(self.product)

        list_sent_tweet = TweetSentimentPrediction(list_tweet, SUBSCRIPTION_KEY,SENTIMENT_ENDPOINT_URL).predict()
                
        list_json = []
        for tweet in list_sent_tweet:
            #print(tweet.to_json())
            list_json.append(tweet.to_json())

        db.getInstance().add_many_tweets(list_json)

        self.export_timeseries_chart()








    



"""
if __name__ == "__main__":
    print(resources.CONSUMER_SECRRET)
    #print(resources.CONSUMER_KEY)
"""