# Generated by Django 3.0.2 on 2020-04-07 17:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jsa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsa',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
