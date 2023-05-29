from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import leaguestandings
from json import JSONDecodeError
from django.http import JsonResponse


#TODO: Sort 
def get_standings(request):
    try:
        season_id = request.GET.get('season_id', SeasonAll.default)
        standings= leaguestandings.LeagueStandings(season=season_id).get_normalized_dict()
        standings_sorted =sorted(standings['Standings'], key=lambda team: team['Record'], reverse=True)
        standings['Standings'] = standings_sorted
        return JsonResponse(standings)
    except JSONDecodeError:
        return JSONDecodeError({'error': 'Invalid season id'}, status=400)
                
def get_conference_standings(request):
    try:
        season_id = request.GET.get('season_id', SeasonAll.default)
        
        standings = leaguestandings.LeagueStandings(season=season_id).get_normalized_dict()
        east_list =[]
        west_list=[]
        for team in standings['Standings']:
            if team['Conference'] == 'East':
                east_list.append(team)
            else:
                west_list.append(team)
                
        east_list_sorted = sorted(east_list, key=lambda team: team['Record'], reverse=True)
        west_list_sorted = sorted(west_list, key=lambda team: team['Record'], reverse=True)
        return JsonResponse({'West':west_list_sorted,'East':east_list_sorted})
    except:
        return JSONDecodeError({'error': 'Invalid season id'}, status=400)
    
    
def get_all_seasons(request):
     
    return JsonResponse({'seasonList':[f"{year}-{str(year+1)[-2:]}" for year in range(1980, 2022+1)][::-1]})

