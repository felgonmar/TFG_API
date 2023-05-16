"""
URL configuration for nba_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views, players_functions, teams_functions

urlpatterns = [
    path('admin/', admin.site.urls),
    #Teams url
    path('teams/',  teams_functions.team_list, name='team_list'),
    path('teams/<int:team_id>/players/', teams_functions.team_players, name='team_players'),
    #players url
    path('playerStats/<int:player_id>/', players_functions.player_stats, name='player_stats'),
    path('playerCompare/<int:player_id>/<int:vs_player_id>', players_functions.playerCompare, name='player_compare'),
    path('playerCommonInfo/<int:player_id>/', players_functions.player_common_info, name='player_common_info')
]
