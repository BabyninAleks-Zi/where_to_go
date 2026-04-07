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
            raw_place_data = get_json(json_url)
        except requests.RequestException as error:
            raise CommandError(f'Не удалось скачать JSON: {error}')

        coordinates = raw_place_data['coordinates']

        place_defaults = {
            'short_description': raw_place_data['description_short'],
            'long_description': raw_place_data['description_long'],
            'lng': float(coordinates['lng']),
            'lat': float(coordinates['lat']),
        }

        place, _ = Place.objects.update_or_create(
            title=raw_place_data['title'],
            defaults=place_defaults,
        )

        place.images.all().delete()

        for position, raw_image_url in enumerate(raw_place_data.get('imgs', []), start=1):
            image_url = urljoin(json_url, raw_image_url)
            try:
                image_content = download_image(image_url)
            except requests.RequestException as error:
                raise CommandError(f'Не удалось скачать картинку {image_url}: {error}')

            filename = get_filename_from_url(image_url)
            PlaceImage.objects.create(
                place=place,
                position=position,
                image=ContentFile(image_content, name=filename),
            )

        self.stdout.write(self.style.SUCCESS(f'Загружено место: {place.title}'))
