from django import forms

from .models import Review
from crispy_forms.helper import FormHelper


class ModelComment(forms.ModelForm):
    helper = FormHelper

    class Meta:
        model = Review
        fields = ['review']
