from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from .models import Favorite, Car, Reglage, ConfigurationReglage, Like
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from tduscmap.form import ConfigurationReglageUserForm, ReglageForm, ChoixModeleForm
from django.db.models import Count, Q, Prefetch
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    return render(
        request,
        "home.html",
    )


@login_required
def ajouter_favori(request):
    if request.method == "POST":
        try:
            # Convertir les données JSON en dictionnaire Python
            data = json.loads(request.body)
            lat = data.get("lat")
            lng = data.get("lng")
            description = data.get("description")
            # Créer et sauvegarder un nouveau favori dans la base de données
            Favorite.objects.create(
                user=request.user, lat=lat, lng=lng, description=description
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method"}
        )


# Supprimer un favori
@login_required
def supprimer_favori(request, favori_id):
    favori = Favorite.objects.get(id=favori_id, user=request.user)
    favori.delete()
    return redirect("afficher_favoris")


# Afficher les favoris de l'utilisateur connecté
@login_required
def afficher_favoris(request):
    favoris = Favorite.objects.filter(user=request.user)
    return render(request, "afficher_favoris.html", {"favoris": favoris})


@login_required
def mymaps(request):
    return render(request, "tduscmap/mymaps.html")


@login_required
def get_favorites(request):
    """Récupérer les favoris de l'utilisateur connecté."""
    user = request.user
    # Filtrer les favoris par utilisateur
    favs = Favorite.objects.filter(user=user)
    favorites_list = [
        {
            "id": fav.id,
            "lat": fav.lat,
            "lng": fav.lng,
            "description": fav.description,
        }
        for fav in favs
    ]
    return JsonResponse(favorites_list, safe=False)


@login_required
@require_http_methods(["DELETE"])
def delete_favorite(request, favorite_id):
    try:
        favorite = Favorite.objects.get(id=favorite_id)
        favorite.delete()
        return JsonResponse({"success": True})
    except Favorite.DoesNotExist:
        return JsonResponse({"success": False, "error": "Favori introuvable"})


@login_required
def get_friends(request):
    """Récupérer la liste des amis de l'utilisateur."""
    user = request.user
    friends = user.friends.all()
    friend_list = [
        {"id": friend.id, "username": friend.username} for friend in friends
    ]
    return JsonResponse(friend_list, safe=False)


@login_required
def get_friend_favorites(request, friend_id):
    if request.method == "GET":
        try:
            friend = CustomUser.objects.get(id=friend_id)
            favorites = Favorite.objects.filter(user=friend)
            favorites_data = [
                {
                    "id": fav.id,
                    "lat": fav.lat,
                    "lng": fav.lng,
                    "description": fav.description,
                }
                for fav in favorites
            ]
            return JsonResponse(favorites_data, safe=False)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "Ami non trouvé"}, status=404)


@login_required
def search_friends(request):
    search_query = request.GET.get("search", "")
    if search_query:
        users = CustomUser.objects.filter(username__icontains=search_query)
    else:
        users = CustomUser.objects.none()

    results = [{"username": user.username, "id": user.id} for user in users]
    return JsonResponse({"users": results})


@login_required
@csrf_exempt
def add_friend(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            friend_id = data.get("friend_id")  # L'ID de l'ami à ajouter

            user = CustomUser.objects.get(id=user_id)
            friend = CustomUser.objects.get(id=friend_id)

            # Vérifie si l'utilisateur n'essaie pas de s'ajouter lui-même
            if user.id == friend.id:
                return JsonResponse(
                    {"success": False, "message": "Action non autorisée"}
                )

            # Ajoute l'ami
            user.friends.add(friend)

            return JsonResponse(
                {"success": True, "message": "Ami ajouté avec succès !"}
            )
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Utilisateur non trouvé"}
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Erreur de décodage JSON"}
            )
    else:
        return JsonResponse(
            {"success": False, "message": "Requête non autorisée"}
        )


