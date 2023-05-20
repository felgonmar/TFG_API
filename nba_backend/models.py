from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=128)
    
    # class Meta:
    #     db_table = 'users'

    def save(self, *args, **kwargs):
        if self.password_hash:
            self.password_hash = make_password(self.password_hash)
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.full_name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.IntegerField(null=True, blank=True)
    player_id = models.IntegerField(null=True, blank=True)
    team_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField()

    def save(self, *args, **kwargs):
        # checking that only 1 of the fields is written
        if sum([bool(self.game_id), bool(self.player_id), bool(self.team_id)]) != 1:
            raise ValidationError("You must rate a game, player or team, but not more than 1 at the time.")

        super().save(*args, **kwargs)