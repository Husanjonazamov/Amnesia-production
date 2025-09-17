from django import forms

from core.apps.havasbook.models import ChildcategoryModel


class ChildcategoryForm(forms.ModelForm):

    class Meta:
        model = ChildcategoryModel
        fields = "__all__"
