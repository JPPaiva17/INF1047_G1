from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Team, TeamMember, TeamInvite, TeamRequest
from .forms import TeamCreateForm
from players.models import Players
from players.constants import ROLE_CHOICES


@login_required
def team_list(request):
    query = request.GET.get('q', '')
    teams = Team.objects.all()
    if query:
        teams = teams.filter(name__icontains=query)
    featured = Team.objects.order_by('-created_at')[:4]
    return render(request, 'app/teams_list.html', {'teams': teams, 'featured': featured, 'query': query})


@login_required
def team_create(request):
    player = request.user.player
    if hasattr(player, 'owned_team'):
        return redirect('team_detail', pk=player.owned_team.pk)

    if request.method == 'POST':
        form = TeamCreateForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = player
            team.save()
            player.is_team_owner = True
            player.save(update_fields=['is_team_owner'])
            return redirect('team_manage', pk=team.pk)
    else:
        form = TeamCreateForm()

    return render(request, 'app/team_create.html', {'form': form})


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = team.members.exclude(role='coach').select_related('player__user')
    coach = team.members.filter(role='coach').select_related('player__user').first()

    current_player = request.user.player
    is_owner = hasattr(current_player, 'owned_team') and current_player.owned_team == team
    is_member = team.members.filter(player=current_player).exists()
    has_any_team = current_player.team_memberships.exists() or current_player.is_team_owner
    can_request = not is_owner and not has_any_team
    has_pending_request = team.join_requests.filter(player=current_player, status='pending').exists()

    return render(request, 'app/team_detail.html', {
        'team': team,
        'players': members,
        'coach': coach,
        'is_owner': is_owner,
        'is_member': is_member,
        'can_request': can_request,
        'has_pending_request': has_pending_request,
        'role_choices': ROLE_CHOICES,
    })


@login_required
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk)
    player = request.user.player

    if not hasattr(player, 'owned_team') or player.owned_team != team:
        return redirect('team_detail', pk=pk)

    if request.method == 'POST':
        form = TeamCreateForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()

    return redirect('team_manage', pk=pk)


@login_required
def team_delete_confirm(request, pk):
    team = get_object_or_404(Team, pk=pk)
    player = request.user.player
    if not hasattr(player, 'owned_team') or player.owned_team != team:
        return redirect('team_list')
    return render(request, 'app/team_delete_confirm.html', {'team': team})


@login_required
def team_delete(request, pk):
    if request.method != 'POST':
        return redirect('team_manage', pk=pk)

    team = get_object_or_404(Team, pk=pk)
    player = request.user.player

    if not hasattr(player, 'owned_team') or player.owned_team != team:
        return redirect('team_list')

    player.is_team_owner = False
    player.save(update_fields=['is_team_owner'])
    team.delete()

    return redirect('team_list')


@login_required
def team_manage(request, pk):
    team = get_object_or_404(Team, pk=pk)
    player = request.user.player

    if not hasattr(player, 'owned_team') or player.owned_team != team:
        return redirect('team_detail', pk=pk)

    pending_requests = team.join_requests.filter(status='pending').select_related('player__user')
    pending_invites = team.invites.filter(status='pending').select_related('player__user')
    members = team.members.select_related('player__user')

    owner_membership = team.members.filter(player=player).first()

    return render(request, 'app/team_manage.html', {
        'team': team,
        'form': TeamCreateForm(instance=team),
        'pending_requests': pending_requests,
        'pending_invites': pending_invites,
        'members': members,
        'owner_membership': owner_membership,
        'role_choices': ROLE_CHOICES,
    })


@login_required
def owner_set_role(request, pk):
    if request.method != 'POST':
        return redirect('team_manage', pk=pk)

    team = get_object_or_404(Team, pk=pk)
    player = request.user.player

    if not hasattr(player, 'owned_team') or player.owned_team != team:
        return redirect('team_manage', pk=pk)

    role = request.POST.get('role', '')
    TeamMember.objects.filter(team=team, player=player).delete()
    if role:
        non_coaches = team.members.exclude(role='coach').count()
        coaches = team.members.filter(role='coach').count()
        full = (role == 'coach' and coaches >= 1) or (role != 'coach' and non_coaches >= 5)
        if not full:
            TeamMember.objects.create(team=team, player=player, role=role)

    return redirect('team_manage', pk=pk)


