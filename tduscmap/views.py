
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from .models import Favorite, Car, CarPrice
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from django.db.models import Prefetch

def home(request):
    return render(
        request,
        "home.html",
    )


def ajouter_favori(request):
    if request.method == 'POST':
        try:
            # Convertir les données JSON en dictionnaire Python
            data = json.loads(request.body)
            lat = data.get('lat')
            lng = data.get('lng')
            description = data.get('description')
            # Créer et sauvegarder un nouveau favori dans la base de données
            Favorite.objects.create(user=request.user,lat=lat, lng=lng, description=description)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
# Supprimer un favori
# @login_required
def supprimer_favori(request, favori_id):
    favori = Favorite.objects.get(id=favori_id, user=request.user)
    favori.delete()
    return redirect('afficher_favoris')
# Afficher les favoris de l'utilisateur connecté
# @login_required
def afficher_favoris(request):
    favoris = Favorite.objects.filter(user=request.user)
    return render(request, 'afficher_favoris.html', {'favoris': favoris})

def mymaps(request):
    return render(request, 'tduscmap/mymaps.html')


@login_required
def get_favorites(request):
    """Récupérer les favoris de l'utilisateur connecté."""
    user = request.user  # Cela devrait être votre CustomUser
    favorites = Favorite.objects.filter(user=user)  # Filtrer les favoris par utilisateur
    favorites_list = [{'id': favorite.id, 'lat': favorite.lat, 'lng': favorite.lng, 'description': favorite.description} for favorite in favorites]
    return JsonResponse(favorites_list, safe=False)


@require_http_methods(["DELETE"])
def delete_favorite(request, favorite_id):
    try:
        favorite = Favorite.objects.get(id=favorite_id)
        favorite.delete()
        return JsonResponse({'success': True})
    except Favorite.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Favori introuvable'})


@login_required
def get_friends(request):
    """Récupérer la liste des amis de l'utilisateur."""
    user = request.user  # Cela devrait être votre CustomUser
    friends = user.friends.all()  # Assurez-vous que le champ friends existe dans CustomUser
    friend_list = [{'id': friend.id, 'username': friend.username} for friend in friends]
    return JsonResponse(friend_list, safe=False)


@login_required
def get_friend_favorites(request, friend_id):
    if request.method == 'GET':
        try:
            friend = CustomUser.objects.get(id=friend_id)
            favorites = Favorite.objects.filter(user=friend)
            favorites_data = [{
                'id': fav.id,
                'lat': fav.lat,
                'lng': fav.lng,
                'description': fav.description
            } for fav in favorites]
            return JsonResponse(favorites_data, safe=False)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Ami non trouvé'}, status=404)


def search_friends(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = CustomUser.objects.filter(username__icontains=search_query)
    else:
        users = CustomUser.objects.none()

    results = [{'username': user.username, 'id': user.id} for user in users]
    return JsonResponse({'users': results})



@csrf_exempt
def add_friend(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            friend_id = data.get('friend_id')  # L'ID de l'ami à ajouter

            user = CustomUser.objects.get(id=user_id)
            friend = CustomUser.objects.get(id=friend_id)

            # Vérifie si l'utilisateur n'essaie pas de s'ajouter lui-même
            if user.id == friend.id:
                return JsonResponse({'success': False, 'message': 'Vous ne pouvez pas vous ajouter comme ami.'})

            # Ajoute l'ami
            user.friends.add(friend)

            return JsonResponse({'success': True, 'message': 'Ami ajouté avec succès !'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Utilisateur non trouvé'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Erreur de décodage JSON'})
    else:
        return JsonResponse({'success': False, 'message': 'Requête non autorisée'})
    

# def car_price_history(request, car_id):
#     car = Car.objects.get(id=car_id)
#     prices = car.historique_prix.all().order_by('date')

#     # Préparer les données pour Chart.js
#     dates = [price.date.strftime('%Y-%m-%d') for price in prices]
#     price_values = [price.prix for price in prices]

#     # Ajouter le prix initial au début de la liste des prix
#     price_values.insert(0, car.prix_initial)
#     dates.insert(0, 'Prix initial')  # Pour ajouter une étiquette pour le prix initial

#     context = {
#         'car': car,
#         'dates': dates,
#         'price_values': price_values,
#     }
#     return render(request, 'tduscmap/car_price_history.html', context)


def car_price_choice(request):
    cars = Car.objects.all()  # Fetch all cars initially
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        car_selected = Car.objects.get(pk=car_id)  # Assuming primary key is 'id'
    # Préparer les données pour Chart.js
        prices = car_selected.historique_prix.all().order_by('date')
        dates = [price.date.strftime('%Y-%m-%d') for price in prices]
        price_values = [price.prix for price in prices]

        # Ajouter le prix initial au début de la liste des prix
        price_values.insert(0, car_selected.prix_initial)
        dates.insert(0, 'Prix initial')  # Pour ajouter une étiquette pour le prix initial

        context = {
            'cars': cars,
            'car_selected': car_selected,
            'dates': dates,
            'price_values': price_values,
        }
    else:
        car_selected = None
        context = {'cars': cars, 'car_selected': car_selected}

    return render(request, 'tduscmap/car_list.html', context)

def car_prices_view(request):
    cars = Car.objects.prefetch_related('historique_prix').all()
    
    prices_data = {}
    for car in cars:
        prices_data[car] = []
        for price in car.historique_prix.all():
            prices_data[car].append({
                'date': price.date,
                'prix': price.prix if price.prix is not None else None
            })

    context = {
        'prices_data': prices_data,
    }
    return render(request, 'tduscmap/car_prices.html', context)