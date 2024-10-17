# Generated by Django 5.1.2 on 2024-10-17 17:17

import django.db.models.deletion
from django.db import migrations, models


def populate_cultures(apps, *args, **kwargs):
    Culture = apps.get_model('agro', 'Culture')

    # if i've a long list i don't use this way, maybe i would use a CSV for load on create database
    # and i would use a bulk create
    for name in ['Soja', 'Milho', 'Algodão', 'Café', 'Cana de Açucar', 'Manga', 'Limão', 'Banana']:
        culture = Culture(name=name)
        culture.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Culture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Cultura")),
            ],
            options={
                "db_table": "culture",
            },
        ),
        migrations.CreateModel(
            name="Farmer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Nome")),
                (
                    "document",
                    models.CharField(
                        max_length=14, unique=True, verbose_name="CPF/CNPJ"
                    ),
                ),
            ],
            options={
                "db_table": "farmer",
            },
        ),
        migrations.CreateModel(
            name="Farm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Nome")),
                (
                    "total_area",
                    models.DecimalField(
                        decimal_places=2, max_digits=11, verbose_name="Area total"
                    ),
                ),
                (
                    "vegetal_area",
                    models.DecimalField(
                        decimal_places=2, max_digits=11, verbose_name="Area Vegetação"
                    ),
                ),
                (
                    "available_area",
                    models.DecimalField(
                        decimal_places=2, max_digits=11, verbose_name="Area agricutável"
                    ),
                ),
                ("city", models.CharField(max_length=100, verbose_name="Cidade")),
                ("state", models.CharField(max_length=2, verbose_name="Estado")),
                (
                    "cultures",
                    models.ManyToManyField(related_name="farms", to="agro.culture"),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="farm",
                        to="agro.farmer",
                    ),
                ),
            ],
            options={
                "db_table": "farm",
            },
        ),

        migrations.RunPython(populate_cultures)
    ]
