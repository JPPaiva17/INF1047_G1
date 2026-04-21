from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Players

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords don't match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This Username already exists!")
            return redirect('register')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "This email is already in use!")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, "Account created succesfully!")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
 
        user = authenticate(request, username=username, password=password)
 
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password incorrects.')
            return redirect('login')
 
    return render(request, 'login.html')
 
 
def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    return render(request, 'forgot.html')


@login_required
def players_list_view(request):
    players = Players.objects.filter(looking_for_team=True).select_related('user')
    context = {'players': players}
    current_player = request.user.player
    if current_player.is_team_owner:
        team = current_player.owned_team
        context['is_team_owner'] = True
        context['invited_ids'] = set(team.invites.filter(status='pending').values_list('player_id', flat=True))
        context['member_ids'] = set(team.members.values_list('player_id', flat=True))
    return render(request, 'app/players.html', context)


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    player = get_object_or_404(Players, user=profile_user)
    is_owner = request.user.is_authenticated and request.user == profile_user
    owned_team = getattr(player, 'owned_team', None)
    member_team = player.team_memberships.select_related('team').first()
    return render(request, 'app/profile.html', {
        'profile_user': profile_user,
        'player': player,
        'is_owner': is_owner,
        'owned_team': owned_team,
        'member_team': member_team,
    })


@login_required
def profile_edit_view(request):
    player = get_object_or_404(Players, user=request.user)
    if request.method == 'POST':
        player.bio = request.POST.get('bio', '')
        player.primary_role = request.POST.get('primary_role', '')
        player.secondary_role = request.POST.get('secondary_role', '')
        player.tertiary_role = request.POST.get('tertiary_role', '')
        player.gamers_club_level = request.POST.get('gamers_club_level') or None
        player.faceit_level = request.POST.get('faceit_level') or None
        player.instagram = request.POST.get('instagram', '')
        player.youtube = request.POST.get('youtube', '')
        player.steam = request.POST.get('steam', '')
        player.looking_for_team = 'looking_for_team' in request.POST
        if 'avatar' in request.FILES:
            player.avatar = request.FILES['avatar']
        if 'banner' in request.FILES:
            player.banner = request.FILES['banner']
        player.save()
        return redirect('profile', username=request.user.username)
    from .constants import ROLE_CHOICES
    return render(request, 'app/profile_edit.html', {
        'player': player,
        'role_choices': ROLE_CHOICES,
    })