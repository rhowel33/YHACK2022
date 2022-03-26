from django.shortcuts import render
from django.http import HttpResponse

def landing(request):
    return HttpResponse("Put a button here that generates a speech.")

# Create your views here.
