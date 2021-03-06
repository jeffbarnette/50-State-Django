# Generated by Django 3.1.6 on 2021-02-13 15:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capital',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True,
                                     primary_key=True,
                                     serialize=False,
                                     verbose_name='ID')
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^[a-zA-Z]*$',
                                'Only alpha characters are allowed.'
                            )
                        ]
                    )
                ),
            ],
            options={
                'verbose_name': 'capital',
                'verbose_name_plural': 'capitals',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^[a-zA-Z]*$',
                                'Only alpha characters are allowed.'
                            )
                        ]
                    )
                ),
                (
                    'abbr',
                    models.CharField(
                        max_length=2,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^[a-zA-Z]*$',
                                'Only alpha characters are allowed.'
                            )
                        ],
                        verbose_name='Abbreviation'
                    )
                ),
                (
                    'capital',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='location.capital'
                    )
                ),
            ],
            options={
                'verbose_name': 'state',
                'verbose_name_plural': 'states',
                'ordering': ['name'],
            },
        ),
    ]
