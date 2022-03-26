from django.shortcuts import render
from django.http import HttpResponse

def landing(request):
    with open("../generated/test_speech.txt") as fin:
        text = fin.read()
    return HttpResponse(text)

