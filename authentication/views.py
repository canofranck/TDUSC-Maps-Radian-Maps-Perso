from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm  # Import correct du formulaire
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage ,send_mail
from .tokens import account_activation_token
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives


def signup_page(request):
    """Affiche et traite la page d'inscription des utilisateurs avec activation par email."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save immediately
            user.is_active = False  # Deactivate the user
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activation de votre compte'
            message = render_to_string("authentication/acc_active_email.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            try:
                email = EmailMultiAlternatives(
                    mail_subject,
                    message,  # Contenu texte brut
                    settings.DEFAULT_FROM_EMAIL,
                    [to_email],
                )
                email.attach_alternative(message, "text/html")  # Contenu HTML
                email.send(fail_silently=False)  # Important pour lever les erreurs
                # print("Email envoyé avec succès !")
                # Envoi de l'email de notification à l'administrateur
                admin_mail_subject = 'Nouvel utilisateur inscrit'
                admin_message = f"Un nouvel utilisateur vient de s'inscrire :\n\nNom d'utilisateur : {user.username}\nEmail : {user.email}"
                admin_email = EmailMultiAlternatives(
                    admin_mail_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],  # Remplace par ton email
                )
                admin_email.send(fail_silently=False)
                # print("Email de notification envoyé à l'administrateur.")
                return render(request, "authentication/confirm_email.html")  # Confirmation page
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email d'activation : {e}")
                return render(request, "authentication/signup.html", context={"form": form})

        else:
            # Gestion des erreurs de formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Erreur dans le champ {field}: {error}")
            return render(request, "authentication/signup.html", context={"form": form})

    else:
        form = CustomUserCreationForm()
    return render(request, "authentication/signup.html", context={"form": form})

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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user) # Connecter l'utilisateur après l'activation
        return redirect(settings.LOGIN_REDIRECT_URL)  # Redirection après activation
    else:
        return render(request, 'authentication/activation_failed.html')