
from rest_framework.response import Response
from .models import Rating, User
from django.http import JsonResponse
from django.forms.models import model_to_dict

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def rate(request):
    user_id = request.POST.get('user_id')
    game_id = request.POST.get('game_id', None)
    player_id = request.POST.get('player_id', None)
    team_id = request.POST.get('team_id', None)
    rating_value = request.POST.get('rating')

    if sum([bool(game_id), bool(player_id), bool(team_id)]) != 1:
        return JsonResponse({"error": "You must rate a game, player or team, but not more than 1 at the time."}, status=400)

    if not (0 <= int(rating_value) <= 10):
        return JsonResponse({"error": "Rating must be between 0 and 10."}, status=400)

    user = User.objects.get(pk=user_id)
    rating = Rating.objects.update_or_create(user=user, game_id=game_id, player_id=player_id, team_id=team_id, rating=rating_value)[0]
    rating.save()

    return JsonResponse({"message": "Rating successfully created."}, status=201)



def get_ratings(request):
    try:
        target_type = request.GET.get('type')  
        target_id = request.GET.get('id')  

        if target_type not in ['player', 'game', 'team']:
            return JsonResponse([])  
        ratings = Rating.objects.filter(**{f'{target_type}_id': target_id})
        ratings_list = [model_to_dict(rating) for rating in ratings]  
        return JsonResponse(ratings_list, safe=False)  
    except Exception as e:
        return JsonResponse({"error": str(e)})