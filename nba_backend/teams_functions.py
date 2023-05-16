from django.http import JsonResponse
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, playerdashboardbylastngames, playergamelog,playercareerstats, playercompare
from nba_api.stats.library.parameters import SeasonAll
from json import JSONDecodeError
from rest_framework.decorators import api_view
from . import utils

def team_list(request):
    team_list = teams.get_teams()
    return JsonResponse(team_list, safe=False)

def team_players(request, team_id):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_dict()
    
    players = roster['resultSets'][0]['rowSet']
    headers = roster['resultSets'][0]['headers']
    player_stats= []
    #to return the dict
    for player in players:
        player_stats.append(dict(zip(headers,player)))
    res = {
        'players': players,
        'headers': headers,
        'players_dict':player_stats
    }
    return JsonResponse(res, safe=False)

def team_players_headers(request, team_id):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id)
    headers = roster.get_dict()['resultSets'][0]['rowSet']
    return JsonResponse(headers, safe=False)
