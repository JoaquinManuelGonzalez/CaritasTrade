import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from data_base.models import (
    ExchangeSolicitude,
    ExchangePost,
    Affiliate,
    Workers,
    Exchange,
    Reputation,
)


# Create your views here.
def see_exchange_requests(request):
    if not request.session.get("id") and not request.session.get("role") == "user":
        return redirect("landing_page")
    requests = ExchangePost.objects.filter(
        affiliate_id=request.session.get("id"), is_active=True
    )
    requests = ExchangeSolicitude.objects.filter(
        exchange_post_for_id__in=requests, denied=False
    )
    requests = requests.exclude(
        id__in=Exchange.objects.filter().values_list(
            "exchange_solicitude_id", flat=True
        )
    )
    active_exchanges = (
        Exchange.objects.filter(
            affiliate_1_id=request.session.get("id"), timestamp__isnull=True
        ).count()
        + Exchange.objects.filter(
            affiliate_2_id=request.session.get("id"), timestamp__isnull=True
        ).count()
    )
    return render(
        request,
        "see_exchange_requests.html",
        {
            "requests": requests,
            "user_session": False,
            "session_id": request.session.get("id"),
            "session_name": Affiliate.objects.get(id=request.session.get("id")).name,
            "active_exchanges": active_exchanges,
        },
    )


def register_exchange(request):
    if not request.session.get("id") and not request.session.get("role") == "worker":
        return redirect("landing_page")
    if request.method == "GET":
        return render(
            request,
            "register_exchange.html",
            {
                "user_session": False,
                "session_id": request.session.get("id"),
                "session_name": Workers.objects.get(id=request.session.get("id")).name,
            },
        )


def get_penalized_affiliate(code):
    if Exchange.objects.filter(code1=code, timestamp__isnull=True).exists():
        exchange = Exchange.objects.get(code1=code, timestamp__isnull=True)
        exchange.timestamp = datetime.datetime.now()
        exchange.save()
        finish_post(exchange)
        return Exchange.objects.get(code1=code).affiliate_2
    elif Exchange.objects.filter(code2=code, timestamp__isnull=True).exists():
        exchange = Exchange.objects.get(code2=code, timestamp__isnull=True)
        exchange.timestamp = datetime.datetime.now()
        exchange.save()
        finish_post(exchange)
        return Exchange.objects.get(code2=code).affiliate_1
    return None


def finish_post(exchange):
    exchange_solicitude = exchange.exchange_solicitude
    post_for = exchange_solicitude.exchange_post_for_id
    in_post = exchange_solicitude.in_exchange_post_id
    post_for.is_finished = True
    post_for.save()
    in_post.is_finished = True
    in_post.save()


def penalize_affiliate(affiliate):
    if affiliate.points > 0:
        affiliate.points -= 1
        affiliate.save()
    return f"Se ha penalizado al usuario {affiliate.name}"


