# Generated by Django 2.0.5 on 2018-07-11 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_auto_20180711_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='geojson',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='gaupalika',
            name='geojson',
            field=models.TextField(blank=True),
        ),
    ]