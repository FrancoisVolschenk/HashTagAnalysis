from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from website.ml_pipeline.ml import *
from website.Tweepy_Pipeline.twitterPipeline import *
# Create your views here.

@api_view(["GET"])
def list(request):
    """This method returns a list of methods available via our API"""
    msg = ['Analyse: A POST method, expects body parameters "ht" which is the hashtag you wish to analyse. Optional parameter "num", sets the upper limit for the number of tweets to retrieve']
    msg.append('Tweets: A GET method, expects URL parameers "ht" which is the hashtag you wish to analyse. Optional parameter "num", sets the upper limit for the number of tweets to retrieve')
    return Response({"msg": msg})

@api_view(["POST"])
def analyze_hashtag(request):
    """This method takes in a hashtag, retrieves a set amount of tweets from twitter and analyzes it with the ML model then returns the result of the analysis"""
    if request.POST.get("ht", None) is None:
        return Response({"msg": "POST body should include the following paratemers: <ht: the hashtag to be analysed>, <num: (optional) The upper limit for the number of tweets to analyse. Defaullt is 300>"})
    else:
        hashtag = request.POST["ht"]
        if not(hashtag.startswith("#")):
            hashtag = "#" + hashtag
        upper_lim = int(request.POST.get("num", 300))

        data = acquire_tweets(hashtag, int(upper_lim))
        analysis = predict_sentiment(data)

        response = {"msg": f"Successful analysis @{timezone.now()}",
                    "raw_data": data,
                    "analysis_results": analysis}
        return Response(response)

@api_view(["GET"])
def get_tweets(request):
    """This method takes in a hashtag, retrieves a set amount of tweets from twitter and analyzes it with the ML model then returns the result of the analysis"""
    if request.GET.get("ht", None) is None:
        return Response({"msg": "GET should include the following paratemers: <ht: the hashtag to be analysed>, <num: (optional) The upper limit for the number of tweets to analyse. Defaullt is 300>"})
    else:
        hashtag = request.GET["ht"]
        if not(hashtag.startswith("#")):
            hashtag = "#" + hashtag
        upper_lim = int(request.GET.get("num", 300))

        data = acquire_tweets(hashtag, int(upper_lim))

        response = {"msg": f"Successful retrieval @{timezone.now()}",
                    "tweets": data}
        return Response(response)
