# Generated by Django 5.1.1 on 2024-12-15 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tduscmap', '0006_alter_car_marque'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='background',
            field=models.CharField(default='default_background', max_length=50),
        ),
    ]
