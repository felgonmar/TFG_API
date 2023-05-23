from django.http import JsonResponse
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2, playbyplayv2
from datetime import datetime


def get_games_by_date(request ):
    try:
        date = request.GET.get('date', datetime.now().strftime("%m/%d/%Y"))

        games = leaguegamefinder.LeagueGameFinder(date_from_nullable=date, date_to_nullable=date, league_id_nullable='00').get_normalized_dict()

        return JsonResponse(games)
    except Exception as e:
        return JsonResponse({"error": str(e)})

def get_game_details(request, game_id):
    try:
        box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_normalized_dict()

        play_by_play = playbyplayv2.PlayByPlayV2(game_id=game_id).get_normalized_dict()

        return JsonResponse({"box_score": box_score, "play_by_play": play_by_play})
    except Exception as e:
        return JsonResponse({"error": str(e)})
