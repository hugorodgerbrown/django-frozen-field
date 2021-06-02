# Generated by Django 3.2.4 on 2021-06-02 21:19

import django.db.models.deletion
from django.db import migrations, models

import frozen_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FlatModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("field_int", models.IntegerField()),
                ("field_str", models.TextField()),
                ("field_bool", models.BooleanField()),
                ("field_date", models.DateField()),
                ("field_datetime", models.DateTimeField()),
                ("field_decimal", models.DecimalField(decimal_places=3, max_digits=8)),
                ("field_float", models.FloatField()),
                ("field_uuid", models.UUIDField()),
                ("field_json", models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="NestedModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "frozen",
                    frozen_field.fields.FrozenObjectField(
                        "app_model",
                        blank=True,
                        exclude=[],
                        include=[],
                        null=True,
                        select_related=[],
                    ),
                ),
                (
                    "fresh",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tests.flatmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeepNestedModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "frozen",
                    frozen_field.fields.FrozenObjectField(
                        "app_model",
                        blank=True,
                        exclude=[],
                        include=["id", "frozen"],
                        null=True,
                        select_related=[],
                    ),
                ),
                (
                    "fresh",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tests.nestedmodel",
                    ),
                ),
            ],
        ),
    ]
