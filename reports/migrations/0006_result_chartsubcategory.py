# Generated by Django 2.1.7 on 2019-05-04 08:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20190504_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='chartSubCategory',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]