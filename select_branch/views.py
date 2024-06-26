from django.shortcuts import render
from django.contrib import messages
from datetime import datetime, timedelta
from data_base.models import Branches, Exchange, ExchangeSolicitude, Affiliate
from view_profile.views import session_name
from log_in.views import send_email

def select_branch(request, solicitude_id):
    session_id = request.session.get("id")
    user_session = session_id == id

    branches = Branches.objects.all()
    available_branches_by_date = {}
    # Obtener la fecha actual
    fecha_actual = datetime.now()
    # Calcular la fecha de fin (6 meses a partir de la fecha actual)
    fecha_fin = fecha_actual + timedelta(days=1*30)  # Aproximadamente 6 meses
    # Inicializar la fecha actual para iterar
    fecha_iter = fecha_actual
    # Iterar desde la fecha actual hasta la fecha de fin
    while fecha_iter <= fecha_fin:
        if fecha_iter.weekday() in [5, 6]:
            available_branches = []
            for branch in branches:
                reservations_count = Exchange.objects.filter(branch=branch.id, exchange_date=fecha_iter.date()).count()
                if reservations_count < 1: #Ese número se debe cambiar a 50 (cantidad de turnos que puede tener una filial por día)
                    available_branches.append(branch)
            if available_branches:
                available_branches_by_date[fecha_iter.strftime("%Y-%m-%d")] = available_branches
        fecha_iter += timedelta(days=1)
    if request.method == "POST":
        exchange_date = request.POST.get("exchange_date")
        exchange_branch = request.POST.get("exchange_branch")
        if not exchange_branch:
            messages.error(request, "Por favor, selecciona una filial para continuar.")
            return render(request, 'select_branch.html', {
                "session_id": session_id,
                "user_session": user_session,
                "session_name": session_name(request),
                "solicitude_id": solicitude_id,
                "available_branches_by_date": available_branches_by_date
            })
        exchange_solicitude = ExchangeSolicitude.objects.get(id=solicitude_id)
        affiliate_1 = Affiliate.objects.get(id=session_id)
        affiliate_2 = exchange_solicitude.affiliate_id
        exchange = Exchange(
            exchange_date=datetime.strptime(exchange_date, "%Y-%m-%d"),
            branch=Branches.objects.get(id=exchange_branch),
            exchange_solicitude=exchange_solicitude,
            affiliate_1=affiliate_1,
            affiliate_2=affiliate_2
        )
        exchange.save()
        send_email(affiliate_2.email, "Nueva Propuesta de Filial y Fecha para Intercambio", f"El usuario {affiliate_1.name} {affiliate_1.surname} te ha enviado una nueva propuesta de filial y fecha para el intercambio de {exchange_solicitude.exchange_post_for_id.title} por {exchange_solicitude.in_exchange_post_id.title}. Por favor, confirma o rechaza la nueva propuesta generada.")
        return render(request, "success_message_exchange.html")     
    return render(request, 'select_branch.html', {
        "session_id": session_id,
        "user_session": user_session,
        "session_name": session_name(request),
        "solicitude_id": solicitude_id,
        "available_branches_by_date": available_branches_by_date
    })