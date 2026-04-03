from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Краткое описание')
    description_long = models.TextField('Полное описание')
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место',
    )
    image = models.ImageField('Картинка', upload_to='places_images/')
    position = models.PositiveSmallIntegerField('Позиция', default=0, db_index=True)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return str(self.place)
