from django.shortcuts import render
from django.urls import reverse
from data_base.models import ExchangePost
from django.http import HttpResponseRedirect


# Create your views here.
def delete_post(request, id):
    if request.method == "POST" and request.session.get("id"):
        post_id = id
        post = ExchangePost.objects.get(id=post_id)
        post.is_active = False
        post.save()
        profile_url = reverse(
            "view_profile", kwargs={"id": request.session.get("id")}
        )
        return HttpResponseRedirect(profile_url)
    else:
        return HttpResponseRedirect("landing_page")
