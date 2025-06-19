from django import forms

from core.apps.havasbook.models import BrandModel


class BrandForm(forms.ModelForm):

    class Meta:
        model = BrandModel
        fields = "__all__"
