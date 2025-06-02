from django import forms

from core.apps.havasbook.models import OrganizationModel


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = OrganizationModel
        fields = "__all__"
