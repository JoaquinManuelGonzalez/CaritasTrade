from django.shortcuts import render
from . import forms
from data_base.models import Branches, Workers
import folium


def capitalize_element(data):
    data_list = data.split()
    data_list_capitalized = [data.lower().capitalize() for data in data_list]
    data_capitalized = " ".join(data_list_capitalized)
    return data_capitalized


def create_map():
    bounds = [[-35.92145, -58.95453], [-33.92145, -56.95453]]
    map = folium.Map(location=[-34.92145, -57.95453], zoom_start=13, min_zoom=12, max_zoom=18)
    map.options['maxBounds'] = bounds
    map.add_child(folium.LatLngPopup())
    branches = Branches.objects.all()
    [folium.Marker([branch.latitude, branch.altitude], popup=branch.name, icon=folium.Icon(color="red",icon="church", prefix="fa")).add_to(map) for branch in branches]
    return map._repr_html_()


def list_branches(request):
    branches = Branches.objects.select_related('worker').all()
    return render(request, "branches_management.html", {
        "session_id": request.session.get("id"),
        "user_session": False,
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
            worker=branch_form.cleaned_data['worker']
            if (not available_workers.exists()):
                branch_form.add_error(
                    None,
                    "Actualmente no existen Ayudantes libres en el sistema."
                )
                return render(request, "create_branch.html", {
                    "session_id" : request.session.get("id"),
                    "user_session" : False,
                    'form': branch_form,
                    "map_html": map_html
                })
            elif (available_workers.exists()) and (worker == None):
                branch_form.add_error(
                    None,
                    "Por favor seleccione un Ayudante Libre."
                )
                return render(request, "create_branch.html", {
                    "session_id" : request.session.get("id"),
                    "user_session" : False,
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
                "session_id" : request.session.get("id"),
                "user_session" : False,
                'form': branch_form,
                'success_message': success_message,
                "map_html": map_html
            })
    else:
        branch_form = forms.BranchForm()
    return render(request, "create_branch.html", {
                "session_id" : request.session.get("id"),
                "user_session" : False,
                'form': branch_form,
                "map_html": map_html
            })