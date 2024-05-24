from django.shortcuts import render
import folium

from data_base.models import Branches

def view_map(request):
    bounds = [[-35.92145, -58.95453], [-33.92145, -56.95453]]
    map = folium.Map(location=[-34.92145, -57.95453], zoom_start=13, min_zoom=12, max_zoom=18)
    map.options['maxBounds'] = bounds
    branches = Branches.objects.all()
    [folium.Marker([branch.latitude, branch.altitude], popup=branch.name).add_to(map) for branch in branches]
    map_html = map._repr_html_()

    return render(request, "view_map.html", {
        'map_html' : map_html
    })
