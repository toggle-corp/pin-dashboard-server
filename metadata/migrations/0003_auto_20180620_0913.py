# Generated by Django 2.0.5 on 2018-06-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0002_auto_20180620_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='application',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='household',
            name='eligibility',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='household',
            name='result',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
