from django.shortcuts import render
from view_profile.views import session_name
from data_base.models import Exchange
from log_in.views import generate_otp, send_email



def pending_exchanges_management(request):
    session_id = request.session.get("id")
    user_session = session_id == id
    pending_exchanges = list(
        Exchange.objects.filter(
            affiliate_2_id=session_id,
            is_confirmed=False,
        )
    )

    return render(request, "pending_exchanges_management.html", {
        "session_id": session_id,
        "user_session": user_session,
        "session_name": session_name(request),
        "pending_exchanges": pending_exchanges,
    })

def accept_exchange(request, exchange_id):
    session_id = request.session.get("id")
    user_session = session_id == id
    pending_exchanges = list(
        Exchange.objects.filter(
            affiliate_2_id=session_id,
            is_confirmed=False,
        )
    )

    exchange = Exchange.objects.get(id=exchange_id)
    affiliate_1 = exchange.affiliate_1
    affiliate_2 = exchange.affiliate_2
    
    exchange.is_confirmed = True
    exchange.code1 = generate_otp(5)
    exchange.code2 = generate_otp(5)
    exchange.save()
    send_email(affiliate_1.email, f"OTP para confirmar el intercambio con el usuario: {affiliate_2.name} {affiliate_2.surname}", "OTP: " + str(exchange.code1) + f" Contáctese con el usuario {affiliate_2.name} {affiliate_2.surname} para pactar su horario de encuentro a través de este email {affiliate_2.email}")
    send_email(affiliate_2.email, f"OTP para confirmar el intercambio con el usuario: {affiliate_1.name} {affiliate_1.surname}", "OTP: " + str(exchange.code2) + f" Contáctese con el usuario {affiliate_1.name} {affiliate_1.surname} para pactar su horario de encuentro a través de este email {affiliate_1.email}")
    success_message = "El intercambio ha sido confirmado exitosamente."
    return render(request, "pending_exchanges_management.html", {
        "session_id": session_id,
        "user_session": user_session,
        "success_message": success_message,
        "session_name": session_name(request),
        "pending_exchanges": pending_exchanges,
    })

def reject_exchange(request, exchange_id):
    exchange = Exchange.objects.get(id=exchange_id)
    exchange.is_confirmed = False
    exchange.save()
    return render(request, "exchange_rejected.html", {
        "session_id": request.session.get("id"),
        "user_session": False,
        "session_name": session_name(request),
        "exchange": exchange,
    })