@login_required
def car_price_choice(request):
    cars = Car.objects.all()
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        car_selected = Car.objects.get(pk=car_id)
        # Préparer les données pour Chart.js
        prices = car_selected.historique_prix.all().order_by("date")
        dates = [price.date.strftime("%Y-%m-%d") for price in prices]
        price_values = [price.prix for price in prices]
        # Ajouter le prix initial au début de la liste des prix
        price_values.insert(0, car_selected.prix_initial)
        # Pour ajouter une étiquette pour le prix initial
        dates.insert(0, "Prix initial")
        context = {
            "cars": cars,
            "car_selected": car_selected,
            "dates": dates,
            "price_values": price_values,
        }
    else:
        car_selected = None
        context = {"cars": cars, "car_selected": car_selected}

    return render(request, "tduscmap/car_list.html", context)


@login_required
def car_prices_view(request):
    cars = Car.objects.prefetch_related("historique_prix").all()

    prices_data = {}
    for car in cars:
        prices_data[car] = []
        for price in car.historique_prix.all():
            prices_data[car].append(
                {
                    "date": price.date,
                    "prix": price.prix if price.prix is not None else None,
                }
            )

    context = {
        "prices_data": prices_data,
    }
    return render(request, "tduscmap/car_prices.html", context)


@login_required
def liste_reglages(request):
    reglages = (
        Reglage.objects.all()
        .annotate(like_count=Count("likes"))
        .prefetch_related(Prefetch("car"))
    )

    # Construire la requête en fonction des critères de recherche
    query = Q()
    marque = request.GET.get("marque")
    modele = request.GET.get("modele")
    if marque:
        query &= Q(car__marque__icontains=marque)
    if modele:
        query &= Q(car__modele__icontains=modele)
    reglages = reglages.filter(query)

    # Trier les résultats
    order_by = request.GET.get(
        "order_by", "-like_count"
    )  # Permet de trier par d'autres champs
    reglages = reglages.order_by(order_by)

    # Récupérer les marques et modèles distincts à partir du prefetch
    marques = Car.objects.values_list("marque", flat=True).distinct()
    modeles = Car.objects.values_list("modele", flat=True).distinct()

    # Pagination
    limit = int(request.GET.get("limit", 5))  # Valeur par défaut 10
    paginator = Paginator(reglages, limit)  # 25 résultats par page
    page = request.GET.get("page")
    try:
        reglages = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, renvoyer la première page
        reglages = paginator.page(1)
    except EmptyPage:
        # Si la page est hors limites (trop élevée), renvoyer la dernière page
        reglages = paginator.page(paginator.num_pages)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tduscmap/liste_reglages.html",
        {
            "reglages": page_obj,
            "marques": marques,
            "modeles": modeles,
            "paginator": paginator,
            "page": page_number,
            "limit": limit,
        },
    )


@login_required
def detail_reglage(request, pk):
    reglage = Reglage.objects.get(pk=pk)
    nombre_likes = reglage.likes.count()
    if request.method == "POST":
        # Vérifier si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Vérifier si l'utilisateur a déjà liké ce réglage
            if not reglage.likes.filter(user=request.user).exists():
                Like.objects.create(reglage=reglage, user=request.user)
            # Rediriger vers la même page pour afficher le nouveau nombre de likes
            return redirect("detail_reglage", pk=reglage.pk)
    return render(
        request,
        "tduscmap/detail_reglage.html",
        {"reglage": reglage, "nombre_likes": nombre_likes},
    )


@login_required
def get_configuration(request, car_id):
    try:
        reglage = Reglage.objects.get(car_id=car_id)
        configuration = ConfigurationReglage.objects.get(car_id=car_id)
        return render(
            request,
            "ton_template.html",
            {
                "reglage": reglage,
                "configurationreglage": configuration,
            },
        )
    except ConfigurationReglage.DoesNotExist:
        return JsonResponse({"error": "Configuration non trouvée"}, status=404)


