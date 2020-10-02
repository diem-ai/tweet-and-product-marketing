from database.db_access import DatabaseManager as db

if __name__ == "__main__":
    

    tweet_id = "1304045426715299846"

    print(db.getInstance().get_tweet_by_id(tweet_id) == None)

    print(db.getInstance().get_tweet_by_id('id') == None)