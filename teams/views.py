from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Team, TeamMember
from .forms import TeamCreateForm


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    players = team.members.exclude(role='coach').select_related('player__user')
    coach = team.members.filter(role='coach').select_related('player__user').first()
    return render(request, 'app/team_detail.html', {'team': team, 'players': players, 'coach': coach})


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
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamCreateForm()

    return render(request, 'app/team_create.html', {'form': form})


@login_required
def team_list(request):
    query = request.GET.get('q', '')
    teams = Team.objects.all()
    if query:
        teams = teams.filter(name__icontains=query)
    featured = Team.objects.order_by('-created_at')[:4]
    return render(request, 'app/teams_list.html', {'teams': teams, 'featured': featured, 'query': query})
