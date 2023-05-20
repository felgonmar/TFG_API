from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rating, User
from django.views.generic.list import ListView


class CreateRatingView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        game_id = request.data.get('game_id', None)
        player_id = request.data.get('player_id', None)
        team_id = request.data.get('team_id', None)
        rating_value = request.data.get('rating')

        if sum([bool(game_id), bool(player_id), bool(team_id)]) != 1:
            return Response({"error": "Debe calificar a un juego, jugador o equipo, pero no a más de uno al mismo tiempo."}, status=400)

        if not (0 <= rating_value <= 10):
            return Response({"error": "El rating debe ser entre 0 y 10."}, status=400)

        user = User.objects.get(pk=user_id)
        rating = Rating.objects.create(user=user, game_id=game_id, player_id=player_id, team_id=team_id, rating=rating_value)
        rating.save()

        return Response({"message": "Rating successfully created."}, status=201)

class RatingListView(ListView):
    model = Rating
    context_object_name = 'ratings'  # Opcional: este será el nombre del objeto en tu template

    def get_queryset(self):
        target_type = self.request.GET.get('type')  
        target_id = self.request.GET.get('id')  

        if target_type not in ['player', 'game', 'team']:
            return self.model.objects.none()  

        return self.model.objects.filter(**{f'{target_type}_id': target_id})  