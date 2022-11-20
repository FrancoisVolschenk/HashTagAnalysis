from django.urls import path
from . import views

"""From here, we use the URL to determine where to send the user"""
urlpatterns = [

    path('', views.index, name="home"), # This is the default path, it sends the user to the index.html page
    path('dashboard', views.dashboard, name="dashboard") # This is the data visualization dashboard page
    #NOTE: the dashboard should only be accessible via the form on the index page after a hashtag has been sent
]
