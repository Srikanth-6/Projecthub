# Generated by Django 3.0.14 on 2022-06-30 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20220628_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='featured_images',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
