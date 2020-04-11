"""rook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('enter_game/', views.enter_game, name='enter_game'),
    path('game/', views.game, name='game'),
    path('bid/', views.bid, name='bid'),
    path('discard/', views.discard, name='discard'),
    path('select_trump/', views.select_trump, name='select_trump'),
    path('play_card/', views.play_card, name='play_card'),
    path('reset/', views.reset, name='reset'),
    path('state/', views.state, name='state'),
    path('create_game/', views.create_game, name='create_game'),
    path('delete_game/', views.delete_game, name='delete_game'),
    path('player_name/', views.player_name, name='player_name'),
    path('active_check/', views.active_check, name='active_check'),
]
