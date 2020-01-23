# Generated by Django 2.1.1 on 2019-08-30 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('category', models.CharField(default='', max_length=100)),
                ('document', models.FileField(upload_to='support/documentation')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_type', models.CharField(default='', max_length=100)),
                ('prod_family', models.CharField(default='', max_length=100)),
                ('prod_model', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'products',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentation.Products'),
        ),
    ]
