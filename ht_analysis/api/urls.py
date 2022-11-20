from django.urls import path
from . import views

urlpatterns = [

    path('', views.list, name = "list_functions"), # This will display a list of the available functions from our API

    path("Analyse", views.analyze_hashtag, name = "analyse"), # This method takes in a hashtag, retrieves the data from twitter, analyses it and returns the result

    path("Tweets", views.get_tweets, name = "get_tweets") # This methid simply retrieves tweets for a given hashtag

]
