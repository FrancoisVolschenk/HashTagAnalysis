from django.shortcuts import render, redirect


def index(request):
    """This method will return the default (home) page of our project where users are asked to enter a hashtag to be analysed"""

    # if a get request was made, return the form as is
    if request.method == "GET":
        return render(request, "website/index.html")

    # if a post reques was made, the user searched for a hashtag
    elif request.method == "POST":
        # extract the hashtag from the request
        hashtag = request.POST.get("ht", None)
        if hashtag is None:
            Context = {"msg": "Please be sure to enter a valid hashtag"}
            return render(request, "website/index.html", Context) 
        else:
            """We have the hashtag and can use it to perform the analysis"""
            return data_visualizationPage(request, hashtag)
            

def data_visualizationPage(request, hashtag = None):
    if hashtag is None:
        return redirect(index)
    else:
        pass
        """We process the data and return it in a format that can be visualized on the front end"""
