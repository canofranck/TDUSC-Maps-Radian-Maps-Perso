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
    path('admin/', admin.site.urls),
    path(
        "login",
        LoginView.as_view(
            template_name="authentication/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path('mymaps/ajouter-favori/', tduscmap.views.ajouter_favori,
         name='ajouter_favori'),
    path('favorites/', tduscmap.views.get_favorites, name='get_favorites'),
    
    path('favorites/<int:favorite_id>/delete/', tduscmap.views.delete_favorite,
         name='delete_favorite'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("", tduscmap.views.home, name="home"),
    path("mymaps/", tduscmap.views.mymaps, name="mymaps"),
    path('get_friends/', tduscmap.views.get_friends, name='get_friends'),
    path('friends/<int:friend_id>/favorites/', tduscmap.views.get_friend_favorites, name='get_friend_favorites'),
    path('search-friends/', tduscmap.views.search_friends, name='search_friends'),
    path('add-friend/<int:user_id>/', tduscmap.views.add_friend, name='add_friend'),
    # path('car/<int:car_id>/price-history/', tduscmap.views.car_price_history, name='car_price_history'),
    path('car/select/', tduscmap.views.car_price_choice, name='car_select'),
    path('car-prices/', tduscmap.views.car_prices_view, name='car_prices'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )