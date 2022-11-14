#Make sure to add your twitter keys in a file name : config.ini. do not add them as strings add them like : api_key = gknbogfbjn

import tweepy
import configparser
import pandas as pd

#read all of the credentials

config = configparser.ConfigParser()
config.read('config.ini')

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
#TheWifeShow can be changed to any hashtag, it is used for testing purposes.
tweet_hashtag = '#TheWifeShowMax' 
#Maximum of 300 tweets will be returned per run/call  
number_of_hashtag_tweets = 300  

tweets = tweepy.Cursor(tweets_access_api.search_tweets, q = tweet_hashtag , count = 200, tweet_mode = 'extended').items(number_of_hashtag_tweets)

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
