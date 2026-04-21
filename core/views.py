from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teams.models import TeamInvite

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    player = request.user.player
    received_invites = player.invites_received.filter(status='pending').select_related('team')
    sent_invites = None
    pending_requests = None
    if player.is_team_owner:
        sent_invites = player.owned_team.invites.filter(status='pending').select_related('player__user')
        pending_requests = player.owned_team.join_requests.filter(status='pending').select_related('player__user')
    return render(request, 'app/dashboard.html', {
        'received_invites': received_invites,
        'sent_invites': sent_invites,
        'pending_requests': pending_requests,
    })
