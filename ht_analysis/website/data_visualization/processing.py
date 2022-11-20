import pandas as pd
from website.ml_pipeline.ml import *

def timeData(data):
    df = pd.DataFrame(data)
    df.sort_values(by='time')
    # Get time difference between top and bottom value

    t1 = df.iloc[-1][1]  # last time in time column
    t2 = df.iloc[0][1]  # first value in time column
    delta = t2 - t1  # time difference
    ms = delta.total_seconds() * 1000  # difference in milliseconds
    unit = "millisecond"  # default is millisecond
    if (ms < 1000):
        unit = "millisecond"
        df2 = (df.groupby([pd.Grouper(freq='L', key='time', closed="left"), 'sentiment'])[
               'value'].count().unstack(fill_value=0)).reset_index()

    else:  # must be a bigger scale
        if (ms < 60000):
            unit = "second"
            df2 = (df.groupby([pd.Grouper(freq='S', key='time', closed="left"), 'sentiment'])[
                   'value'].count().unstack(fill_value=0)).reset_index()

        else:  # must be a bigger scale
            if (ms < 3600000):
                unit = "minute"
                df2 = (df.groupby([pd.Grouper(freq='T', key='time', closed="left"), 'sentiment'])[
                       'value'].count().unstack(fill_value=0)).reset_index()

            else:
                unit = "hour"  # Max group by hour
                df2 = (df.groupby([pd.Grouper(freq='H', key='time', closed="left"), 'sentiment'])[
                       'value'].count().unstack(fill_value=0)).reset_index()

    # Return
    return {"unit": unit, "df": df2}


def parsechartpoints(df):
    #results : context
    # df : contains the groupings for the time splits

    pos_ds = []  # positive data points
    neg_ds = []
    neu_ds = []
    # convert datetime to string for json
    df['time'] = df['time'].astype(str)
    for i in df.index:

        if 'Positive' in df.columns:
            pos_ds.append({"x": df['time'][i], "y": int(df['Positive'][i])})
        if 'Negative' in df.columns:
            neg_ds.append({"x": df['time'][i], "y": int(df['Negative'][i])})
        if 'Unsure' in df.columns:
            neu_ds.append({"x": df['time'][i], "y": int(df['Unsure'][i])})

    return {"p": pos_ds, "n": neg_ds, "u": neu_ds}


def wordFrequency(tweets, hashtag):

    processed = cleantweets(tweets, hashtag)
    words = []
    for tweet in processed:
        for j in tweet.split():
            words.append(j)
    dict_ = wordListToFreqDict(words)  # split the tweets into words

    sorted = sortFreqDict(dict_)

    return sorted


def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist, wordfreq)))


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key)
           for key in freqdict]  # tupple of word with frequency
    aux.sort()  # sort by count
    aux.reverse()
    return aux


def cleantweets(tweets, hashtag):
    cleaned = []
    for i in tweets:  # for each tweet
        i = preprocess(i)  # preprocess the tweet here
        # remove the hastag cause it will apppear the most
        i = i.replace(str(hashtag).lower(), '')
        cleaned.append(i)
    return cleaned  # cleaned tweets


def wordFrequency_Sentiment(words, alltweets):
    pos = []
    neu = []
    neg = []

    for word in words:
        num_in = 0
        sentiment = 0
        for row in alltweets:
            ans = preprocess(row['tweet'])

            if word in ans:
                num_in = num_in + 1
                sentiment = sentiment + row['value']

        avg = (sentiment/num_in) if num_in > 0 else 0
        if (avg < 0.45):
            neg.append({"word": word, "count": num_in, })
        elif (avg > 0.55):
            pos.append({"word": word, "count": num_in, })
        else:
            neu.append({"word": word, "count": num_in, })

    all = pos + neu + neg  # note order
    return {"words": [d["word"] for d in all], "pos": [d["count"] for d in pos], "neu": [d["count"] for d in neu], "neg": [d["count"] for d in neg]}


def locationData(alltweets):

    df = pd.DataFrame(alltweets)
    df2 = df.groupby('location', sort=False).agg(
        {'value': ['mean', 'count']}).reset_index()
    sortedDF = df2.sort_values([('value', 'count')], ascending=False)
    list_ = sortedDF.values.tolist()
    places = [i[0] for i in list_]
    sentiment = [i[1] for i in list_]
    counts = [i[2] for i in list_]
    pos = []
    neu = []
    neg = []
    for s in sentiment:
        if (s < 0.45):
            # The sentiment and count are at correnspinding indices
            neg.append(counts[sentiment.index(s)])
        elif (s > 0.55):
            pos.append(counts[sentiment.index(s)])
        else:
            neu.append(counts[sentiment.index(s)])

    return {"places": [d for d in places], "pos": pos, "neu": neu, "neg": neg}
