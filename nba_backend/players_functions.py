from django.http import JsonResponse
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo,playercareerstats, playercompare
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