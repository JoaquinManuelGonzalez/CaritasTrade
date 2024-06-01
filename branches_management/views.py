from django.shortcuts import render
from . import forms
from data_base.models import Branches, Workers, Exchange
from log_in.views import send_email
import folium
from view_profile.views import session_name


def capitalize_element(data):
    data_list = data.split()
    data_list_capitalized = [data.lower().capitalize() for data in data_list]
    data_capitalized = " ".join(data_list_capitalized)
    return data_capitalized


def check_latitude_and_existing_altitude(branch, latitude):
    return Branches.objects.filter(latitude=latitude, altitude=branch.altitude).exists()


def check_altitude_and_existing_latitude(branch, altitude):
    return Branches.objects.filter(latitude=branch.latitude, altitude=altitude).exists()


def create_map():
    bounds = [[-35.92145, -58.95453], [-33.92145, -56.95453]]
    map = folium.Map(location=[-34.92145, -57.95453],
                     zoom_start=13, min_zoom=12, max_zoom=18)
    map.options['maxBounds'] = bounds
    map.add_child(folium.LatLngPopup())
    branches = Branches.objects.all()
    [folium.Marker([branch.latitude, branch.altitude], popup=branch.name, icon=folium.Icon(
        color="red", icon="church", prefix="fa")).add_to(map) for branch in branches]
    return map._repr_html_()


def list_branches(request):
    branches = Branches.objects.select_related('worker').all()
    return render(request, "branches_management.html", {
        "session_id": request.session.get("id"),
        "user_session": False,
        "session_name": session_name(request),
        "branches": branches
    })


def create_branch(request):
    map_html = create_map()
    available_workers = Workers.objects.exclude(
        branches__isnull=False
    ).exclude(
        email="caritas_trade_grupo38@outlook.com"
    )
    if request.method == 'POST':
        branch_form = forms.BranchForm(request.POST)
        if branch_form.is_valid():
            worker = branch_form.cleaned_data['worker']
            if (not available_workers.exists()):
                branch_form.add_error(
                    None,
                    "Actualmente no existen Ayudantes libres en el sistema."
                )
                return render(request, "create_branch.html", {
                    "session_id": request.session.get("id"),
                    "user_session": False,
                    "session_name": session_name(request),
                    'form': branch_form,
                    "map_html": map_html
                })
            elif (available_workers.exists()) and (worker == None):
                branch_form.add_error(
                    None,
                    "Por favor seleccione un Ayudante Libre."
                )
                return render(request, "create_branch.html", {
                    "session_id": request.session.get("id"),
                    "user_session": False,
                    "session_name": session_name(request),
                    'form': branch_form,
                    "map_html": map_html
                })
            branch = Branches(
                worker=branch_form.cleaned_data['worker'],
                name=capitalize_element(branch_form.cleaned_data['name']),
                latitude=branch_form.cleaned_data['latitude'],
                altitude=branch_form.cleaned_data['altitude']
            )
            branch.save()
            success_message = "Filial creada exitosamente"
            return render(request, "create_branch.html", {
                "session_id": request.session.get("id"),
                "user_session": False,
                "session_name": session_name(request),
                'form': branch_form,
                'success_message': success_message,
                "map_html": map_html
            })
    else:
        branch_form = forms.BranchForm()
    return render(request, "create_branch.html", {
        "session_id": request.session.get("id"),
        "user_session": False,
        "session_name": session_name(request),
        'form': branch_form,
        "map_html": map_html
    })


