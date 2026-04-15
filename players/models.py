from django.db import models
from players.options import ROLE_CHOICES

class Players(model.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'player')
    team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.SET_NULL)
    primary_role = models.CharField(max_length = 50, choices = ROLE_CHOICES)
    secondary_role = models.CharField(max_length = 50, choices = ROLE_CHOICES, blank = True)
    tertiary_role = models.CharField(max_length = 50, choices = ROLE_CHOICES, blank = True)
    gamers_club_level = models.IntegerField(null=True, blank=True)
    faceit_level = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_team_owner = models.BooleanField(default = False)