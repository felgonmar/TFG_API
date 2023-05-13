from django.http import JsonResponse
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, playerdashboardbylastngames, playergamelog
from nba_api.stats.library.parameters import SeasonAll
from json import JSONDecodeError
from rest_framework.decorators import api_view

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
        player_stats.append(dict(zip(player,headers)))
    res = {
        'players': players,
        'headers': headers
    }
    return JsonResponse(res, safe=False)

def team_players_headers(request, team_id):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id)
    headers = roster.get_dict()['resultSets'][0]['rowSet']
    return JsonResponse(headers, safe=False)


@api_view(['GET'])
def player_stats(request, player_id):
    try:
        # Usa la API para obtener las estadísticas del jugador
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season = SeasonAll.current_season)

        # Convierte las estadísticas a un diccionario
        gamelog_dict = gamelog.get_normalized_dict()

        # Las estadísticas de los partidos están en 'PlayerGameLog'
        games_stats = gamelog_dict['PlayerGameLog']

        # Aquí puedes procesar las estadísticas de los partidos para obtener las estadísticas agregadas
        # Por ejemplo, puedes sumar todos los puntos para obtener el total de puntos de la temporada
        # Este es un ejemplo simple y es posible que quieras agregar más lógica aquí
        total_points = sum(game['PTS'] for game in games_stats)

        # Devuelve las estadísticas como respuesta JSON
        return JsonResponse({'total_points': total_points})

    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid player id or season'}, status=400)
    # Usa la API para obtener las estadísticas del jugador
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season = SeasonAll.current_season)

    # Convierte las estadísticas a un diccionario
    gamelog_dict = gamelog.get_normalized_dict()

    # Las estadísticas de los partidos están en 'PlayerGameLog'
    games_stats = gamelog_dict['PlayerGameLog']

    # Aquí puedes procesar las estadísticas de los partidos para obtener las estadísticas agregadas
    # Por ejemplo, puedes sumar todos los puntos para obtener el total de puntos de la temporada
    # Este es un ejemplo simple y es posible que quieras agregar más lógica aquí
    total_points = sum(game['PTS'] for game in games_stats)

    # Devuelve las estadísticas como respuesta JSON
    return JsonResponse({'total_points': total_points})