from django.http import JsonResponse
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import commonplayerinfo,playercareerstats, playercompare, playerdashboardbygeneralsplits, playergamelog, boxscoretraditionalv2
from nba_api.stats.library.parameters import SeasonAll
from json import JSONDecodeError
from . import utils


def player_common_info(request, player_id):
    try:
        info = get_common_player_info(player_id)
        print(info)
        return JsonResponse(info)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid player id'}, status=400)

def player_stats(request, player_id):
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id).get_normalized_dict() #['resultSets']
        print(career)
        return JsonResponse(career)           

    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid player id or season'}, status=400)
    
    
def get_advanced_stats(request,player_id):
    try:
        season_id = request.GET.get('seasonId', SeasonAll.default)
        player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id, season=season_id, timeout=60).get_normalized_dict()
       
        for key in player_dashboard:
            print(key)
            for item in player_dashboard[key]:
                print(item)
                #def rat is a dense call, only for the first one
                if key == 'OverallPlayerDashboard':
                    player_dashboard[key][player_dashboard[key].index(item)]['OFF_RAT'] =get_off_rat(player_dashboard[key][player_dashboard[key].index(item)])
                    player_dashboard[key][player_dashboard[key].index(item)]['DEF_RAT'] =get_def_rat(player_dashboard[key][player_dashboard[key].index(item)], player_id, season_id)
                    player_dashboard[key][player_dashboard[key].index(item)]['NET_RAT'] = player_dashboard[key][player_dashboard[key].index(item)]['OFF_RAT'] - player_dashboard[key][player_dashboard[key].index(item)]['DEF_RAT']
                player_dashboard[key][player_dashboard[key].index(item)]['PER']= get_per(player_dashboard[key][player_dashboard[key].index(item)])
                player_dashboard[key][player_dashboard[key].index(item)]['EFG'] = get_efg(player_dashboard[key][player_dashboard[key].index(item)])
                player_dashboard[key][player_dashboard[key].index(item)]['TS']=get_ts(player_dashboard[key][player_dashboard[key].index(item)])
                player_dashboard[key][player_dashboard[key].index(item)]['TS']=get_win_shares(player_dashboard[key][player_dashboard[key].index(item)])
        return JsonResponse(player_dashboard)
    except JSONDecodeError:
        return JsonResponse({'error':'Invalid player or season'}, status=400)   
     


def playerCompare(request, player_id, vs_player_id):
    try:

        seasonId = request.GET.get('seasonId', SeasonAll.default)
        compare = playercompare.PlayerCompare(
            player_id, vs_player_id, season=seasonId
        )
        
        data = compare.get_normalized_dict() 
        return JsonResponse(data)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid player id'}, status=400)
    
    

#player finder for only active players and for more than 3 chars
def playerFinder(request,name):
    try:
        if len(name) <3:
            return JsonResponse({'error': 'name has to be at least 3 chars lenght'}, status=400)
        else:
            p1= players.find_players_by_full_name(name)
            active_players = [player for player in p1 if player['is_active']]
            for player in active_players:
                player['commonPlayerInfo']=get_common_player_info(player['id'])['CommonPlayerInfo'][0]
            return JsonResponse({'players': active_players})
    except JSONDecodeError as e:
        return JsonResponse({'error': e}, status=400)
    
def get_per(player_data):
    """
    Calculate the simplified Player Efficiency Rating (PER) based on the given player data.
    """

    # Extract necessary stats
    pts = player_data.get('points', 0)
    three_p = player_data.get('three_points_made', 0)
    ast = player_data.get('assists', 0)
    orb = player_data.get('offensive_rebounds', 0)
    drb = player_data.get('defensive_rebounds', 0)
    stl = player_data.get('steals', 0)
    blk = player_data.get('blocks', 0)
    to = player_data.get('turnovers', 0)
    fta = player_data.get('free_throws_attempted', 0)
    fga = player_data.get('field_goals_attempted', 0)
    min_played = player_data.get('minutes_played', 1)  # avoid division by zero

    # Calculate PER
    per = (pts + three_p + 0.5*ast + 1.25*orb + drb + stl + 0.5*blk - to - 0.5*fta - 0.5*fga) / min_played

    return per

#approximated because it´s really hard to calc it prop
def get_win_shares(player_stats):
    pts = player_stats['PTS']
    ast = player_stats['AST']
    reb = player_stats['REB']
    stl = player_stats['STL']
    blk = player_stats['BLK']
    tov = player_stats['TOV']
    fga = player_stats['FGA']
    fta = player_stats['FTA']   
    team_wins = player_stats['W']
    
    offensive_contribution = pts + ast + reb - fga - fta
    defensive_contribution = stl + blk - tov
    
    approximate_ws = (offensive_contribution + defensive_contribution) / 10
    
    return approximate_ws / team_wins


