# Generated by Django 3.0.14 on 2022-07-16 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20220715_1208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]