"""
URL configuration for authentication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
import authentication.views
import tduscmap.views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login",
        LoginView.as_view(
            template_name="authentication/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "mymaps/ajouter-favori/",
        tduscmap.views.ajouter_favori,
        name="ajouter_favori",
    ),
    path("favorites/", tduscmap.views.get_favorites, name="get_favorites"),
    path(
        "favorites/<int:favorite_id>/delete/",
        tduscmap.views.delete_favorite,
        name="delete_favorite",
    ),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("", tduscmap.views.home, name="home"),
    path("mymaps/", tduscmap.views.mymaps, name="mymaps"),
    

    path("get_friends/", tduscmap.views.get_friends, name="get_friends"),
    path(
        "friends/<int:friend_id>/favorites/",
        tduscmap.views.get_friend_favorites,
        name="get_friend_favorites",
    ),
    path(
        "search-friends/", tduscmap.views.search_friends, name="search_friends"
    ),
    path(
        "add-friend/<int:user_id>/",
        tduscmap.views.add_friend,
        name="add_friend",
    ),
    path("car/select/", tduscmap.views.car_price_choice, name="car_select"),
    path("car-prices/", tduscmap.views.car_prices_view, name="car_prices"),
    path("reglages/", tduscmap.views.liste_reglages, name="liste_reglages"),
    path(
        "reglages/<int:pk>/",
        tduscmap.views.detail_reglage,
        name="detail_reglage",
    ),
    # path(
    #     "get-configuration/<int:car_id>/",
    #     tduscmap.views.get_configuration,
    #     name="get_configuration",
    # ),
    path("choix_modele/", tduscmap.views.choix_modele, name="choix_modele"),
    path(
        "saisie_reglage/<int:car_id>/",
        tduscmap.views.saisie_reglage,
        name="saisie_reglage",
    ),
    # path("user_configurationreglage/<int:car_id>/", tduscmap.views.user_configurationreglage, name="user_configurationreglage"),
    path('modifier_reglages/<int:id>/', tduscmap.views.modifier_reglages, name='modifier_reglages'),
    path('mes_reglages/', tduscmap.views.mes_reglages, name='mes_reglages'),
    path('supprimer_reglage/<int:id>/', tduscmap.views.supprimer_reglage, name='supprimer_reglage'),
    path("save_trajet/", tduscmap.views.save_trajet, name="save_trajet"),
    path('myiti/', tduscmap.views.myiti, name='myiti'),
    path('list_trajets/', tduscmap.views.liste_trajets, name='list_trajets'),
    path('afficher_trajets/<int:trajet_id>/', tduscmap.views.afficher_trajet, name='afficher_trajet'),
    path('get-friend-trajets/<int:friend_id>/', tduscmap.views.get_friend_trajets, name='get_friend_trajets'),
    path('get-friend-trajet-details/<int:trajet_id>/', tduscmap.views.get_friend_trajet_details, name='get_friend_trajet_details'),
    path('delete-trajet/<int:trajet_id>/', tduscmap.views.supprimer_trajet, name='delete_trajet'),
    path('telecharger/', tduscmap.views.telecharger, name='telecharger'),
    path('credits/', tduscmap.views.credits, name='credits'),
]  
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
