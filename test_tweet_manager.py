###################################################
#@author: Diem Bui
#@Date: 08/09/2020
###################################################

import sys
#sys.path.insert(0, '')
from configuration import resources
import database
import datatweet
import dataviz
from datatweet.tweet_manager import TweetCollection
from datatweet.tweet_manager import TweetSentimentPrediction
from datatweet.tweet import SentTweet
from database.db_access import DatabaseManager as db


#from datatweet import tweet_manager
#from datatweet.tweet_manager import TweetCollection

if __name__ == "__main__":
    #print(resources.CONSUMER_SECRRET)
    product_name = "#XboxSeriesS"


    # test first 5 most recent tweets
    list_tweet = TweetCollection(resources.CONSUMER_KEY
    , resources.CONSUMER_SECRRET
    , resources.ACCESS_TOKEN
    , resources.ACCESS_TOKEN_SECRET).get_tweet_by_product(product_name)


#    print("before getting the sentiment")
    for tweet in list_tweet:
        print(tweet.to_json())
        print("\n")


    list_sent_tweet = TweetSentimentPrediction(list_tweet
            , resources.SUBSCRIPTION_KEY
            , resources.SENTIMENT_ENDPOINT_URL).predict()
    



#    print("after getting the sentiment")
    list_json = []
    for tweet in list_sent_tweet:
        print(tweet.to_json())
        list_json.append(tweet.to_json())
        print("\n")


    db.getInstance().add_many_tweets(list_json)

    