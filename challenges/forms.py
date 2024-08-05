# forms.py
from django import forms
from .models import ConfigHome, Challenge


class ConfigHomeForm(forms.ModelForm):
    class Meta:
        model = ConfigHome
        fields = ["title", "description", "banner"]

    def __init__(self, *args, **kwargs):
        super(ConfigHomeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ["title", "description", "secret_code", "is_free", "index"]
