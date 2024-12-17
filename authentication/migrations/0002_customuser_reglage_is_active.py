# Generated by Django 5.1.1 on 2024-12-17 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='reglage_is_active',
            field=models.BooleanField(default=False, help_text="Autorise l'utilisateur à enregistrer des réglages."),
        ),
    ]
