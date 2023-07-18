# -*- coding: utf-8 -*-
from django.db import models, migrations
import django_kmatch.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('k', django_kmatch.fields.KField()),
            ],
        ),
        migrations.CreateModel(
            name='NullTrueModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('k', django_kmatch.fields.KField(null=True)),
            ],
        ),
    ]
