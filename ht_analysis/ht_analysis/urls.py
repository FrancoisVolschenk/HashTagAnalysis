
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls), # The admin site handles basic crud on our behalf

    path('', include("website.urls")), # This will redirect the user to the website

    #path("api/", include("api.urls")), # If we wish to add an API to make the service accessible to mobile apps or other programmers

]
