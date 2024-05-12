import base64
from  django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render
from data_base.models import Affiliate, ExchangePost, ProductCategory, Reputation

def list_products2(request):
    return HttpResponse("<h1> Hola virgi gi gi gi</h1>")

def list_products(request):
    post = ExchangePost.objects.filter(is_active=True)
    # Lógica para procesar la búsqueda y los filtros
    # Puedes usar request.GET para acceder a los parámetros de la URL
    query = request.GET.get('q')
    category = request.GET.get('category')
    response_rating = request.GET.get('rating')

    if query:
        post = post.filter( title__icontains=query)
    if category:
        post = post.filter(product_category_id=category)
    
    if response_rating:
        rating = float(response_rating)

        id_de_afiliados_con_mayor = Reputation.objects.filter(reputation__gt=rating).values_list('affiliate', flat=True)
        afiliados_con_reputacion_mayor = Affiliate.objects.filter(id__in=id_de_afiliados_con_mayor)
        posteos_coincidentes = ExchangePost.objects.filter(
            affiliate_id__in=afiliados_con_reputacion_mayor, is_rejected=False, is_active=True
        )

        # if posteos_coincidentes:
        post = post.filter(id__in=posteos_coincidentes.values_list('id', flat=True))


        # # Primero, obtenemos el promedio de la reputación de cada afiliado
        # affiliate_reputation = Reputation.objects.values('affiliate').annotate(promedio_reputacion=Avg('reputation'))
        # # Luego, filtramos aquellos afiliados cuyo promedio de reputación es mayor que rating
        # affiliate_reputation_plus = affiliate_reputation.filter(promedio_reputacion__gt= rating)
        # # Ahora, buscamos los posteos de esos afiliados
        # post_with_reputation_plus = ExchangePost.objects.filter(affiliate_id__in=affiliate_reputation_plus)
        # #filtro los posteos con los post que tienen un puntaje mayor a RATiNG
        
                
    # decodifico las imagenes
    decoded_images = []
    for p in post:
        if p.image:
            image_data = p.image.decode('utf-8')
            decoded_images.append(image_data)
        else:
            decoded_images.append(None)
    
    combined_data = list(zip(decoded_images, post))
    categories = ProductCategory.objects.all()

    request.session['id'] = 1 # BORRARLO
    session_id = request.session.get("id")
    user_session = False

    return render(request, 'exchange_product_list.html', {
        'post': post,
        'session_id' : session_id,
        'user_session': user_session,
        'combined_data':combined_data,
        'categories' : categories,
        })