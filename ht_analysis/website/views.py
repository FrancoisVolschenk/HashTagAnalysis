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
            return data_visualizationPage(request, data)
            

def data_visualizationPage(request, data):
    if data is None:
        return redirect(index)
    else:
        # We process the data and return it in a format that can be visualized on the front end
        # make a call to the ML model and have the data processed
        results = predict_sentiment(data)
        # save the word clouds so that they can be displayed on the web page
        results['wc_p'].save("website/static/website/img/wc_p.jpg")
        results['wc_n'].save("website/static/website/img/wc_n.jpg")
        results['wc_u'].save("website/static/website/img/wc_u.jpg")
        # print(results)
        results['msg'] = "The data has been displayed on the console for the time being" #Temp
        
        return render(request, "website/dashboard.html", results)
        # TODO: Parse the data in the front end to display the charts with the returned data
