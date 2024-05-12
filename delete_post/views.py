from django.shortcuts import render
from django.urls import reverse
from data_base.models import ExchangePost, Affiliate
from django.http import HttpResponseRedirect


# Create your views here.
def delete_post(request, id):
    if request.method == "POST" and request.session.get("id"):
        post_id = id
        post = ExchangePost.objects.get(id=post_id)
        creator = Affiliate.objects.get(id=post.affiliate_id)
        if creator.id == request.session.get("id"):
            post.delete()
        profile_url = reverse(
            "view_profile", kwargs={"id": request.session.get("id")}
        )
        return HttpResponseRedirect(profile_url)
    else:
        return HttpResponseRedirect("landing_page")