def validate_exchange_codes(request):
    if (
        request.method != "POST"
        or not request.session.get("id")
        or request.session.get("role") != "worker"
    ):
        return render(
            request,
            "message.html",
            {"message": "Operación no permitida", "type_of_alert": "danger"},
        )

    code1, code2 = request.POST.get("code_1"), request.POST.get("code_2")
    
    message = "Alguno o ambos de los códigos son inválidos"
    type_of_alert = "danger"

    if code1 and not code2:
        if Exchange.objects.filter(code1=code1, timestamp__isnull=True).exists() and not Exchange.objects.get(code1=code1, timestamp__isnull=True).exchange_date == datetime.datetime.now().date():
            message = "Este intercambio no tiene turno para el dia actual"
            type_of_alert = "danger"
        elif Exchange.objects.filter(code2=code1, timestamp__isnull=True).exists() and not Exchange.objects.get(code1=code1, timestamp__isnull=True).exchange_date == datetime.datetime.now().date():
            message = "Este intercambio no tiene turno para el dia actual"
            type_of_alert = "danger"
        else:
            penalized_affiliate = get_penalized_affiliate(code1)
            if penalized_affiliate:
                message = penalize_affiliate(penalized_affiliate)
                type_of_alert = "success"

    elif not code1 and code2:
        if Exchange.objects.filter(code1=code2, timestamp__isnull=True).exists() and not Exchange.objects.get(code1=code1, timestamp__isnull=True).exchange_date == datetime.datetime.now().date():
            message = "Este intercambio no tiene turno para el dia actual"
            type_of_alert = "danger"
        elif Exchange.objects.filter(code2=code2, timestamp__isnull=True).exists() and not Exchange.objects.get(code1=code1, timestamp__isnull=True).exchange_date == datetime.datetime.now().date():
            message = "Este intercambio no tiene turno para el dia actual"
            type_of_alert = "danger"
        else:
            penalized_affiliate = get_penalized_affiliate(code2)
            if penalized_affiliate:
                message = penalize_affiliate(penalized_affiliate)
                type_of_alert = "success"

    elif code1 and code2:
        exchange = (
            Exchange.objects.filter(
                code1=code1, code2=code2, timestamp__isnull=True
            ).first()
            or Exchange.objects.filter(
                code1=code2, code2=code1, timestamp__isnull=True
            ).first()
        )
        if exchange:
            if not exchange.exchange_date == datetime.datetime.now().date():
                message = "Este intercambio no tiene turno para el dia actual"
                type_of_alert = "danger"
            else:
                exchange.timestamp = datetime.datetime.now()
                exchange.affiliate_1.points += 1
                exchange.affiliate_2.points += 1
                exchange.affiliate_1.save()
                exchange.affiliate_2.save()
                finish_post(exchange)
                new_rep1 = Reputation.objects.create(
                    reputation=3.0,
                    affiliate=exchange.affiliate_1,
                    to_do=True,
                    comes_from_affiliate=exchange.affiliate_2,
                )
                new_rep1.save()
                new_rep2 = Reputation.objects.create(
                    reputation=3.0,
                    affiliate=exchange.affiliate_2,
                    to_do=True,
                    comes_from_affiliate=exchange.affiliate_1,
                )
                new_rep2.save()
                exchange.save()
                message = "Se ha registrado el intercambio de forma exitosa"
                type_of_alert = "success"

    return render(
        request, "message.html", {"message": message, "type_of_alert": type_of_alert}
    )


def return_error_message_regarding_active_exchanges(request):
    return render(
        request,
        "message.html",
        {
            "message": "La cantidad de intercambios activos alcanzo el maximo",
            "type_of_alert": "danger",
        },
    )


def delete_request(request, id):
    if not request.session.get("id") and not request.session.get("role") == "user":
        return redirect("landing_page")
    exchange_request = ExchangeSolicitude.objects.get(id=id)
    exchange_request.denied = True
    exchange_request.save()
    requests = ExchangePost.objects.filter(
        affiliate_id=request.session.get("id"), is_active=True
    )
    requests = ExchangeSolicitude.objects.filter(
        exchange_post_for_id__in=requests, denied=False
    )
    requests = requests.exclude(
        id__in=Exchange.objects.values_list("exchange_solicitude_id", flat=True)
    )
    active_exchanges = (
        Exchange.objects.filter(
            affiliate_1_id=request.session.get("id"), timestamp__isnull=True
        ).count()
        + Exchange.objects.filter(
            affiliate_2_id=request.session.get("id"), timestamp__isnull=True
        ).count()
    )
    return render(
        request,
        "see_exchange_requests.html",
        {
            "requests": requests,
            "user_session": False,
            "session_id": request.session.get("id"),
            "session_name": Affiliate.objects.get(id=request.session.get("id")).name,
            "active_exchanges": active_exchanges,
            "message": "Intercambio rechazado con exito",
        },
    )
