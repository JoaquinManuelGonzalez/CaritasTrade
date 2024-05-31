from django.shortcuts import render, redirect
from data_base.models import Workers, Branches
from create_worker.views import registration_form_worker
from edit_worker.views import edit_worker_profile

def see_workers(request):
    if request.session.get("role") != "admin":
        return redirect("list_products")
    workers = Workers.objects.all().exclude(email='caritas_trade_grupo38@outlook.com')
    return render(request, "see_workers.html", {"workers": workers, "session_id": request.session.get("id"), "user_session": False, "failure_message": None, "success_message": None,}) 

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
    if request.method == "POST":
        worker_id = request.POST.get("id")
        workers = Workers.objects.all().exclude(email='caritas_trade_grupo38@outlook.com')
        if (Branches.objects.filter(worker_id=worker_id).first()):
            return render(request, "see_workers.html", {"workers": workers, "session_id": request.session.get("id"), "user_session": False, "failure_message": "El ayudante no puede eliminarse porque esta asignado a una filial", "success_message": None,})         
        else:
            worker = Workers.objects.get(id=worker_id)
            worker.delete()
            return render(request, "see_workers.html", {"workers": workers, "session_id": request.session.get("id"), "user_session": False, "failure_message": None,
            "success_message": "Ayudante eliminado exitosamente",})       
    return redirect("see_workers")
    
