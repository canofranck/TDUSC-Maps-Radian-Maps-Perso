# Generated by Django 5.1.1 on 2024-11-27 08:36

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(choices=[('Abarth', 'Abarth'), ('AC', 'AC'), ('Alfa Romeo', 'Alfa Romeo'), ('Alpine', 'Alpine'), ('Apollo Automobil', 'Apollo Automobil'), ('Aston Martin', 'Aston Martin'), ('Audi', 'Audi'), ('Bentley', 'Bentley'), ('BMW', 'BMW'), ('Bugatti', 'Bugatti'), ('Caterham', 'Caterham'), ('Chevrolet', 'Chevrolet'), ('Citroën', 'Citroën'), ('Dodge', 'Dodge'), ('Ferrari', 'Ferrari'), ('Ford', 'Ford'), ('Jaguar', 'Jaguar'), ('Koenigsegg', 'Koenigsegg'), ('Lamborghini', 'Lamborghini'), ('Land Rover', 'Land Rover'), ('Lancia', 'Lancia'), ('Lotus', 'Lotus'), ('Maserati', 'Maserati'), ('McLaren', 'McLaren'), ('MercedesAMG', 'MercedesAMG'), ('MercedesBenz', 'MercedesBenz'), ('Mini', 'Mini'), ('Nissan', 'Nissan'), ('Porsche', 'Porsche'), ('Shelby', 'Shelby'), ('Sientero', 'Sientero'), ('WMotors', 'WMotors'), ('Volkswagen', 'Volkswagen'), ('W Motors', 'W Motors')], max_length=50)),
                ('modele', models.CharField(max_length=50)),
                ('annee', models.PositiveIntegerField(null=True)),
                ('transmission', models.CharField(choices=[('RWD', 'RWD'), ('FWD', 'FWD'), ('4WD', '4WD')], max_length=3, null=True)),
                ('ip', models.PositiveIntegerField(null=True)),
                ('categorie', models.CharField(choices=[('A', 'Catégorie A'), ('B', 'Catégorie B'), ('C', 'Catégorie C'), ('D', 'Catégorie D'), ('E', 'Catégorie E'), ('F', 'Catégorie F'), ('G', 'Catégorie G'), ('H', 'Catégorie H')], max_length=1, null=True)),
                ('rarete', models.CharField(blank=True, choices=[('légendaire', 'Légendaire'), ('épique', 'Épique'), ('rare', 'Rare'), ('commun', 'Commun'), ('peu commun', 'Peu commun'), (None, 'Aucune')], max_length=10, null=True)),
                ('prix_initial', models.PositiveIntegerField(null=True)),
                ('nb_vitesse', models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='CarPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix', models.PositiveIntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historique_prix', to='tduscmap.car')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reglage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='exemple : pour circuit court avec de nombreux virage')),
                ('pieces', models.CharField(choices=[('Serie', 'Serie'), ('Performance', 'Perfomance'), ('Sport', 'Sport'), ('Super Sport', 'Super Sport'), ('Course', 'Course')], max_length=15)),
                ('rapport_final', models.DecimalField(decimal_places=2, max_digits=5)),
                ('premiere_vitesse', models.DecimalField(decimal_places=2, max_digits=4)),
                ('deuxieme_vitesse', models.DecimalField(decimal_places=2, max_digits=4)),
                ('troisieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('quatrieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('cinquieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('sixieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('septieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('huitieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('neuvieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('dixieme_vitesse', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('appui_aerodynamique_avant', models.DecimalField(decimal_places=2, max_digits=3)),
                ('appui_aerodynamique_arriere', models.DecimalField(decimal_places=2, max_digits=3)),
                ('taille_suspension_arriere', models.DecimalField(decimal_places=2, max_digits=6)),
                ('taille_suspension_avant', models.DecimalField(decimal_places=2, max_digits=6)),
                ('durete_ressorts_arriere', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)])),
                ('durete_ressorts_avant', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)])),
                ('compression_amortisseurs_avant', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)])),
                ('compression_amortisseurs_arriere', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)])),
                ('decompression_amortisseurs_avant', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)])),
                ('decompression_amortisseurs_arriere', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(120)])),
                ('acceleration_avant', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('deceleration_avant', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('freinage_avant', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('distribution_puissance_avant_arriere', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('acceleration_centrale', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('deceleration_centrale', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('freinage_central', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('acceleration_arriere', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('deceleration_arriere', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('freinage_arriere', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('durete_barre_antiroulis_avant', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('durete_barre_antiroulis_arriere', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('angle_carrossage_arriere', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(-6), django.core.validators.MaxValueValidator(3)])),
                ('angle_carrossage_avant', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(-6), django.core.validators.MaxValueValidator(3)])),
                ('pression_pneus_arriere', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('pression_pneus_avant', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('repartiteur_freinage_avant', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('pression_freinage', models.IntegerField(validators=[django.core.validators.MinValueValidator(-1000), django.core.validators.MaxValueValidator(1000)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('background', models.CharField(default='default_background', max_length=50)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tduscmap.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trajet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Nom ou description du trajet', max_length=100)),
                ('depart_lat', models.FloatField(help_text='Coordonnée Y en pixels du point de départ')),
                ('depart_lng', models.FloatField(help_text='Coordonnée X en pixels du point de départ')),
                ('etapes', models.JSONField(help_text='Liste des points intermédiaires sous forme de coordonnées pixels')),
                ('arrivee_lat', models.FloatField(help_text="Coordonnée Y en pixels du point d'arrivée")),
                ('arrivee_lng', models.FloatField(help_text="Coordonnée X en pixels du point d'arrivée")),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trajets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reglage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='tduscmap.reglage')),
            ],
            options={
                'unique_together': {('reglage', 'user')},
            },
        ),
    ]
