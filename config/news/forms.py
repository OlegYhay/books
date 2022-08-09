from django import forms
from crispy_forms.helper import FormHelper

from news.models import Article


class ArticleForm(forms.ModelForm):
    helper = FormHelper

    class Meta:
        model = Article
        fields = '__all__'
