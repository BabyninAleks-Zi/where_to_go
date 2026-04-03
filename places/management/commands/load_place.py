from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from places.models import Place, PlaceImage


def get_json(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


def download_image(image_url):
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    return response.content


def get_filename_from_url(url):
    filename = Path(urlparse(url).path).name
    if filename:
        return filename
    return 'image.jpg'


class Command(BaseCommand):
    help = 'Загружает одно место по URL JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str)

    def handle(self, *args, **options):
        json_url = options['json_url']

        try:
            place_data = get_json(json_url)
        except requests.RequestException as error:
            raise CommandError(f'Не удалось скачать JSON: {error}')

        coordinates = place_data['coordinates']
        place, created = Place.objects.get_or_create(
            title=place_data['title'],
            defaults={
                'description_short': place_data['description_short'],
                'description_long': place_data['description_long'],
                'lng': float(coordinates['lng']),
                'lat': float(coordinates['lat']),
            },
        )

        if not created:
            place.description_short = place_data['description_short']
            place.description_long = place_data['description_long']
            place.lng = float(coordinates['lng'])
            place.lat = float(coordinates['lat'])
            place.save()

        place.images.all().delete()

        for position, raw_image_url in enumerate(place_data.get('imgs', []), start=1):
            image_url = urljoin(json_url, raw_image_url)
            try:
                image_content = download_image(image_url)
            except requests.RequestException as error:
                raise CommandError(f'Не удалось скачать картинку {image_url}: {error}')

            filename = get_filename_from_url(image_url)
            image_file = ContentFile(image_content, name=filename)
            place_image = PlaceImage(place=place, position=position)
            place_image.image.save(filename, image_file, save=True)

        self.stdout.write(self.style.SUCCESS(f'Загружено место: {place.title}'))
