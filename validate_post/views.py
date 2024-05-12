from django.shortcuts import render
from data_base.models import ExchangePost

# Create your views here.

def see_waiting_posts(request):
    posts = ExchangePost.objects.filter(is_active=False, is_rejected=False)
    return render(request, "see_waiting_posts.html", {"posts": posts})
