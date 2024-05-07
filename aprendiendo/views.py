from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .forms import createNewTask
from data_base.models import Reputation, Affiliate
# Create your views here.


def hello2(request, username):
    print(username)
    return HttpResponse("<h2>chau %s</h2> " % username)


def afiliados(request):
    affiliate = list(Affiliate.objects.values())
    return JsonResponse(affiliate, safe=False)


def afiliados2(request):
    affiliates=Affiliate.objects.all()
    return render(request, 'afiliados2.html', {
        "affiliates" : affiliates
    })


def prueba_render(request):
    title= "la reyna del nilo"
    return render(request, 'profile.html',{
        "title" : title,
    })


def createAfiliado(request):
    print(request.GET)
     #para crear ahora un objeto y poner los datos del extraidos del form, 1ero creo reputacion y luego afiliado
    if request.method == 'GET':
        return render (request, 'create_new_task.html',{
        'form': createNewTask()
        })
    else:
        # Crear un objeto Reputation
        reputation=Reputation.objects.create()
        # Crear un objeto Affiliate, asignando la clave foránea al objeto Reputation creado anteriormente
        Affiliate.objects.create(dni=request.POST['dni'],
        email=request.POST['email'],
        name = request.POST['name'], 
        surname = request.POST['surname'],
        phone_number = request.POST['phone_number'],
        password=request.POST['password'],
        birth_day='',
        reputation_id=reputation)
        # Redirigir a la página de afiliados
        return redirect('afiliado')


def mostrarDatos (request, id):
    usuario = get_object_or_404(Affiliate,id=id)  #mostrar el 404 es lo correcto si no encuentra el objeto
    print(id)
    print(usuario)
    return render (request, 'usuario.html',{
        'usuario' : usuario
    })