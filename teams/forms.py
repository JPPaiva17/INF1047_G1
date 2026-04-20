from django import forms
from .models import Team


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo', 'banner', 'description', 'min_faceit_level', 'min_gc_level', 'is_recruiting']