def edit_branch(request, branch_id):
    branch = Branches.objects.get(id=branch_id)
    worker_in_charge = Workers.objects.get(id=branch.worker_id)
    map_html = create_map()
    if request.method == "POST":
        branch_form = forms.EditBranchForm(request.POST)
        if branch_form.is_valid():
            name = capitalize_element(branch_form.cleaned_data['name'])
            if name:
                branch.name = name
            latitude = branch_form.cleaned_data['latitude']
            if latitude:
                if check_latitude_and_existing_altitude(branch, latitude):
                    branch_form.add_error(
                        None,
                        "Una Filial con esta Latitud y Longitud ya existe en el sistema."
                    )
                    return render(request, "edit_branch.html", {
                        "session_id": request.session.get("id"),
                        "user_session": False,
                        "session_name": session_name(request),
                        "branch": branch,
                        "worker_in_charge": worker_in_charge,
                        "map_html": map_html,
                        "form": branch_form
                    })
                else:
                    branch.latitude = latitude
            altitude = branch_form.cleaned_data['altitude']
            if altitude:
                if check_altitude_and_existing_latitude(branch, altitude):
                    branch_form.add_error(
                        None,
                        "Una Filial con esta Latitud y Longitud ya existe en el sistema."
                    )
                    return render(request, "edit_branch.html", {
                        "session_id": request.session.get("id"),
                        "user_session": False,
                        "session_name": session_name(request),
                        "branch": branch,
                        "worker_in_charge": worker_in_charge,
                        "map_html": map_html,
                        "form": branch_form
                    })
                else:
                    branch.altitude = altitude
            worker = branch_form.cleaned_data['worker']
            if worker:
                branch.worker = worker
            branch.save()
            success_message = "Los datos de la Filial han sido editados exitosamente."
            return render(request, "edit_branch.html", {
                "session_id": request.session.get("id"),
                "user_session": False,
                "session_name": session_name(request),
                "branch": branch,
                "worker_in_charge": worker_in_charge,
                "map_html": map_html,
                'success_message': success_message
            })
    else:
        branch_form = forms.EditBranchForm()
    return render(request, "edit_branch.html", {
        "session_id": request.session.get("id"),
        "user_session": False,
        "session_name": session_name(request),
        "branch": branch,
        "form": branch_form,
        "worker_in_charge": worker_in_charge,
        "map_html": map_html
    })


def delete_branch(request, branch_id):
    branch = Branches.objects.get(id=branch_id)
    if Exchange.objects.filter(branch=branch.id, timestamp__isnull=True).exists():
        exchanges = Exchange.objects.filter(
            branch=branch.id, timestamp__isnull=True)
        for exchange in exchanges:
            affiliate_1 = exchange.affiliate_1
            affiliate_2 = exchange.affiliate_2
            send_email(affiliate_1.email, "Eliminación de Filial", f"Lamentamos informarle que el intercambio pendiente con el afiliado {affiliate_2.name} {affiliate_2.surname} en la fecha {exchange.exchange_date} de el producto {exchange.exchange_solicitude.exchange_post_for_id.title} por el producto {exchange.exchange_solicitude.in_exchange_post_id.title} no se podrá realizar debido a la eliminación de la filial {branch.name}. Hemos habilitado nuevamente la solicitud de intercambio que recibió de parte del afiliado {affiliate_2.name} {affiliate_2.surname} para que pueda elegir una nueva Filial para llevar a cabo su intercambio.")
            send_email(affiliate_2.email, "Eliminación de Filial", f"Lamentamos informarle que el intercambio pendiente con el afiliado {affiliate_1.name} {affiliate_1.surname} en la fecha {exchange.exchange_date} de el producto {exchange.exchange_solicitude.exchange_post_for_id.title} por el producto {exchange.exchange_solicitude.in_exchange_post_id.title} no se podrá realizar debido a la eliminación de la filial {branch.name}. Hemos habilitado nuevamente la solicitud de intercambio que realizó al afiliado {affiliate_1.name} {affiliate_1.surname} para que este último pueda elegir una nueva Filial para llevar a cabo su intercambio.")
        Exchange.objects.filter(branch=branch.id, timestamp__isnull=True).delete()
        Exchange.objects.filter(branch=branch.id).update(deleted=True)
    branch.delete()
    success_message = "La Filial ha sido eliminada exitosamente."
    return render(request, "branches_management.html", {
        "session_id": request.session.get("id"),
        "user_session": False,
        "session_name": session_name(request),
        "branches": Branches.objects.all(),
        'success_message': success_message
    })
