# Generated by Django 3.0 on 2019-12-13 00:17

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricefinderapp', '0004_auto_20191213_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprice',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]