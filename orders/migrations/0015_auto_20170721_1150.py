# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20170709_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinbasket',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
        migrations.AlterField(
            model_name='productinorder',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
    ]
