import itertools
import json
from django.shortcuts import render, redirect
from .Tweepy_Pipeline.twitterPipeline import *
from .ml_pipeline.ml import *


def index(request):
    """This method will return the default (home) page of our project where users are asked to enter a hashtag to be analysed"""

    # if a get request was made, return the form as is
    if request.method == "GET":
        return render(request, "website/index.html")

    # if a post reques was made, the user searched for a hashtag
    elif request.method == "POST":
        # extract the hashtag from the request
        hashtag = request.POST.get("ht", None)
        upper_limit = request.POST.get("limit", None)
        if hashtag is None:
            Context = {"msg": "Please be sure to enter a valid hashtag"}
            return render(request, "website/index.html", Context)
        else:
            """We have the hashtag and can use it to perform the analysis"""
            data = acquire_tweets(hashtag, int(upper_limit))
            return data_visualizationPage(request, data, hashtag)


def data_visualizationPage(request, data, hashtag):
    if data is None:
        return redirect(index)
    else:
        # We process the data and return it in a format that can be visualized on the front end
        # make a call to the ML model and have the data processed

        results = predict_sentiment(data)

        results['hashtag'] = hashtag
        # General Data
        tweets_pulled = len(results['positive']) + \
            len(results['unsure']) + len(results['negative'])
        results['tweets_pulled'] = tweets_pulled
        results['percent_pos'] = (len(results['positive'])/tweets_pulled)*100
        results['percent_neu'] = (len(results['unsure'])/tweets_pulled)*100
        results['percent_neg'] = (len(results['negative'])/tweets_pulled)*100
        results['max'] = max({'p': results['percent_pos'], 'u': results['percent_neu'], 'n':  results['percent_neg']}, key=(
            {'p': results['percent_pos'], 'u': results['percent_neu'], 'n':  results['percent_neg']}).get)

        # save the word clouds so that they can be displayed on the web page

        results['wc_p'].save("website/static/website/img/wc_p.jpg")
        results['wc_n'].save("website/static/website/img/wc_n.jpg")
        results['wc_u'].save("website/static/website/img/wc_u.jpg")

        # Temp
        results['msg'] = "The data has been displayed on the console for the time being"

        #For  Tweets' table
        results['all_tweets'] = results['positive'] + results['unsure'] + results['negative']

       # For Distribution pie chart
        results['n_sentiment'] = json.dumps(
            [len(results['positive']), len(results['unsure']), len(results['negative'])])

       # Sentiment over Time
        
        td_values = timeData(results['all_tweets'])
        results['unit'] = td_values['unit']
        time_datasets = parsechartpoints(td_values['df'])
        results['pos_ds'] = json.dumps(time_datasets['p'])
        results['neg_ds'] = json.dumps(time_datasets['n'])
        results['neu_ds'] = json.dumps(time_datasets['u'])

        # Word Frequency

        frq = wordFrequency([d['tweet'] for d in results['all_tweets']], hashtag)
        frq_values = [x[0] for x in frq]
        frq_words = [x[1] for x in frq]
        results['freq_words'] = json.dumps(
            frq_words[0:10])  # 10 most frequent words
        results['freq_values'] = json.dumps(
            frq_values[0:10])  # 10 most frequent words
        # Word Frequency with sentiment
        wf_sentiment = wordFrequency_Sentiment(  frq_words[0:10],results['all_tweets'])
        results['wf_words'] = json.dumps(wf_sentiment['words'])
        results['wf_counts'] = json.dumps(wf_sentiment['counts'])
        results['wf_sentiments'] = json.dumps(wf_sentiment['sentiments'])

        #UserLocation vs Average sentiment
        loc_values = locationData(results['all_tweets'])
        results['ls_places'] = json.dumps(list(loc_values['places'])[1:11])
        results['ls_values'] = json.dumps(list(loc_values['sentiment'])[1:11])
        results['ls_counts'] = json.dumps(list(loc_values['counts'])[1:11])
        return render(request, "website/dashboard.html", results)
        # TODO: Parse the data in the front end to display the charts with the returned data
        

def dashboard(request):
    # if a get request was made, return the form as is
    if request.method == "GET":
        return render(request, "website/dashboard.html")

    # if a post reques was made, the user updated the number of tweets to pull so request again
    elif request.method == "POST":
        return index(request)


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

    dict_ = wordListToFreqDict(processed)
   
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
    for i in tweets:
        # remove the hastag cause it will apppear the most
        i = i.replace(str(hashtag).lower(), '')
        i = preprocess(i) #preprocess the tweet here
        for j in i.split():
            cleaned.append(j)

    return cleaned
def wordFrequency_Sentiment(words,alltweets):  
    wordf_sentiment = []
    for word in words:
        num_in = 0
        sentiment = 0
       
        for row in alltweets:
            ans = preprocess(row['tweet'])
            if word in ans:         
                num_in = num_in + 1
                sentiment = sentiment+ row['value']

        wordf_sentiment.append({"word":word,"n_in":num_in,"avg_sentiment":(sentiment/num_in) if num_in>0 else 0}) 

    return {"words":[d["word"] for d in wordf_sentiment],"counts":[d["n_in"] for d in wordf_sentiment],"sentiments":[d["avg_sentiment"] for d in wordf_sentiment]}

def locationData(alltweets):
   
    df = pd.DataFrame(alltweets)
    df2 = df.groupby('location',sort=False).agg({'value': ['mean','count']}).reset_index()
    sortedDF=df2.sort_values([('value', 'count')], ascending=False)
    dict =  sortedDF.to_dict()
   
    return {"places": list(dict.values())[0].values(),"sentiment": list(dict.values())[1].values(),"counts": list(dict.values())[2].values()}