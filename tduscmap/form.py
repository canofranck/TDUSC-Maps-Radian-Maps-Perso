from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Reglage, Car, ConfigurationReglage


class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription pour les utilisateurs.

    Ce formulaire est utilisé pour permettre aux utilisateurs de s'inscrire
    en fournissant un nom d'utilisateur et un mot de passe.

    Attributes:
        model (User): Le modèle d'utilisateur à utiliser.
        fields : Le champs à inclure dans le formulaire.

    """

    class Meta(UserCreationForm.Meta):
        """
        Métadonnées du formulaire d'inscription.

        Les métadonnées spécifient le modèle à utiliser et les champs
        à inclure.

        Attributes:
            model (User): Le modèle d'utilisateur à utiliser.
            fields : Le champs à inclure dans le formulaire.

        """

        model = get_user_model()
        fields = ("username",)


class ReglageForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 50}),
        label="Description détaillée",
        help_text="Veuillez entrer une description complète.",
    )

    class Meta:
        model = Reglage
        exclude = ("car", "user", "configurationreglage")


class ModeleSelectionForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["id"]
        widgets = {
            "id": forms.HiddenInput(),  # On cache le champ 'id' car il sera rempli dynamiquement
        }


class ChoixModeleForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["modele"]


class ConfigurationReglageUserForm(
    forms.ModelForm,
):

    class Meta:
        model = ConfigurationReglage
        exclude = ("car",)

        labels = {
            "troisieme_vitesse_min": "troisieme_vitesse_min ( si pas présente entrer 9999)",
            "troisieme_vitesse_max": "troisieme_vitesse_max ( si pas présente entrer 9999)",
            "quatrieme_vitesse_min": "quatrieme_vitesse_min ( si pas présente entrer 9999)",
            "quatrieme_vitesse_max": "quatrieme_vitesse_max ( si pas présente entrer 9999)",
            "cinquieme_vitesse_min": "cinquieme_vitesse_min ( si pas présente entrer 9999)",
            "cinquieme_vitesse_max": "cinquieme_vitesse_max ( si pas présente entrer 9999)",
            "sixieme_vitesse_min": "sixieme_vitesse_min ( si pas présente entrer 9999)",
            "sixieme_vitesse_max": "sixieme_vitesse_max ( si pas présente entrer 9999)",
            "septieme_vitesse_min": "septieme_vitesse_min ( si pas présente entrer 9999)",
            "septieme_vitesse_max": "septieme_vitesse_max ( si pas présente entrer 9999)",
            "huitieme_vitesse_min": "huitieme_vitesse_min ( si pas présente entrer 9999)",
            "huitieme_vitesse_max": "huitieme_vitesse_max ( si pas présente entrer 9999)",
            "acceleration_avant_min": "acceleration_avant_min ( entre 0 et 100) si pas présente entrer 9999",
            "acceleration_avant_max": "acceleration_avant_max ( entre 0 et 100) si pas présente entrer 9999",
            "deceleration_avant_min": "deceleration_avant_min ( entre 0 et 100) si pas présente entrer 9999",
            "deceleration_avant_max": "deceleration_avant_max ( entre 0 et 100) si pas présente entrer 9999",
            "freinage_avant_min": "freinage_avant_min ( entre 0 et 100) si pas présente entrer 9999",
            "freinage_avant_max": "freinage_avant_max ( entre 0 et 100) si pas présente entrer 9999",
            "distribution_puissance_avant_arriere_min": "distribution_puissance_avant_arriere_min ( entre 0 et 100) si pas présente entrer 9999",
            "distribution_puissance_avant_arriere_max": "distribution_puissance_avant_arriere_max ( entre 0 et 100) si pas présente entrer 9999",
            "acceleration_centrale_min": "acceleration_centrale_min ( entre 0 et 100) si pas présente entrer 9999",
            "acceleration_centrale_max": "acceleration_centrale_max ( entre 0 et 100) si pas présente entrer 9999",
            "deceleration_centrale_min": "deceleration_centrale_min ( entre 0 et 100) si pas présente entrer 9999",
            "deceleration_centrale_max": "deceleration_centrale_max ( entre 0 et 100) si pas présente entrer 9999",
            "freinage_centrale_min": "freinage_centrale_min ( entre 0 et 100) si pas présente entrer 9999",
            "freinage_centrale_max": "freinage_centrale_max ( entre 0 et 100) si pas présente entrer 9999",
            "pression_pneus_arriere_min": "pression_pneus_arriere_min ( entre 2 et 6) si pas présente entrer 9999",
            "pression_pneus_arriere_max": "pression_pneus_arriere_max ( entre 2 et 6) si pas présente entrer 9999",
            "pression_pneus_avant_min": "pression_pneus_avant_min ( entre 2 et 6) si pas présente entrer 9999",
            "pression_pneus_avant_max": "pression_pneus_avant_max ( entre 2 et 6) si pas présente entrer 9999",
        }

        def save(self, commit=True):
            instance = super().save(commit=False)

            if instance.car:
                configuration, created = (
                    ConfigurationReglage.objects.get_or_create(
                        car=instance.car
                    )
                )
                instance.configurationreglage = configuration
            else:
                raise forms.ValidationError(
                    "La voiture doit être sélectionnée."
                )

            if commit:
                instance.save()
            return instance
