# Generated by Django 3.0.5 on 2020-04-19 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricefinderapp', '0005_auto_20191213_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userproduct',
            options={'ordering': ['-id']},
        ),
    ]
