# Generated by Django 2.0.5 on 2018-08-03 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0010_auto_20180803_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='geosite',
            name='ward',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='household',
            name='ward',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
