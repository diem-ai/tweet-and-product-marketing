
from database.database_access import DatabaseManager
from configuration import resources

from database.db_access import DatabaseManager as db

if __name__ == "__main__":
    
    """
    mongo_instance = DatabaseManager(resources.MONGODB_USER
                                    , resources.MONGODB_PASSWORD
                                    , resources.MONGODB_SERVER)

    for data in mongo_instance.get
    """
    dict_tag = {}
    for tweet in db.getInstance().get_tweets({}):
        list_tag = tweet['entities']['hashtags']
        for tag in list_tag:
            text = tag['text']
            if (not text in dict_tag):
                dict_tag[text] = 1
            else:
                dict_tag[text] += 1
    
    dict_tag = sorted(dict_tag.items(), key=lambda x: x[1], reverse=True)
    print(dict_tag[:5])

    for key, v in dict_tag[:20]:
        print(key)



        
        