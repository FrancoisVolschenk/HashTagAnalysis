import json
from django.shortcuts import render, redirect
from .Tweepy_Pipeline.twitterPipeline import *
from .ml_pipeline.ml import *
from .data_visualization.processing import *

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
    """This method analyses the retrieved data and returns the results to be displayed in the front end in a data dashboard"""
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
        # results['msg'] = "The data has been displayed on the console for the time being"

        # For  Tweets' table
        results['all_tweets'] = results['positive'] + \
            results['unsure'] + results['negative']

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

        frq = wordFrequency([d['tweet']
                            for d in results['all_tweets']], hashtag)
        frq_values = [x[0] for x in frq]
        frq_words = [x[1] for x in frq]
        results['freq_words'] = json.dumps(
            frq_words[0:10])  # 10 most frequent words
        results['freq_values'] = json.dumps(
            frq_values[0:10])  # values of the 10 most frequent words

        # Word Frequency with sentiment
        wf_sentiment = wordFrequency_Sentiment(
            frq_words[0:10], results['all_tweets'])

        results['wfs_words'] = json.dumps(wf_sentiment['words'])
        results['wfs_pos'] = json.dumps(wf_sentiment['pos'])
        results['wfs_neu'] = json.dumps(wf_sentiment['neu'])
        results['wfs_neg'] = json.dumps(wf_sentiment['neg'])

        # UserLocation vs Average sentiment
        # Some tweets don't have the user's location and their bar will appear without a label on the graph as they are grouped together,
        # need to check if it exists and filter it out later
        loc_values = locationData(results['all_tweets'])
        results['ls_places'] = json.dumps(loc_values['places'][0:10])
        results['ls_pos'] = json.dumps(loc_values['pos'][0:10])
        results['ls_neu'] = json.dumps(loc_values['neu'][0:10])
        results['ls_neg'] = json.dumps(loc_values['neg'][0:10])
        return render(request, "website/dashboard.html", results)


def dashboard(request):
    # if a get request was made, return the form as is
    if request.method == "GET":
        return render(request, "website/dashboard.html")

    # if a post reques was made, the user updated the number of tweets to pull so request again
    elif request.method == "POST":
        return index(request)


