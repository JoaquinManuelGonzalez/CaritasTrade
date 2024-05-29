from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from data_base.models import Affiliate, Reputation
from django.shortcuts import redirect

def view_pending_score(request):
    role = request.session.get("role")
    if role == "user":
        id = request.session.get("id")
        session_name = Affiliate.objects.get(id=id).name
        pending_scores = Reputation.objects.filter(comes_from_affiliate=id, to_do=True)

        if not pending_scores.exists():
            message = "No hay puntuaciones pendientes por asignar."
        else:
            message = ""

        return render(
            request,
            "pending_score.html",
            {
                "message": message,
                "pending_scores": pending_scores,
                "user_session": False,
                "session_id": id,
                "session_name": session_name,
                "star_range": range(6),
            },
        )
    else:
        return HttpResponseRedirect("landing_page")

def submit_score(request, reputation_id):
    reputation = get_object_or_404(Reputation, id=reputation_id)
    
    if request.method == "POST":
        score = request.POST.get("score")
        
        if score is not None:
            score = int(score)
            reputation.reputation = score
            reputation.to_do = False
            reputation.save()
            return redirect("view_pending_score")
        else:
            # Manejar el caso en que no se haya seleccionado ningún puntaje
            return render(request, "submit_score.html", {
                "reputation": reputation,
                "error_message": "Por favor selecciona una puntuación."
            })

    return render(request, "submit_score.html", {"reputation": reputation})