def get_efg(player_stats): # effective Field Goal percentage (FG + 0.5 * 3P) / FGA.
    fg = player_stats['FGM']
    fg3 = player_stats['FG3M']  # Three-Point Field Goals Made
    fga = player_stats['FGA']  # Field Goal Attempts

    efg = (fg + 0.5 * fg3) / fga

    return efg



def get_ts(player_stats): # True Shooting Percentage  PTS / (2 * TSA). TSA= todos los tiros intentados (3pt, 2pt, FT). tsa = FGA + 0.44 * FTA.
    pts = player_stats['PTS']  # Points
    fga = player_stats['FGA']  # Field Goal Attempts
    fta = player_stats['FTA']  # Free Throw Attempts

    ts = pts / (2 * (fga + 0.44 * fta))

    return ts

def get_off_rat(player_stats):# Offensive Rating = (Pts + Ast + FG + (0.5 * 3P)) / (FGA + (0.44 * FTA) + Ast + TO)
    
    Pts = player_stats['PTS']
    Ast = player_stats['AST']
    FG = player_stats['FGM']
    ThreeP = player_stats['FG3M']
    FGA = player_stats['FGA']
    FTA = player_stats['FTA']
    TO = player_stats['TOV']
    
    if (FGA + (0.44 * FTA) + Ast + TO) != 0:
        Off_Rating = (Pts + Ast + FG + (0.5 * ThreeP)) / (FGA + (0.44 * FTA) + Ast + TO)
        return Off_Rating * 100
    else:
        return 0
def get_def_rat(player_stats, player_id, season_id): #Defensive Rating = 100 * (Opponent Points / (Opponent FGA + (0.44 * Opponent FTA) + Opponent TOV)) - 0.5 * (Steals + Blocks) / (Opponent FGA + (0.44 * Opponent FTA) + Opponent TOV)
    
    opponent_stats = get_opponent_stats(player_id,season_id)
    opponent_points = opponent_stats['PTS']
    opponent_fga = opponent_stats['FGA']
    opponent_fta = opponent_stats['FTA']
    opponent_tov = opponent_stats['TOV']
    player_steals = player_stats['STL']
    player_blocks = player_stats['BLK']

    if (opponent_fga + 0.44 * opponent_fta - opponent_tov) != 0:
        defensive_rating = 100 * (opponent_points / (opponent_fga + 0.44 * opponent_fta - opponent_tov)) - 0.5 * (player_steals + player_blocks) / (opponent_fga + 0.44 * opponent_fta - opponent_tov)

        return defensive_rating
    else:
        return 0



def get_opponent_stats(player_id, season):
    # Obtén todos los juegos del jugador en una temporada
    gamelog = playergamelog.PlayerGameLog(player_id, season)
    games = gamelog.get_data_frames()[0]
    
    opponent_stats = {'PTS': 0, 'FGA': 0, 'FTA': 0, 'TOV': 0}

    # Para cada juego, obtén las estadísticas del equipo oponente
    for i in range(len(games)):
        game_id = games['Game_ID'][i]
        matchup = games['MATCHUP'][i]

        # Dividir la cadena de emparejamiento para obtener los equipos
        teams = matchup.split(' ')
        if teams[1] == 'vs.':
            opponent_team_abbreviation = teams[2]
        else: # El jugador está jugando fuera, por lo que el oponente es el primer equipo
            opponent_team_abbreviation = teams[0]

        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id)
        team_stats = boxscore.get_data_frames()[1]

        # Identifica qué fila de team_stats corresponde al equipo oponente
        opponent_row = team_stats[team_stats['TEAM_ABBREVIATION'] == opponent_team_abbreviation]

        # Suma las estadísticas del equipo oponente a las totales
        opponent_stats['PTS'] += opponent_row['PTS'].values[0]
        opponent_stats['FGA'] += opponent_row['FGA'].values[0]
        opponent_stats['FTA'] += opponent_row['FTA'].values[0]
        opponent_stats['TOV'] += opponent_row['TO'].values[0]
        
    return opponent_stats


def get_common_player_info(player_id):
    try:
        info = commonplayerinfo.CommonPlayerInfo(player_id).get_normalized_dict()
        return info
    except:
        KeyError('Invalid player_id')