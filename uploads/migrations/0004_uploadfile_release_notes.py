# Generated by Django 3.0.2 on 2020-04-03 19:02

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_auto_20200403_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='release_notes',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/software/', location='/opt/services/ufts/software/'), upload_to=''),
        ),
    ]
