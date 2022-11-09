from django.urls import path
from . import views

"""From here, we use the URL to determine where to send the user"""
urlpatterns = [

    path('', views.index, name="home"), # This is the default path, it sends the user to the index.html page

]
