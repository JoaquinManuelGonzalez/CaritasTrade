from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def edit_profile(request):
    print("holi")
    return HttpResponse("<h1>holi</h1>")