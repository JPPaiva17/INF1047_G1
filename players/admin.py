from django.contrib import admin
from django.contrib.auth.models import User
from .models import Players
from teams.models import TeamMember, Team


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0
    fk_name = 'player'


class OwnedTeamInline(admin.TabularInline):
    model = Team
    extra = 0
    fk_name = 'owner'
    fields = ['name']
    readonly_fields = ['name']
    can_delete = False
    verbose_name = 'Time que possui'


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_team_owner', 'looking_for_team']
    search_fields = ['user__username']
    inlines = [TeamMemberInline, OwnedTeamInline]
