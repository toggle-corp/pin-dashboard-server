# Generated by Django 2.0.5 on 2018-06-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='land_size',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
