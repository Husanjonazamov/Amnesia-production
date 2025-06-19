from django import forms

from core.apps.havasbook.models import GenderModel


class GenderForm(forms.ModelForm):

    class Meta:
        model = GenderModel
        fields = "__all__"
