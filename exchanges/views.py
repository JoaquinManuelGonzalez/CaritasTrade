from django.shortcuts import redirect, render
from data_base.models import ExchangeSolicitude, ExchangePost


# Create your views here.
def see_exchange_requests(request):
    if not request.session.get("id") and not request.session.get("role") == "user":
        return redirect("landing_page")
    requests = ExchangePost.objects.filter(
        affiliate_id=request.session.get("id"), is_active=True
    )
    requests = ExchangeSolicitude.objects.filter(
        in_exchange_post_id__in=requests, denied=False
    )
    return render(request, "see_exchange_requests.html", {"requests": requests})
