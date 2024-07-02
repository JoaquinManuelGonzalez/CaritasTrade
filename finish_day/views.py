from django.shortcuts import render, redirect
from data_base.models import Exchange, Branches, Affiliate
from django.utils import timezone
from exchanges.views import fail_post

def penalize_affiliate(affiliate):
    if affiliate.points > 0:
        affiliate.points -= 1
        affiliate.save()

def finish_day(request):
    if request.session.get("role") != "worker":
        return redirect("list_products")
    branch = Branches.objects.filter(worker_id=request.session.get("id")).first()
    if (branch):
        exchanges = Exchange.objects.filter(branch_id=branch.id, exchange_date__lte=timezone.now().date(), timestamp__isnull=True).all()
        if (exchanges):
            for exchange in exchanges:
                exchange.timestamp=timezone.now()
                exchange.has_failed=True
                exchange.save()
                penalize_affiliate(exchange.affiliate_1)
                penalize_affiliate(exchange.affiliate_2)
                fail_post(exchange)
            return render(request, "success_day_message.html")
        else:
            return render(request, "empty_day_message.html")
    else:
        return render(request, "no_branch_message.html")
