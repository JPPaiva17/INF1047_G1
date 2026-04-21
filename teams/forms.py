from django import forms
from .models import Team


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo', 'banner', 'description', 'training_schedule',
                  'min_faceit_level', 'min_gc_level', 'is_recruiting',
                  'trial_deadline', 'contact', 'instagram', 'youtube', 'website']

    def clean_min_gc_level(self):
        value = self.cleaned_data.get('min_gc_level')
        if value is not None and not (1 <= value <= 21):
            raise forms.ValidationError('O nível GC deve ser entre 1 e 21.')
        return value

    def clean_min_faceit_level(self):
        value = self.cleaned_data.get('min_faceit_level')
        if value is not None and not (1 <= value <= 10):
            raise forms.ValidationError('O nível Faceit deve ser entre 1 e 10.')
        return value
