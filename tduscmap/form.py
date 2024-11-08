from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Reglage, Car


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
    class Meta:
        model = Reglage
        exclude = ('car', 'user', 'configurationreglage')
        
class ModeleSelectionForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["id"]  # On sélectionne uniquement le champ 'id'
        widgets = {
            "id": forms.HiddenInput(),  # On cache le champ 'id' car il sera rempli dynamiquement
        }


class ChoixModeleForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['modele']


