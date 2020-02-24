# Generated by Django 3.0.2 on 2020-02-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jsa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayName', models.CharField(blank=True, max_length=200)),
                ('document', models.FileField(upload_to='support/jsas')),
                ('description', models.TextField()),
            ],
        ),
    ]