@login_required
def invite_player(request, player_pk):
    if request.method != 'POST':
        return redirect('players_list')

    owner_player = request.user.player
    if not owner_player.is_team_owner:
        return redirect('players_list')

    team = owner_player.owned_team
    target = get_object_or_404(Players, pk=player_pk)
    role = request.POST.get('role', 'rifler')

    if target != owner_player and not team.members.filter(player=target).exists():
        TeamInvite.objects.update_or_create(
            team=team,
            player=target,
            defaults={'role': role, 'status': 'pending'},
        )

    return redirect('players_list')


@login_required
def respond_invite(request, invite_pk):
    if request.method != 'POST':
        return redirect('my_invites')

    invite = get_object_or_404(TeamInvite, pk=invite_pk, player=request.user.player)
    if invite.status != 'pending':
        return redirect('my_invites')

    action = request.POST.get('action')
    if action == 'accept':
        team = invite.team
        non_coaches = team.members.exclude(role='coach').count()
        coaches = team.members.filter(role='coach').count()
        full = (invite.role == 'coach' and coaches >= 1) or (invite.role != 'coach' and non_coaches >= 5)
        if not full:
            TeamMember.objects.create(team=team, player=invite.player, role=invite.role)
            invite.player.looking_for_team = False
            invite.player.save(update_fields=['looking_for_team'])
            TeamInvite.objects.filter(player=invite.player, status='pending').exclude(pk=invite.pk).update(status='declined')
            invite.status = 'accepted'
        else:
            invite.status = 'declined'
        invite.save()
    elif action == 'decline':
        invite.status = 'declined'
        invite.save()

    return redirect('dashboard')


@login_required
def my_invites(request):
    player = request.user.player
    pending = player.invites_received.filter(status='pending').select_related('team')
    past = player.invites_received.exclude(status='pending').select_related('team').order_by('-created_at')[:10]
    return render(request, 'app/my_invites.html', {'pending_invites': pending, 'past_invites': past})


@login_required
def request_join(request, team_pk):
    if request.method != 'POST':
        return redirect('team_detail', pk=team_pk)

    team = get_object_or_404(Team, pk=team_pk)
    player = request.user.player
    role = request.POST.get('role', 'rifler')

    if not player.is_team_owner and not player.team_memberships.exists():
        TeamRequest.objects.update_or_create(
            team=team,
            player=player,
            defaults={'role': role, 'status': 'pending'},
        )

    return redirect('team_detail', pk=team_pk)


@login_required
def respond_request(request, req_pk):
    if request.method != 'POST':
        return redirect('team_list')

    req = get_object_or_404(TeamRequest, pk=req_pk)
    owner_player = request.user.player

    if not hasattr(owner_player, 'owned_team') or owner_player.owned_team != req.team:
        return redirect('team_list')

    if req.status != 'pending':
        return redirect('team_manage', pk=req.team.pk)

    action = request.POST.get('action')
    if action == 'accept':
        team = req.team
        non_coaches = team.members.exclude(role='coach').count()
        coaches = team.members.filter(role='coach').count()
        full = (req.role == 'coach' and coaches >= 1) or (req.role != 'coach' and non_coaches >= 5)
        if not full:
            TeamMember.objects.create(team=team, player=req.player, role=req.role)
            req.player.looking_for_team = False
            req.player.save(update_fields=['looking_for_team'])
            TeamRequest.objects.filter(player=req.player, status='pending').exclude(pk=req.pk).update(status='declined')
            req.status = 'accepted'
        else:
            req.status = 'declined'
    elif action == 'decline':
        req.status = 'declined'

    req.save()
    return redirect('team_manage', pk=req.team.pk)


@login_required
def cancel_invite(request, invite_pk):
    if request.method != 'POST':
        return redirect('team_manage', pk=0)

    invite = get_object_or_404(TeamInvite, pk=invite_pk)
    owner_player = request.user.player

    if hasattr(owner_player, 'owned_team') and owner_player.owned_team == invite.team:
        invite.status = 'declined'
        invite.save()

    next_url = request.POST.get('next', '')
    if next_url == 'dashboard':
        return redirect('dashboard')
    return redirect('team_manage', pk=invite.team.pk)
