import datetime
from django.shortcuts import redirect, render
from data_base.models import ExchangePost, ProductCategory
from .forms import ExchangeForm
# Create your views here.
def create_post(request):    
    if request.method == 'GET':# and request.session.get("id"):
        if not request.session.get("id"):
           request.session["id"] = 1
        form = ExchangeForm()
        return render(request, 'create_post.html', {
            'categories': ProductCategory.objects.all(),
            "form": form,
        })
    elif request.method == 'POST':# and request.sesssion.get("id"):
        form = ExchangeForm(request.POST)
        if form.is_valid():
            print("Es valido caralho")
        else:
            print(form.errors)
        return redirect('landing_page')
    else:
        return redirect('landing_page')