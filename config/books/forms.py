from django import forms
from django.contrib.auth import get_user_model

from .models import Review, Order
from crispy_forms.helper import FormHelper


class ModelComment(forms.ModelForm):
    helper = FormHelper

    class Meta:
        model = Review
        fields = ['review']


class ModelOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    user = forms.ModelChoiceField(widget=forms.HiddenInput(), required=False,queryset=get_user_model().objects.all())
    status = forms.CharField(widget=forms.HiddenInput(), required=False)
