from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm  # Import correct du formulaire


def signup_page(request):
    """Affiche et traite la page d'inscription des utilisateurs."""
    
    form = CustomUserCreationForm()  # Utilisation du bon formulaire
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Utilisation du formulaire pour les données POST
        if form.is_valid():
            user = form.save()
            # auto-login de l'utilisateur après création du compte
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    
    return render(
        request, "authentication/signup.html", context={"form": form}
    )


def logout_user(request):
    """Déconnecte l'utilisateur actuellement authentifié.

    Cette vue permet à l'utilisateur actuellement authentifié de se déconnecter
    en invalidant sa session d'authentification. Une fois déconnecté,
    l'utilisateur est redirigé vers la page de connexion.

    Args:
        request (HttpRequest): L'objet HttpRequest représente la requête HTTP.

    Returns:
        HttpResponseRedirect: Une redirection HTTP vers la page de connexion
        après la déconnexion de l'utilisateur.

    """
    logout(request)
    return redirect("login")

