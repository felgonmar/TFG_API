from django.http import JsonResponse
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo,playercareerstats, playercompare, playerdashboardbygeneralsplits, leaguedashplayerstats
from nba_api.stats.library.parameters import SeasonAll
from json import JSONDecodeError
from . import utils


def player_common_info(request, player_id):
    try:
        info = commonplayerinfo.CommonPlayerInfo(player_id).get_normalized_dict()
        print(info)
        return JsonResponse(info)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid player id'}, status=400)

def player_stats(request, player_id):
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id).get_normalized_dict() #['resultSets']
        print(career)
        # player_stats ={}
        # for category in career:
        #     name = category['name']
        #     headers = category['headers']
        #     stats= {}
        #     for season in category['rowSet']:
        #         season_dict = (dict(zip(headers,season)))
        #         if 'SEASON_ID' in season_dict:
        #             stats[season_dict['SEASON_ID']]= season_dict
        #         else:
        #             stats['TOTAL']=season_dict
        #     player_stats[name] = stats
        return JsonResponse(career)           

    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid player id or season'}, status=400)
    
    
def get_advanced_stats(request,player_id):
    try:
        player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id).get_normalized_dict()
        get_off_rat(player_id)
        for key in player_dashboard:
            print(key)
            for item in player_dashboard[key]:
                print(item)
                player_dashboard[key][player_dashboard[key].index(item)]['PER']= get_per(player_dashboard[key][player_dashboard[key].index(item)])
        
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

#not like this
def get_win_shares(player_data):
    """
    Calculate the simplified Win Shares based on the given player data.
    """

    # Extract necessary stats
    pts = player_data.get('points', 0)
    drb = player_data.get('defensive_rebounds', 0)
    orb = player_data.get('offensive_rebounds', 0)
    ast = player_data.get('assists', 0)
    stl = player_data.get('steals', 0)
    blk = player_data.get('blocks', 0)
    to = player_data.get('turnovers', 0)
    fga = player_data.get('field_goals_attempted', 0)
    fta = player_data.get('free_throws_attempted', 0)
    min_played = player_data.get('minutes_played', 1)  # avoid division by zero

    # Calculate Win Shares (very simplified)
    ws = (pts + drb + orb + ast + stl + blk - to - 0.5*fga - 0.5*fta) / min_played

    return ws

#TODO:
#def get_efg effective Field Goal percentage (FG + 0.5 * 3P) / FGA.
#def get_ts True Shooting Percentage  PTS / (2 * TSA). TSA= todos los tiros intentados (3pt, 2pt, FT)
# def get_off_rat(player_id, season_id='22021'):
#     from nba_api.stats.endpoints import playerdashboardbygeneralsplits

#     player_dashboard = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id, season=season_id)
#     player_dashboard_dict = player_dashboard.get_dict()

#     result_sets = player_dashboard_dict['resultSets']

#     for result_set in result_sets:
#         if result_set['name'] == 'OverallPlayerDashboard':
#             headers = result_set['headers']
#             rows = result_set['rowSet']

#             # Extract the player's data
#             player_data = dict(zip(headers, rows[0]))

#             # The number of possessions a player uses can be approximated by the sum of field goal attempts,
#             # turnovers, and 0.44 times free throw attempts (to account for possessions ending in free throws)
#             possessions = player_data['FGA'] + player_data['TO'] + 0.44 * player_data['FTA']

#             # Calculate the offensive rating
#             off_rat = 100 * player_data['PTS'] / possessions

#             return off_rat




# def get_off_rat(player_id, season): Offensive Rating = (Pts + Ast + FG + (0.5 * 3P)) / (FGA + (0.44 * FTA) + Ast + TO)

#     player_stats = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id, season=season)
#     player_stats_dict = player_stats.get_normalized_dict()
#     player_overall_stats = player_stats_dict['OverallPlayerDashboard'][0]
    
#     Pts = player_overall_stats['PTS']
#     Ast = player_overall_stats['AST']
#     FG = player_overall_stats['FGM']
#     ThreeP = player_overall_stats['FG3M']
#     FGA = player_overall_stats['FGA']
#     FTA = player_overall_stats['FTA']
#     TO = player_overall_stats['TOV']
    
#     if (FGA + (0.44 * FTA) + Ast + TO) != 0:
#         Off_Rating = (Pts + Ast + FG + (0.5 * ThreeP)) / (FGA + (0.44 * FTA) + Ast + TO)
#         return Off_Rating * 100
#     else:
#         return None
#def get_def_rat
#def get_net_rat (off_rat - def_rat)