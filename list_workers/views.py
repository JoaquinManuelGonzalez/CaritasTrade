from django.shortcuts import render, redirect
from data_base.models import Workers
from create_worker.views import registration_form_worker
from edit_worker.views import edit_worker_profile

def see_workers(request):
    if request.session.get("role") != "admin":
        return redirect("list_products")
    workers = Workers.objects.all().exclude(email='caritas_trade_grupo38@outlook.com')
    return render(request, "see_workers.html", {"workers": workers, "session_id": request.session.get("id"), "user_session": False,})

def create_worker(request):
    if request.session.get("role") != "admin":
        return redirect("list_products")
    return registration_form_worker(request)

def edit_worker(request):
    if request.session.get("role") != "admin":
        return redirect("list_products")
    return edit_worker_profile(request, request.GET.get("id"))

def delete_worker(request):
    if request.session.get("role") != "admin":
        return redirect("list_products")
    return redirect("see_workers")
    
