# -*- coding: utf-8 -*-
import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from django.conf import settings
from players.models import Players
from teams.models import Team, TeamMember

BASE_DIR = settings.BASE_DIR
STATIC_IMAGES = BASE_DIR / 'static' / 'images'
MEDIA_TEAMS = BASE_DIR / 'media' / 'teams'
MEDIA_LOGOS = MEDIA_TEAMS / 'logos'
MEDIA_BANNERS = MEDIA_TEAMS / 'banners'
MEDIA_AVATARS = BASE_DIR / 'media' / 'avatars'

for folder in [MEDIA_LOGOS, MEDIA_BANNERS, MEDIA_AVATARS]:
    folder.mkdir(parents=True, exist_ok=True)

shutil.copy(STATIC_IMAGES / 'team_logo.png', MEDIA_LOGOS / 'team_logo.png')
shutil.copy(STATIC_IMAGES / 'team_background.png', MEDIA_BANNERS / 'team_background.png')
shutil.copy(STATIC_IMAGES / 'profilepic.png', MEDIA_AVATARS / 'profilepic.png')

players_data = [
    {'username': 'raalz',   'faceit': 10, 'gc': 21, 'role': 'rifler'},
    {'username': 'kraghen', 'faceit': 10, 'gc': 20, 'role': 'awper'},
    {'username': 'bnox',    'faceit': 10, 'gc': 19, 'role': 'entry_fragger'},
    {'username': 'flayy',   'faceit': 10, 'gc': 18, 'role': 'support'},
    {'username': 'cej0t',   'faceit': 10, 'gc': 17, 'role': 'in_game_leader'},
]

owner_data = players_data[0]

created_players = []
for p in players_data:
    user, _ = User.objects.get_or_create(username=p['username'])
    user.set_password('senha123')
    user.save()
    player = user.player
    player.faceit_level = p['faceit']
    player.gamers_club_level = p['gc']
    player.primary_role = p['role']
    player.avatar = 'avatars/profilepic.png'
    player.is_team_owner = (p['username'] == owner_data['username'])
    player.save()
    created_players.append((player, p['role']))

owner_player = created_players[0][0]

team, created = Team.objects.get_or_create(
    name='9ine',
    defaults={
        'description': 'Equipe competitiva de CS2 buscando jogadores dedicados para disputar torneios nacionais.',
        'logo': 'teams/logos/team_logo.png',
        'banner': 'teams/banners/team_background.png',
        'owner': owner_player,
        'training_schedule': 'Segunda, Quarta e Sexta — 20h às 22h',
        'min_faceit_level': 8,
        'min_gc_level': 15,
        'is_recruiting': True,
    }
)

if created:
    for player, role in created_players:
        TeamMember.objects.get_or_create(team=team, player=player, defaults={'role': role})
    print('Time 9ine criado com sucesso!')
else:
    print('Time 9ine já existe.')
