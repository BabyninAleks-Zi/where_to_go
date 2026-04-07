from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_alter_placeimage_options_placeimage_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
    ]
