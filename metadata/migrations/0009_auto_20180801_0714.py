# Generated by Django 2.0.5 on 2018-08-01 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20180717_0445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geosite',
            old_name='probability_of_risk',
            new_name='risk_probability',
        ),
        migrations.RenameField(
            model_name='geosite',
            old_name='risk_rating',
            new_name='risk_score',
        ),
    ]
