# Generated by Django 3.0.14 on 2022-07-15 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220702_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile/user-default.png', null=True, upload_to='profile/'),
        ),
    ]