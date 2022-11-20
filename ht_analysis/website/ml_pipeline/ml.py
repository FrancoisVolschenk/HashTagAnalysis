# from twitterPipeline import *

import pytz
from wordcloud import WordCloud
from itertools import chain
import re
from keras_preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from tensorflow import keras
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import tensorflow as tf
import pandas as pd
import numpy as np

import nltk
nltk.download('stopwords')

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' # tensorflow outputs a "helpful" message to tell you that it has optimizations enabled. This code turns that off
"""2022-09-19 20:52:22.272276: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX AVX2
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags."""

# Get English stopwords
stop_words = stopwords.words('english')
stemmer = SnowballStemmer('english')

# Regex for links
text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

MAX_SEQUENCE_LENGTH = 30


def preprocess(text, stem=False):
    text = re.sub(text_cleaning_re, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)


def predict_sentiment(tweets_o: pd.DataFrame):
    

    #keep original dataframe for the original tweet
    tweets = tweets_o.copy()
    # Clean data
    tweets.Tweets = tweets.Tweets.apply(lambda x: preprocess(x))

    # Split sentences into words
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(tweets.Tweets)

    vocab_size = len(tokenizer.word_index) + 1
    # print("Vocabulary Size :", vocab_size)

    # Create sequences (numpy array) from the tokenized text
    sequences = pad_sequences(tokenizer.texts_to_sequences(
        tweets.Tweets), maxlen=MAX_SEQUENCE_LENGTH)

    # load model
    model = keras.models.load_model(
        'website/ml_pipeline/ht_analysis_model_v1.0.h5')

    # predict sentiment
    predictions = model.predict(sequences, verbose=1, batch_size=10000)

    pred_list = predictions.tolist()
    flat_list = list(chain.from_iterable(pred_list))
    positive = []
    negative = []
    unsure = []
    
    for x in range(len(flat_list)):
        if (flat_list[x] < 0.45):
            negative.append(
                {"tweet": tweets_o.Tweets[x], "time": tweets.Time[x],"location":tweets_o.Location[x], "sentiment": "Negative", "value": flat_list[x]})
        elif (flat_list[x] > 0.55):
            positive.append(
                {"tweet": tweets_o.Tweets[x], "time": tweets.Time[x],"location":tweets_o.Location[x], "sentiment": "Positive", "value": flat_list[x]})
        else:
            unsure.append(
                {"tweet": tweets_o.Tweets[x], "time": tweets.Time[x],"location":tweets_o.Location[x], "sentiment": "Unsure", "value": flat_list[x]})

    t_p = [p.get('tweet') for p in positive] if len(
        positive) > 0 else ["No positive tweets"]
    t_n = [n.get('tweet') for n in negative] if len(
        negative) > 0 else ["No negative tweets"]
    t_u = [u.get('tweet') for u in unsure] if len(
        unsure) > 0 else ["No unsure tweets"]

    # Generate word clouds for each type of tweet

    wc_p = WordCloud(max_words=2000, width=1600,
                     height=800).generate(' '.join(t_p))
    wc_n = WordCloud(max_words=2000, width=1600, height=800).generate(
        ' '.join(t_n))
    wc_u = WordCloud(max_words=2000, width=1600, height=800).generate(
        ' '.join(t_u))

    return {"positive": positive, "negative": negative, "unsure": unsure, "wc_p": wc_p.to_image(), "wc_n": wc_n.to_image(), "wc_u": wc_u.to_image()}


"""ht = input("Please enter a hashtag to search: ")
lim = int(input("Please enter the upper limit of number of tweets: "))
tweets = acquire_tweets(ht, lim)

print(predict_sentiment(tweets))"""
