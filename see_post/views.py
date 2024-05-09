from django.shortcuts import render
from data_base.models import ExchangePost
# Create your views here.
def see_post(request, id):
    post = ExchangePost.objects.get(id=id)
    return render(request,'see_post.html', {
            'post': post
        })
    # if request.method == 'GET' and request.session.get("id"):
        # post = ExchangePost.objects.get(id=id)
        # return render(request,'see_post.html', {
        #         'post': post
        #     })
    # else:
    #     return redirect('landing_page')