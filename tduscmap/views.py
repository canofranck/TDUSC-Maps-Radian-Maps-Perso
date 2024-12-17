import os
from pathlib import Path

from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from .models import Favorite, Car, Reglage,  Like, Trajet, Trajetibiza, Favoriteibiza
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from tduscmap.form import  ReglageForm, ChoixModeleForm
from django.db.models import Count, Q, Prefetch, Value, CharField
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import serializers
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required 

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

@login_required
def ajouter_favori_ibiza(request):
    if request.method == "POST":
        try:
            # Convertir les données JSON en dictionnaire Python
            data = json.loads(request.body)
            lat = data.get("lat")
            lng = data.get("lng")
            description = data.get("description")
            # Créer et sauvegarder un nouveau favori dans la base de données
            Favoriteibiza.objects.create(
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

@login_required
def supprimer_favori_ibiza(request, favori_id):
    favori = Favoriteibiza.objects.get(id=favori_id, user=request.user)
    favori.delete()
    return redirect("afficher_favoris")

# Afficher les favoris de l'utilisateur connecté
@login_required
def afficher_favoris(request):
    favoris = Favorite.objects.filter(user=request.user)
    return render(request, "afficher_favoris.html", {"favoris": favoris})

@login_required
def afficher_favoris_ibiza(request):
    favoris = Favoriteibiza.objects.filter(user=request.user)
    return render(request, "afficher_favoris_ibiza.html", {"favoris": favoris})

@login_required
def mymaps(request):
    return render(request, "tduscmap/mymaps.html")

@login_required
def mymaps_ibiza(request):
    return render(request, "tduscmap/mymaps_ibiza.html")

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
def get_favorites_ibiza(request):
    """Récupérer les favoris de l'utilisateur connecté."""
    user = request.user
    # Filtrer les favoris par utilisateur
    favs = Favoriteibiza.objects.filter(user=user)
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
@require_http_methods(["DELETE"])
def delete_favorite_ibiza(request, favorite_id):
    try:
        favorite = Favoriteibiza.objects.get(id=favorite_id)
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
def get_friend_favorites_ibiza(request, friend_id):
    if request.method == "GET":
        try:
            friend = CustomUser.objects.get(id=friend_id)
            favorites = Favoriteibiza.objects.filter(user=friend)
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
    # Récupérer les filtres de la requête
    piece = request.GET.get("piece", "").strip()  # Supprimer les espaces inutiles
    marque = request.GET.get("marque", "").strip()
    modele = request.GET.get("modele", "").strip()
    order_by = request.GET.get("order_by", "-created_at")
    limit = request.GET.get("limit", "10").strip()

    # Validation de la limite pour éviter les erreurs
    try:
        limit = int(limit) if limit.isdigit() else 10
    except ValueError:
        limit = 10

    # Obtenir la liste des pièces
    pieces = Reglage.objects.values_list('pieces', flat=True).distinct()

    # Construire la requête initiale
    reglages = Reglage.objects.all().annotate(like_count=Count("likes")).prefetch_related(Prefetch("car"))

    # Appliquer les filtres (seulement si des valeurs sont données)
    if piece:
        reglages = reglages.filter(pieces=piece)
    if marque:
        reglages = reglages.filter(car__marque=marque)
    if modele:
        reglages = reglages.filter(car__modele=modele)

    # Appliquer le tri
    if order_by.startswith("like_count"):
        reglages = reglages.order_by(order_by)
    else:
        reglages = reglages.order_by(order_by)

    # Pagination
    paginator = Paginator(reglages, limit)
    page = request.GET.get("page", 1)
    try:
        reglages = paginator.page(page)
    except PageNotAnInteger:
        reglages = paginator.page(1)
    except EmptyPage:
        reglages = paginator.page(paginator.num_pages)

    # Obtenir les marques et modèles distincts
    marques = Car.objects.values_list("marque", flat=True).distinct()
    modeles = Car.objects.values_list("modele", flat=True).distinct()

    # Rendu du template avec les données
    return render(request, "tduscmap/liste_reglages.html", {
        "reglages": reglages,
        "marques": marques,
        "modeles": modeles,
        "paginator": paginator,
        "page": page,
        "limit": limit,
        "pieces": pieces,
        "piece": piece,
        "marque": marque,
        "modele": modele,
        "order_by": order_by,
    })



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


# @login_required
# def get_configuration(request, car_id):
#     try:
#         reglage = Reglage.objects.get(car_id=car_id)
#         configuration = ConfigurationReglage.objects.get(car_id=car_id)
#         return render(
#             request,
#             "ton_template.html",
#             {
#                 "reglage": reglage,
#                 "configurationreglage": configuration,
#             },
#         )
#     except ConfigurationReglage.DoesNotExist:
#         return JsonResponse({"error": "Configuration non trouvée"}, status=404)


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
        modeles = Car.objects.annotate(
            modele_complet=Concat('marque', Value(' '), 'modele', output_field=CharField())
        ).order_by('modele_complet').values_list('marque', 'modele').distinct()
        
        return render(
            request,
            "tduscmap/template_principal.html",
            {"form": form, "modeles": modeles},
        )


def saisie_reglage(request, car_id):
    
    car = Car.objects.get(id=car_id)
    
    initial_data = {
            "car": car,
            "user": request.user,
            
        }
   
    if request.method == "POST":
        form = ReglageForm(request.POST)
        # (request.POST)
        if form.is_valid():
            # print(request.POST)
            # Comme les champs exclus ne sont pas dans le formulaire,
            # on les ajoute manuellement à l'instance avant de l'enregistrer
            reglage = form.save(commit=False)
            reglage.car = car
            reglage.user = request.user
            reglage.background = 'default_background'
            reglage.save()
            return redirect("liste_reglages")
        else:
            print(form.errors)  # For debugging purposes
    else:
        form = ReglageForm(initial=initial_data)
        # print(form.errors)
    return render(
        request,
        "tduscmap/reglage_form.html",
        {"form": form, "car": car, "errors": form.errors},
    )


# def user_configurationreglage(request, car_id):  # Add message argument
#     if request.method == 'POST':
#         form = ConfigurationReglageUserForm(request.POST)
#         if form.is_valid():
#             form.instance.car_id = car_id
#             form.save()
#             # Rediriger vers une page de succès
#             return redirect('choix_modele')
            
#         else:
#             # Afficher le formulaire avec les erreurs
#             form = ConfigurationReglageUserForm()
#             form.instance.car_id = car_id
#             return render(request, 'tduscmap/user_configurationreglage.html', {'form': form})
#     else:
#         form = ConfigurationReglageUserForm()
#         form.instance.car_id = car_id
#         return render(request, 'tduscmap/user_configurationreglage.html', {'form': form})


def modifier_reglages(request, id):

    reglage = Reglage.objects.get(id=id)
    # configuration = reglage.configurationreglage
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
        {"form": form,  "reglage": reglage}
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


@csrf_exempt
def save_trajet(request):
    if request.method == "POST":
        # print("Requête POST reçue")
        data = json.loads(request.body)
        user = request.user  # Utilisateur connecté

        # Vérifier si toutes les données sont présentes
        try:
            data = json.loads(request.body)
            nom = data["nom"]
            depart = data["depart"]
            etapes = data["etapes"]
            arrivee = data["arrivee"]
            depart_lat = float(depart["lat"])
            depart_lng = float(depart["lng"])
            arrivee_lat = float(arrivee["lat"])
            arrivee_lng = float(arrivee["lng"])
            # Sauvegarder dans la base de données
            trajet = Trajet.objects.create(
                user=request.user,
                nom=nom,
                depart_lat=depart_lat,
                depart_lng=depart_lng,
                etapes=json.dumps(etapes),  # Convertir les étapes en JSON
                arrivee_lat=arrivee_lat,
                arrivee_lng=arrivee_lng
            )
            # print("Trajet sauvegardé :", trajet) 
            return JsonResponse({"success": True, "message": "Trajet sauvegardé avec succès.", "trajet_id": trajet.id})
        except KeyError:
            # print("Erreur dans les données :", e)
            return JsonResponse({"success": False, "message": "Données manquantes."}, status=400)
    return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)

