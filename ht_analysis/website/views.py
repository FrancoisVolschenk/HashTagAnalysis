import code
from multiprocessing import context
from django.shortcuts import render
import random

# Create your views here.
def index(request):
    Context = {"numbers": []}
    for i in range(10):
        Context["numbers"].append(random.randint(0, 100))

    return render(request, "website/index.html", Context)
