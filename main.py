import sys
from configuration import resources
import database
import datatweet
import dataviz
from datatweet.tweet_manager import TweetCollection
from datatweet.tweet_manager import TweetSentimentPrediction
from datatweet.tweet import SentTweet
from flask_migrate import Migrate
from sys import exit
from os import environ
from dataviz.config import config_dict
from dataviz.app import create_app
#from database.database_access import DatabaseManager
from datatweet.tweet_manager import TweetLoader
import matplotlib.pyplot as plt

get_config_mode = environ.get('APPSEED_CONFIG_MODE', resources.APPSEED_CONFIG_MODE)

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid APPSEED_CONFIG_MODE environment variable entry.')

app = create_app(config_mode) 

if __name__ == "__main__":
    #print(resources.CONSUMER_SECRRET)
    product_name = "#XboxSeriesS"

    TweetLoader(product_name).load_data()

    app.run(host='localhost', port = 8080,use_reloader=False)
    