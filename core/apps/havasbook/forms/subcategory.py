from django import forms

from core.apps.havasbook.models import SubcategoryModel


class SubcategoryForm(forms.ModelForm):

    class Meta:
        model = SubcategoryModel
        fields = "__all__"
