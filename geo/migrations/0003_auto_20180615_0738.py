# Generated by Django 2.0.5 on 2018-06-15 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_map_default_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='maps'),
        ),
    ]
