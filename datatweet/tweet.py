class SentTweet:


    def __init__(self
                , id
                , text
                , user_name
                , user_screenname
                , user_location
                , language
                , entities
                , created_at):
        self.id = id
        self.text = text
        self.user_name = user_name
        self.user_screenname = user_screenname
        self.user_location = user_location
        self.language = language
        self.entities = entities
        self.created_at = created_at
        # sentiment is an json object
        self.sentiment = ''

    def update_sentiment(self, sentiment):
        self.sentiment = sentiment

    def to_json(self):

        return {"tweet_id": str(self.id)
                , "text": self.text
                , "user_name": self.user_name
                , "user_screenname" : self.user_screenname
                , "user_location": self.user_location
                , "language" : self.language
                , "created_at" : self.created_at
                , "entities" : self.entities
                # sentiment is a json objecy
                , "sentiment" : self.sentiment
                }

    def to_json_azure(self):
        return {"id": self.id
                , "text": self.text}

"""
class Sentiment:

    def __init__(self, sentiment, confidenceScores)
"""