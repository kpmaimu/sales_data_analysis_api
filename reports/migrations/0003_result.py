# Generated by Django 2.1.7 on 2019-05-04 05:54

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('upload', '0003_dataset_isdefault'),
        ('reports', '0002_delete_datasetdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', django.contrib.postgres.fields.jsonb.JSONField()),
                ('sentiment', django.contrib.postgres.fields.jsonb.JSONField()),
                ('category', django.contrib.postgres.fields.jsonb.JSONField()),
                ('datasetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.DataSet')),
            ],
        ),
    ]
