from django.shortcuts import render, redirect
from django.utils import timezone
from data_base.models import Donation
from .forms import DonationForm
from .mercadopago import mp, create_preference


def donation_view(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation_amount = form.cleaned_data["amount"]

            preference = create_preference(donation_amount)

            if preference:
                return redirect(preference["response"]["init_point"])
            else:
                return render(
                    request,
                    "donation_error.html",
                    {
                        "error": "No se pudo conectar con MercadoPago. Inténtelo de nuevo más tarde."
                    },
                )
    else:
        form = DonationForm()
    return render(request, "donation.html", {"form": form})


def donation_success_view(request):
    payment_id = request.GET.get("payment_id")
    if payment_id:
        payment = mp.payment().get(payment_id)
        if payment["response"]["status"] == "approved":
            donation_amount = payment["response"]["transaction_amount"]
            donation = Donation(amount=donation_amount, timestamp=timezone.now())
            donation.save()
            return render(request, "donation_success.html")
    return redirect("donation_failure")


def donation_failure_view(request):
    return render(request, "donation_failure.html")


def donation_pending_view(request):
    return render(request, "donation_pending.html")


# cuenta para donar:
#     user: TESTUSER1306388221
#     pass: eZXl4e3OXr
