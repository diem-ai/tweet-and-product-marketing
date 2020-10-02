from database.db_access import DatabaseManager as db
import pandas as pd
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":


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

    plt.savefig(os.getcwd() + '/dataviz/app/base/static/assets/images/timeseries.png')



    