from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView

from books.models import Book, CategoryBooks


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.all()[:6]
        context['categories'] = CategoryBooks.objects.all()
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'


class GenrePageView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super(GenrePageView, self).get_context_data(**kwargs)
        context['categories'] = CategoryBooks.objects.all()
        return context

    def get_queryset(self):
        categoryB = CategoryBooks.objects.get(name=self.kwargs['genre'])
        return Book.objects.filter(category=categoryB)
