import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from places.models import Place


def serialize_place(place):
    return {
        'title': place.title,
        'imgs': [image.image.url for image in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat,
        },
    }


def serialize_geojson(places):
    features = [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lng, place.lat],
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': f'/places/{place.id}/',
            },
        }
        for place in places
    ]
    return {
        'type': 'FeatureCollection',
        'features': features,
    }


def show_map(request):
    places = Place.objects.all()
    context = {
        'places_geojson': json.dumps(serialize_geojson(places), ensure_ascii=False),
    }
    return render(request, 'index.html', context)


def place_detail(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related('images'), id=place_id)
    return JsonResponse(serialize_place(place), json_dumps_params={'ensure_ascii': False})
