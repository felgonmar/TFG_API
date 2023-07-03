
from rest_framework.response import Response
from .models import Rating, User
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def rate(request):
    try:
        data = json.loads(request.body)

        user_id = data.get('user_id')
        game_id = data.get('game_id', None)
        player_id = data.get('player_id', None)
        team_id = data.get('team_id', None)
        rating_value = data.get('rating')
        comment = data.get('comment', None)


        if sum([bool(game_id), bool(player_id), bool(team_id)]) != 1:
            return JsonResponse({"error": "You must rate a game, player or team, but not more than 1 at the time."}, status=400)

        if not (0 <= int(rating_value) <= 10):
            return JsonResponse({"error": "Rating must be between 0 and 10."}, status=400)

        user = User.objects.get(pk=user_id)
        rating= Rating.objects.filter(user=user, game_id=game_id, player_id=player_id, team_id=team_id).first()
        if rating:
            rating.rating = rating_value
            if comment:
                rating.comment = comment
        else:
            
            rating = Rating.objects.create(user=user, game_id=game_id, player_id=player_id, team_id=team_id, rating=rating_value, comment=comment)    
        # rating = Rating.objects.update_or_create(user=user, game_id=game_id, player_id=player_id, team_id=team_id, rating=rating_value)[0]
        rating.save()

        return JsonResponse({"message": "Rating successfully created."}, status=201)
    except Exception as e:
         return JsonResponse({"error": e}, status=400)



def get_ratings(request):
    try:
        target_type = request.GET.get('type')  
        target_id = request.GET.get('id')  

        if target_type not in ['player', 'game', 'team']:
            return JsonResponse([])  
        ratings = Rating.objects.filter(**{f'{target_type}_id': target_id})
        if len(ratings.all())>0:
            ratings_list = [model_to_dict(rating) for rating in ratings]  
            total = sum(rating['rating'] for rating in ratings_list) /len(ratings_list)
            return JsonResponse({'total':total}, safe=False)
        else:
              return JsonResponse({"error": 'No  ratings for this id'}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
@csrf_exempt    
def get_user_rating(request):
    try:
        target_type = request.GET.get('type')  
        target_id = request.GET.get('id')  
        user_id = request.GET.get('user_id')  
        if target_type not in ['player', 'game', 'team']:
            return JsonResponse({'error': 'no type provided'}, status=400)
        else:
            rate_type = switch_target(target_type)
            kwargs = {
                '{}'.format(rate_type): target_id,
                'user_id': user_id
            }
            rating = Rating.objects.filter(**kwargs).first()
        
            if rating:
                return JsonResponse({'id':rating.id,'rating': rating.rating, 'comment':rating.comment})  
            else:
                return JsonResponse({'error': 'No rating found'},status=404)

    except Exception as e: 
        return JsonResponse({"error":  str(e)}, status=400)   


def switch_target(target):
    return {'player': 'player_id',
            'game':'game_id',
            'team':'team_id'}.get(target, None)