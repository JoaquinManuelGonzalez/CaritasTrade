from django.shortcuts import render


def pending_exchanges_management(request):
    session_id = request.session.get("id")
    user_session = session_id == id

    return render(request, "pending_exchanges_management.html", {
        "session_id": session_id,
        "user_session": user_session
    })