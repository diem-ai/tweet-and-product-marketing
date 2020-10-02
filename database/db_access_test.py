from database.db_access import DatabaseManager as db

#test dataset
test = {
        'name' : 'tweet1',
        'sentiment' : 2,
        'text' : 'random comment'
    }

#test singleton
try:
    singleton_test = db()
    singleton_test = db()
    assert False, 'you should not be able to instanciate Databasemanager twice'
except:
    assert True, 'not able to instanciate Databasemanager as expected'

#insert tweet
result = db.getInstance().add_one_tweet(test)
assert result, 'not able to insert the tweet'

#get all tweet
result = db.getInstance().get_tweets({})
#get id of the first tweet retrieved
tweet_test_id = result[0].get('_id')
print(tweet_test_id)

#get tweet by id
result = db.getInstance().get_tweet_by_id(tweet_test_id)
print(result)

#update tweet by id
result = db.getInstance().update_tweet_by_id(tweet_test_id, {'sentiment',3})
print('record updated: '+ str(result))

#get tweet to check modification
result = db.getInstance().get_tweet_by_id(tweet_test_id)
print(result)

#delete tweet by id
result = db.getInstance().delete_tweets({'_id' :tweet_test_id})
print('nb records deleted '+ str(result))



    