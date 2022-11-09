import code
from multiprocessing import context
from unicodedata import name
from django.shortcuts import render
import random
from .models import Person

# Create your views here.
def index(request):
    Context = {"people": []}
    people = Person.objects.all()
    Context["people"] = people

    return render(request, "website/index.html", Context)
