# Generated by Django 3.0.2 on 2020-04-03 15:02

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_auto_20200224_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url='/software/', location='/opt/services/ufts/software/'), upload_to=''),
        ),
    ]
