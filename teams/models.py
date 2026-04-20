from django.db import models
from django.core.exceptions import ValidationError
from players.models import Players
from players.constants import ROLE_CHOICES


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='teams/logos/', null=True, blank=True)
    banner = models.ImageField(upload_to='teams/banners/', null=True, blank=True)
    owner = models.OneToOneField(Players, on_delete=models.CASCADE, related_name='owned_team')
    training_schedule = models.TextField(blank=True)
    min_faceit_level = models.IntegerField(null=True, blank=True)
    min_gc_level = models.IntegerField(null=True, blank=True)
    is_recruiting = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    player = models.ForeignKey(Players, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('team', 'player')

    def clean(self):
        coaches = self.team.members.filter(role='coach').exclude(pk=self.pk).count()
        non_coaches = self.team.members.exclude(role='coach').exclude(pk=self.pk).count()

        if self.role == 'coach' and coaches >= 1:
            raise ValidationError('A team can only have 1 coach.')
        if self.role != 'coach' and non_coaches >= 5:
            raise ValidationError('A team can only have 5 players.')

    def __str__(self):
        return f'{self.player} - {self.team} ({self.role})'
