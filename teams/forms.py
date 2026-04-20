from django import forms
from .models import Team


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo', 'banner', 'description', 'training_schedule',
                  'min_faceit_level', 'min_gc_level', 'is_recruiting',
                  'trial_deadline', 'contact', 'instagram', 'youtube', 'website']
