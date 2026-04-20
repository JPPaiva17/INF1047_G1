from django.db import models
from players.constants import ROLE_CHOICES
from django.contrib.auth.models import User

class Players(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    primary_role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    secondary_role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    tertiary_role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    gamers_club_level = models.IntegerField(null=True, blank=True)
    faceit_level = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    steam = models.URLField(blank=True)
    looking_for_team = models.BooleanField(default=True)
    is_team_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username