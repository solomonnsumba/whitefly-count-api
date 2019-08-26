from django.http import HttpResponse
import datetime

def hello(request):
    text = """<h1>welcome to my app !</h1>"""
    return HttpResponse(text)