@login_required
def choix_modele(request):
    if request.method == "POST":
        form = ChoixModeleForm(request.POST)
        if form.is_valid():
            modele = form.cleaned_data["modele"]
            # Récupérer la voiture en fonction du modèle (vous pouvez ajouter d'autres critères si nécessaire)
            car = Car.objects.get(modele=modele)
            return redirect("saisie_reglage", car_id=car.id)
    else:
        form = ChoixModeleForm()
        # Récupérer tous les modèles de voitures distincts
        modeles = Car.objects.values_list("modele", flat=True).distinct()
        return render(
            request,
            "tduscmap/template_principal.html",
            {"form": form, "modeles": modeles},
        )


def saisie_reglage(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        configuration = ConfigurationReglage.objects.get(car=car)
        reglage = ConfigurationReglage.objects.get(car_id=car_id)
        initial_data = {
            "car": car,
            "user": request.user,
            "configurationreglage": configuration,
        }
    except (Car.DoesNotExist, ConfigurationReglage.DoesNotExist):
        return redirect("user_configurationreglage", car_id)
    if request.method == "POST":
        form = ReglageForm(request.POST)
        print(request.POST)
        if form.is_valid():
            # Comme les champs exclus ne sont pas dans le formulaire,
            # on les ajoute manuellement à l'instance avant de l'enregistrer
            reglage = form.save(commit=False)
            reglage.car = car
            reglage.user = request.user
            reglage.configurationreglage = configuration
            reglage.save()
            return redirect("liste_reglages")
    else:
        form = ReglageForm(initial=initial_data)

    return render(
        request,
        "tduscmap/reglage_form.html",
        {"form": form, "car": car, "reglage": reglage},
    )


def user_configurationreglage(request, car_id):  # Add message argument
    if request.method == 'POST':
        form = ConfigurationReglageUserForm(request.POST)
        if form.is_valid():
            form.instance.car_id = car_id
            form.save()
            # Rediriger vers une page de succès
            return redirect('choix_modele')
            
        else:
            # Afficher le formulaire avec les erreurs
            form = ConfigurationReglageUserForm()
            form.instance.car_id = car_id
            return render(request, 'tduscmap/user_configurationreglage.html', {'form': form})
    else:
        form = ConfigurationReglageUserForm()
        form.instance.car_id = car_id
        return render(request, 'tduscmap/user_configurationreglage.html', {'form': form})


def modifier_reglages(request, id):

    reglage = Reglage.objects.get(id=id)
    configuration = reglage.configurationreglage
    if request.method == 'POST':
        form = ReglageForm(request.POST, instance=reglage)
        if form.is_valid():
            reglage.save()
            return redirect('liste_reglages')  
    else:
        form = ReglageForm(instance=reglage)
    return render(
        request,
        "tduscmap/modifier_reglage_form.html",
        {"form": form,  "reglage": reglage, "configuration": configuration,}
    )

def mes_reglages(request):
    # Récupérer les réglages de l'utilisateur connecté
    reglages = Reglage.objects.filter(user=request.user)
    reglages = reglages.annotate(like_count=Count('likes'))
    # Pagination
      # Valeur par défaut 10
    paginator = Paginator(reglages, 10)  # 25 résultats par page
    page = request.GET.get("page")
    try:
        reglages = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, renvoyer la première page
        reglages = paginator.page(1)
    except EmptyPage:
        # Si la page est hors limites (trop élevée), renvoyer la dernière page
        reglages = paginator.page(paginator.num_pages)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'tduscmap/mes_reglages.html', {'reglages': page_obj, "paginator": paginator,
                  "page": page_number, })


def supprimer_reglage(request, id):
    """
    Vue pour supprimer un réglage par son identifiant.

    Args:
        request: La requête HTTP.
        reglage_id: L'identifiant du réglage à supprimer.

    Returns:
        Une réponse HTTP redirigeant vers la liste des réglages avec un message de confirmation.
    """

    reglage = Reglage.objects.get(id=id)
    reglage.delete()
    return redirect('liste_reglages')