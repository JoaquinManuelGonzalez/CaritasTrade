from datetime import date
from django.shortcuts import redirect, render
from data_base.models import ExchangePost

# Create your views here.
def create_post(request):
    if request.method == 'GET':# and request.session.get("id"):
        if not request.session.get("id"):
           request.session["id"] = 1
        return render(request, 'create_post.html')
    elif request.method == 'POST':# and request.sesssion.get("id"):
        post = ExchangePost(
            affiliate_id = request.session.get("id"),
            product_category_id=request.POST['product_category_id'],
            title=request.POST['title'],
            image=request.POST['image'],
            description=request.POST['description'],
            timestamp= date.today(),
            is_active=True
        )
        post.save()
        return redirect('landing_page')
    else:
        return redirect('landing_page')