# Generated by Django 5.0.7 on 2024-09-04 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Favorites",
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
                ("name", models.CharField(max_length=100)),
                ("rank", models.IntegerField()),
                ("comments", models.CharField(blank=True, max_length=250, null=True)),
                ("link", models.URLField(blank=True, null=True, unique=True)),
                ("category", models.CharField(max_length=50)),
                ("added_by_suggestion", models.BooleanField(default=0)),
                ("date_added", models.DateField(auto_now_add=True)),
            ],
            options={
                "db_table": "favorites",
            },
        ),
    ]
