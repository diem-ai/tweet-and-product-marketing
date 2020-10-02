from pymongo import MongoClient
from configuration.resources import MONGODB_PASSWORD, MONGODB_SERVER, MONGODB_USER

class DatabaseManager:
    """Provide methods and connection to the MongoDb database
    """

    __CONNECTION_STRING = str.format("mongodb+srv://{}:{}@{}/business?retryWrites=true&w=majority", MONGODB_USER, MONGODB_PASSWORD, MONGODB_SERVER )
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DatabaseManager.__instance == None:
            DatabaseManager()
        return DatabaseManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DatabaseManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseManager.__instance = self
            print(DatabaseManager.__CONNECTION_STRING)
            self.__client = MongoClient(DatabaseManager.__CONNECTION_STRING)

    def __get_collection(self, db_name, collection_name):
        """Generic method to connect to a give collection in a given database
        If the database or the collection don't exist, it will be created

        Args:
            db_name (str): name of the database
            collection_name (str): name of the collection

        Returns:
            collection: the collection
        """
        return self.__client.get_database(db_name).get_collection(collection_name)

    def add_one_tweet(self, tweet):
        """Insert a tweet in the tweets collection

        Args:
            tweet (json): the enhanced tweet json 

        Returns:
            bool : True if insertion succeed else False
        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').insert_one(tweet)
        return result.acknowledged
        
    def add_many_tweets(self, tweets):
        """add list of tweets

        Args:
            tweets (json[]): list of json

        Returns:
            bool: True if insertions fully succeed else false
        """
        result = True
        for tweet in tweets:
            tweet_id = tweet["tweet_id"]
            # add tweet if tweet is not existed in the database yet
            if(self.get_tweet_by_id(tweet_id) == None):
                result &= self.add_one_tweet(tweet)
        return result

    def get_tweet_by_id(self, id):
        """Get a tweet by id

        Args:
            id (str): id of the tweet

        Returns:
            json: the enhanced tweet
        """
        return self.__get_collection('smart_tweets', 'tweets_prod').find_one({'tweet_id': id})

    def get_tweets(self, filters):
        """get tweets by filter

        Args:
            filters (dictionnary): filters to apply for the select.
                                    ex : {'name':'XXXXX', 'sentiment':4}

        Returns:
            json[]: list of enhanced tweets
        """
        return self.__get_collection('smart_tweets', 'tweets_prod').find(filters)

    def get_tweets_paginated(self, page, nb_elements):
        result=  self.__get_collection('smart_tweets', 'tweets_prod').aggregate([
                                                { "$sort" : {
                                                    "created_at" : -1
                                                    }
                                                },
                                                { "$skip" : page*nb_elements },
                                                { "$limit": nb_elements }
                                    ])

        return result

    def update_tweet_by_id(self, id, data):
        """Update a tweet by its id

        Args:
            id (str): id of the tweet
            data (dictionnary): list of key/value to update

        Returns:
            bool: True if one tweet updated else false
        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').update_one({'tweet_id': id}, {"$set": data}, upsert=True)
        return result.modified_count == 1

    def update_tweets(self, filters, data):
        """update list of tweets matching with filters

        Args:
            filters (dictionnary): filters to apply for the select.
            data  (dictionnary): list of key/value to update

        Returns:
            int: number of tweets updated
        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').update_many(filters, data)
        return result.modified_count

    def delete_tweets(self, filters):
        """delete list of tweets matching with filters

        Args:
            filters (dictionnary): filters to apply for the select.

        Returns:
            int: number of tweets deleted
        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').delete_many(filters)
        return result.deleted_count

    def get_tweet_collection(self):
        """temporary method to get collection in order to manipulate collection without methods
            For additionnal methods, db_access should be updated, do not manipulate collection outside this manager

        Returns:
            [type]: [description]
        """
        return self.__get_collection('smart_tweets', 'tweets_prod')


    def get_top_positive_tweets(self, filters):
        """get the top positives tweets of the dataset

        Returns:
            json: top positives tweets
        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').find(filters).sort([("sentiment.confidence_scores.positive", -1), ("created_at", -1)]).limit(5)
        return result

    def get_top_negative_tweets(self, filters):
        """get the top negative tweets of the dataset

        Returns:
            json: top negative tweets
        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').find(filters).sort([("sentiment.confidence_scores.negative", -1), ("created_at", -1)]).limit(5)
        return result
        
    def get_number_of_tweets(self):
        """get the total nomber of tweets.

        Returns:
            int: value
        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').count()
        return result

    def get_number_of_tweets_by_range(self, range):
        """Get the number of tweets for the selected range

        Args:
            str: positive, negative or neutral

        Returns:
            int: value

        """
        result = self.__get_collection('smart_tweets', 'tweets_prod').find({"sentiment.sentiment_score" : range}).count()
        return result

    def get_top_hashtags(self, nb_hashtags):
        """Get the most quoted hashtags.

        Returns:
            list
        """

        hashtags_list= self.__get_collection('smart_tweets', 'tweets_prod').aggregate([
            { "$project": {
                "_id": 0,
                "entities.hashtags" : 1
            }},
            { "$unwind": "$entities.hashtags" },
            { "$group" : {
                    "_id": "$entities.hashtags.text",
                    "count": { "$sum" : 1 }
                    }
            },
            { "$sort" : {
                "count" : -1
                }
            },
            { "$limit": nb_hashtags }
        ])

        results = []
        for hashtag in hashtags_list:
            results.append(hashtag.get('_id'))

        return results

