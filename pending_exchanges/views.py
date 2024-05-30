from django.shortcuts import render
from view_profile.views import session_name
from data_base.models import Exchange


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