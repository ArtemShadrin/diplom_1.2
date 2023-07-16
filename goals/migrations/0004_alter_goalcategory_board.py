# Generated by Django 4.2.3 on 2023-07-25 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("goals", "0003_creae_new_objects"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goalcategory",
            name="board",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="categories",
                to="goals.board",
                verbose_name="Доска",
            ),
        ),
    ]