@csrf_exempt
def save_trajet_ibiza(request):
    if request.method == "POST":
        # print("Requête POST reçue")
        data = json.loads(request.body)
        user = request.user  # Utilisateur connecté

        # Vérifier si toutes les données sont présentes
        try:
            data = json.loads(request.body)
            nom = data["nom"]
            depart = data["depart"]
            etapes = data["etapes"]
            arrivee = data["arrivee"]
            depart_lat = float(depart["lat"])
            depart_lng = float(depart["lng"])
            arrivee_lat = float(arrivee["lat"])
            arrivee_lng = float(arrivee["lng"])
            # Sauvegarder dans la base de données
            trajet = Trajetibiza.objects.create(
                user=request.user,
                nom=nom,
                depart_lat=depart_lat,
                depart_lng=depart_lng,
                etapes=json.dumps(etapes),  # Convertir les étapes en JSON
                arrivee_lat=arrivee_lat,
                arrivee_lng=arrivee_lng
            )
            # print("Trajet sauvegardé :", trajet) 
            return JsonResponse({"success": True, "message": "Trajet sauvegardé avec succès.", "trajet_id": trajet.id})
        except KeyError:
            # print("Erreur dans les données :", e)
            return JsonResponse({"success": False, "message": "Données manquantes."}, status=400)
    return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)


