from django.shortcuts import render

from data_base.models import Branches, Workers

def list_branches(request):
    branches = Branches.objects.all()
    workers = [Workers.objects.get(id=branch.worker_id) for branch in branches]
    branches_workers = zip(branches, workers)
    return render(request, "branches_management.html", {
        "session_id" : request.session.get("id"),
        "user_session" : False,
        "branches_workers" : branches_workers
    })
