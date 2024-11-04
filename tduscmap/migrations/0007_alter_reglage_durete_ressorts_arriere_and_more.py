# Generated by Django 5.1.1 on 2024-11-02 21:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tduscmap', '0006_alter_configurationreglage_taille_suspension_arriere_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reglage',
            name='durete_ressorts_arriere',
            field=models.DecimalField(decimal_places=0, max_digits=3, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='reglage',
            name='durete_ressorts_avant',
            field=models.DecimalField(decimal_places=0, max_digits=3, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)]),
        ),
    ]