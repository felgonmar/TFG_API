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
from . import views, players_functions, teams_functions, seasons, user, games, news
from .rating import RatingListView,CreateRatingView

urlpatterns = [
    path('admin/', admin.site.urls),
    #Teams url
    path('teams/',  teams_functions.team_list, name='team_list'),
    path('teams/<int:team_id>/players/', teams_functions.team_players, name='team_players'),
    #players url
    path('playerStats/<int:player_id>/', players_functions.player_stats, name='player_stats'),
    path('playerCompare/<int:player_id>/<int:vs_player_id>', players_functions.playerCompare, name='player_compare'),
    path('playerCommonInfo/<int:player_id>/', players_functions.player_common_info, name='player_common_info'),
    path('playerAdvancedStats/<int:player_id>', players_functions.get_advanced_stats, name='player_advanced_stats'),
    path('playerFinder/<str:name>', players_functions.playerFinder, name='player_finder'),
    #Seasons
    path('standings', seasons.get_standings, name='standings'),
    path('conferenceStandings', seasons.get_conference_standings, name='conference_standings'),
    #User
    path('register/', user.register, name='register'), #post
    path('login/', user.login, name='login'), #post
    path('logout/', user.log_out, name='logout'),
    #rating
    path('ratings/', RatingListView.as_view, name='ratings_list'),
    path('create-rating/', CreateRatingView.as_view, name='create_rating'), #post
    #games
    path('gamesByDate',games.get_games_by_date, name='gamesDate'),
    path('game/<str:game_id>/', games.get_game_details, name='game'),
    #news
    path('news', news.get_news, name="news"),
]
