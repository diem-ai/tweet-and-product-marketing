
# Product's Twitter Sentiment
Realization of the Smart tweet brief  </br>
![](/mainpage.PNG)

### Installation
- pip install requirements.txt

### Project structure

**/configuration**
- resources.py: contains the key authentication of Azure API and Tweet API

**/database**
- db_access.py : python code files for database manipulation.
	Provide connection to the database with some methods:
	
	- add_one_tweet
	- add_many_tweets
	- get_tweet_by_id
	- get_tweets
	- get_tweets_paginated
	- update_tweet_by_id
	- update_tweets
	- delete_tweets
	
	**method call:**
    ```python
	from database.db_access import DatabaseManager as db

	db.getInstance().add_one_tweet({
        'name' : 'tweet1',
        'sentiment' : 2,
        'text' : 'random comment'
    })
    ```

**/dataviz**
- SQL code
- Python code for dashboard visulization

**/datatweet**: contains python classes that collect tweets with Twitter API and predict their sentiments with Azure API
- tweet_manager.py
	- TweetCollection class: retreive most recent tweets
	- TweetSentimentPrediction class: send tweets to Azure in order to obtain their sentiment score and the confidence scores
	- TweetLoader class: prepare the the availability of database by calling TweetCollection and TweetSentimentPrediction and create the time series chart 
- tweet.py: an python object who transforms python object into json


### Launch
- python main.py


### Credit

This project can not be completed without the help of Andrey and Mathieu
