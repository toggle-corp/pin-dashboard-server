# Generated by Django 2.0.5 on 2018-07-11 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_gaupalika_district'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geosite',
            old_name='high_risk_ok',
            new_name='high_risk_of',
        ),
    ]
