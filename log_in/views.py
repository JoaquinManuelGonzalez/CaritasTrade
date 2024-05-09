from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import Login_Form

def login_view(request):
    return render(request, "log_in.html")