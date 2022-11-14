from django.shortcuts import render, redirect
from .Tweepy_Pipeline.twitterPipeline import *


def index(request):
    """This method will return the default (home) page of our project where users are asked to enter a hashtag to be analysed"""

    # if a get request was made, return the form as is
    if request.method == "GET":
        return render(request, "website/index.html")

    # if a post reques was made, the user searched for a hashtag
    elif request.method == "POST":
        # extract the hashtag from the request
        print(request.POST)
        hashtag = request.POST.get("ht", None)
        upper_limit = request.POST.get("limit", None) # TODO: add a fiel to the UI that can gather an uper limit value from the user
        if hashtag is None:
            Context = {"msg": "Please be sure to enter a valid hashtag"}
            return render(request, "website/index.html", Context) 
        else:
            """We have the hashtag and can use it to perform the analysis"""
            data = acquire_tweets(hashtag, upper_limit)
            return data_visualizationPage(request, data)
            

def data_visualizationPage(request, data):
    if data is None:
        return redirect(index)
    else:
        # We process the data and return it in a format that can be visualized on the front end
        # TODO: make a call to the ML model and have the data processed
        # TODO: create a UI for the data visualization page and pass the data to it in a way that can be visualized
        return render(request, "website/index.html", {"msg": "The data has been displayed on the console for the time being"})  # TEMP
