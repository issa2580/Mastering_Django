from django.shortcuts import render
from django.http import HttpResponse

def say_hello_world(request):
    return HttpResponse("Hello World !")
