
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import Favorite
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import CustomUser


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