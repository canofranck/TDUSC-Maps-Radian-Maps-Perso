# Generated by Django 5.1.1 on 2024-12-15 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tduscmap', '0005_alter_car_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='marque',
            field=models.CharField(choices=[('Abarth', 'Abarth'), ('AC', 'AC'), ('Alfa Romeo', 'Alfa Romeo'), ('Alpine', 'Alpine'), ('Apollo Automobil', 'Apollo Automobil'), ('Aston Martin', 'Aston Martin'), ('Audi', 'Audi'), ('Bentley', 'Bentley'), ('BMW', 'BMW'), ('Bugatti', 'Bugatti'), ('Caterham', 'Caterham'), ('Chevrolet', 'Chevrolet'), ('Citroën', 'Citroën'), ('Dodge', 'Dodge'), ('Ferrari', 'Ferrari'), ('Ford', 'Ford'), ('Jaguar', 'Jaguar'), ('Koenigsegg', 'Koenigsegg'), ('Lamborghini', 'Lamborghini'), ('Land Rover', 'Land Rover'), ('Lancia', 'Lancia'), ('Lotus', 'Lotus'), ('Maserati', 'Maserati'), ('McLaren', 'McLaren'), ('MercedesAMG', 'MercedesAMG'), ('MercedesBenz', 'MercedesBenz'), ('Mini', 'Mini'), ('Nissan', 'Nissan'), ('Pininfarina', 'Pininfarina'), ('Porsche', 'Porsche'), ('Shelby', 'Shelby'), ('Sientero', 'Sientero'), ('WMotors', 'WMotors'), ('Volkswagen', 'Volkswagen'), ('W Motors', 'W Motors')], max_length=50),
        ),
    ]
