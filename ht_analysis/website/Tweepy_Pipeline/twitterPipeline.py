#Make sure to add your twitter keys in a file name : config.ini. do not add them as strings add them like : api_key = gknbogfbjn

import tweepy
import configparser
import pandas as pd

#read all of the credentials

config = configparser.ConfigParser()
config.read('website/Tweepy_Pipeline/config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#Authenticate our account with the twitter API
authentication = tweepy.OAuthHandler(api_key, api_key_secret)

authentication.set_access_token(access_token, access_token_secret)

tweets_access_api = tweepy.API(authentication)

#we will use api to have access to twitter account
public_tweets = tweets_access_api.home_timeline()

#Searching tweets by hashtag
def acquire_tweets(hashtag: str, upper_limit:int = None) -> pd.DataFrame:
    """This method uses the given hashtag and upper limit to gather the data from twitter"""
    if hashtag is not None:
        if not hashtag.startswith("#"): # Ensure correct format of given hashtag
            hashtag = "#" + hashtag

        tweet_hashtag = hashtag
    else:
        tweet_hashtag = "#Python" # default tag to search, can be set to anything

    if upper_limit is not None:    
        #Maximum tweets will be returned per run/call  
        number_of_hashtag_tweets = upper_limit
    else:
        number_of_hashtag_tweets = 300 # set default upper limit   

    tweets = tweepy.Cursor(tweets_access_api.search_tweets, q = tweet_hashtag , count = 200, tweet_mode = 'extended', lang='en').items(number_of_hashtag_tweets)

    #Creating the dataframe with pandas
    columns = ['Tweets']
    data = []



    #Adding tweets to the datafram
    for tweet in tweets:
        #Adding the tweets to the created list.
        data.append([tweet.full_text])

    data_frame = pd.DataFrame(data, columns=columns)

    #Displaying the tweets
    print(data_frame)
    return data_frame

"""ht = input("Please enter a hashtag to search: ")
lim = int(input("Please enter the upper limit of number of tweets: "))
acquire_tweets(ht, lim)"""