@login_required
def liste_trajets(request):
    trajets = Trajet.objects.filter(user=request.user)
    serializer = TrajetSerializer(trajets, many=True)  # many=True for multiple trajets
    return JsonResponse(serializer.data, safe=False)

@login_required
def liste_trajets_ibiza(request):
    trajets = Trajetibiza.objects.filter(user=request.user)
    serializer = TrajetibizaSerializer(trajets, many=True)  # many=True for multiple trajets
    return JsonResponse(serializer.data, safe=False)

@login_required
def myiti(request):
    trajets = Trajet.objects.filter(user=request.user)
    selected_trajet = None
    
    if request.method == 'GET' and 'trajet' in request.GET:
        trajet_id = request.GET['trajet']
        if trajet_id:
            selected_trajet = get_object_or_404(Trajet, id=trajet_id, user=request.user)
    # print(f"Trajets trouvés : {trajets}")  # Ajoute cette ligne pour vérifier
    return render(request, 'tduscmap/mes_iti.html', {
        'trajets': trajets,
        'selected_trajet': selected_trajet
    })

@login_required
def myiti_ibiza(request):
    trajets = Trajetibiza.objects.filter(user=request.user)
    selected_trajet = None
    
    if request.method == 'GET' and 'trajet' in request.GET:
        trajet_id = request.GET['trajet']
        if trajet_id:
            selected_trajet = get_object_or_404(Trajetibiza, id=trajet_id, user=request.user)
    # print(f"Trajets trouvés : {trajets}")  # Ajoute cette ligne pour vérifier
    return render(request, 'tduscmap/mes_iti_ibiza.html', {
        'trajets': trajets,
        'selected_trajet': selected_trajet
    })

@login_required
def afficher_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id, user=request.user)
    serializer = TrajetSerializer(trajet)  # many=False par défaut pour un seul trajet
    return JsonResponse(serializer.data)

@login_required
def afficher_trajet_ibiza(request, trajet_id):
    trajet = get_object_or_404(Trajetibiza, id=trajet_id, user=request.user)
    serializer = TrajetibizaSerializer(trajet)  # many=False par défaut pour un seul trajet
    return JsonResponse(serializer.data)

