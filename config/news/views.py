from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from .models import Article


class ArticleView(ListView):
    model = Article
    template_name = 'news/news_list.html'
    context_object_name = 'articles'