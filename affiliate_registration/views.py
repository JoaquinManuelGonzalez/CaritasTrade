from django.shortcuts import render

# Create your views here.
def registration_form(request):
    return render(request, "registration_form.html")