@login_required
def get_friend_trajets(request, friend_id):
    try:
        friend = CustomUser.objects.get(id=friend_id)
        trajets = Trajet.objects.filter(user=friend).values('id', 'nom')
        return JsonResponse({'success': True, 'trajets': list(trajets)}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur introuvable.'}, status=404)

@login_required
def get_friend_trajets_ibiza(request, friend_id):
    try:
        friend = CustomUser.objects.get(id=friend_id)
        trajets = Trajetibiza.objects.filter(user=friend).values('id', 'nom')
       
        return JsonResponse({'success': True, 'trajets': list(trajets)}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur introuvable.'}, status=404)

@login_required   
def get_friend_trajet_details(request, trajet_id):
    try:
        # Récupérer l'ami en fonction de l'ID
        friend_id = request.GET.get('friend_id')
        friend = CustomUser.objects.get(id=friend_id)
        print("je suis dans friend trajet  details ibiza")
        # Récupérer les trajets associés à l'ami
        trajets_ami = Trajet.objects.filter(user=friend)

        trajet = trajets_ami.get(id=trajet_id)  # Trouver le trajet spécifique

        # Convertir les étapes en une liste de coordonnées
        etapes = trajet.etapes  # Si c'est un JSONField, il sera déjà sous forme de liste

        return JsonResponse({
            "success": True,
            "trajet": {
                "id": trajet.id,
                "nom": trajet.nom,
                "depart_lat": trajet.depart_lat,
                "depart_lng": trajet.depart_lng,
                "etapes": etapes,
                "arrivee_lat": trajet.arrivee_lat,
                "arrivee_lng": trajet.arrivee_lng,
            },
        })
    except CustomUser.DoesNotExist:
        return JsonResponse({"success": False, "error": "Ami non trouvé."})
    except Trajet.DoesNotExist:
        return JsonResponse({"success": False, "error": "Trajet non trouvé pour cet ami."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@login_required   
def get_friend_trajet_details_ibiza(request, trajet_id):
    try:
        # Récupérer l'ami en fonction de l'ID
        friend_id = request.GET.get('friend_id')
        friend = CustomUser.objects.get(id=friend_id)

        # Récupérer les trajets associés à l'ami
        trajets_ami = Trajetibiza.objects.filter(user=friend)

        trajet = trajets_ami.get(id=trajet_id)  # Trouver le trajet spécifique

        # Convertir les étapes en une liste de coordonnées
        etapes = trajet.etapes  # Si c'est un JSONField, il sera déjà sous forme de liste

        return JsonResponse({
            "success": True,
            "trajet": {
                "id": trajet.id,
                "nom": trajet.nom,
                "depart_lat": trajet.depart_lat,
                "depart_lng": trajet.depart_lng,
                "etapes": etapes,
                "arrivee_lat": trajet.arrivee_lat,
                "arrivee_lng": trajet.arrivee_lng,
            },
        })
    except CustomUser.DoesNotExist:
        return JsonResponse({"success": False, "error": "Ami non trouvé."})
    except Trajet.DoesNotExist:
        return JsonResponse({"success": False, "error": "Trajet non trouvé pour cet ami."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
@csrf_exempt  # Permet de traiter les requêtes POST sans jeton CSRF (utile pour AJAX)
def supprimer_trajet(request, trajet_id):
    if request.method == 'POST':
        trajet = get_object_or_404(Trajet, id=trajet_id)

        # Vérifier si l'utilisateur est propriétaire du trajet
        if trajet.user == request.user:
            trajet.delete()
            return JsonResponse({"success": True, "message": "Trajet supprimé avec succès."})
        else:
            return JsonResponse({"success": False, "message": "Vous n'êtes pas autorisé à supprimer ce trajet."})
    return JsonResponse({"success": False, "message": "Requête invalide."})

@csrf_exempt  # Permet de traiter les requêtes POST sans jeton CSRF (utile pour AJAX)
def supprimer_trajet_ibiza(request, trajet_id):
    if request.method == 'POST':
        trajet = get_object_or_404(Trajetibiza, id=trajet_id)

        # Vérifier si l'utilisateur est propriétaire du trajet
        if trajet.user == request.user:
            trajet.delete()
            return JsonResponse({"success": True, "message": "Trajet supprimé avec succès."})
        else:
            return JsonResponse({"success": False, "message": "Vous n'êtes pas autorisé à supprimer ce trajet."})
    return JsonResponse({"success": False, "message": "Requête invalide."})

@staff_member_required
def telecharger(request):
    """
    Vue permettant de télécharger le fichier 'test.rar'.
    Accessible uniquement par les administrateurs.
    """
    # print("je suis dans tele")
    PROJECT_ROOT = Path(__file__).resolve().parent.parent 
    chemin_fichier = os.path.join(PROJECT_ROOT, 'db.sqlite3')  
    # print(f"Chemin du fichier : {chemin_fichier}")  # Vérifiez dans la console
    if os.path.exists(chemin_fichier):
        return FileResponse(open(chemin_fichier, 'rb'), as_attachment=True, filename='db.sqlite3')
    return HttpResponse("Fichier non trouvé", status=404)


def credits(request):
    return render(
        request,
        "tduscmap/credits.html",
    )


class TrajetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trajet
        fields = '__all__'  # Ou spécifiez les champs à inclure

    def get_etapes(self, obj):
        try:
            return json.loads(obj.etapes)  # Convertir en tableau Python
        except (TypeError, json.JSONDecodeError):
            return []

class TrajetibizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trajetibiza
        fields = '__all__'  # Ou spécifiez les champs à inclure

    def get_etapes(self, obj):
        try:
            return json.loads(obj.etapes)  # Convertir en tableau Python
        except (TypeError, json.JSONDecodeError):
            return []

@login_required
def ibiza(request):
    return render(
        request,
        "tduscmap/ibiza_eivissa.html",
    )


def changer_langue(request):
    nouvelle_langue = request.GET.get('langue')  # 'fr' ou 'en'
    if nouvelle_langue in ['fr', 'en']:
        request.session['langue'] = nouvelle_langue
    return redirect(request.META.get('HTTP_REFERER', '/'))

# @login_required
def farm(request):
    return render(
        request,
        "tduscmap/farm.html",
    )