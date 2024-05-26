from django.http import HttpResponse
from django.shortcuts import redirect, render
from data_base.models import ExchangeSolicitude, ExchangePost, Affiliate


# Create your views here.
def see_exchange_requests(request):
    if not request.session.get("id") and not request.session.get("role") == "user":
        return redirect("landing_page")
    requests = ExchangePost.objects.filter(
        affiliate_id=request.session.get("id"), is_active=True
    )
    print(requests)
    requests = ExchangeSolicitude.objects.filter(
        exchange_post_for_id__in=requests, denied=False
    )
    print(requests)
    print(request.session.get("id"))
    return render(
        request,
        "see_exchange_requests.html",
        {
            "requests": requests,
            "user_session": False,
            "session_id": request.session.get("id"),
            "session_name": Affiliate.objects.get(id=request.session.get("id")).name,
        },
    )

def register_exchange(request):
    return HttpResponse("Register exchange")