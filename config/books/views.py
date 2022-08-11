from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet

from cart.forms import CardAddProductForm
from .forms import ModelComment
from .models import Book, CategoryBooks, Review
from .serializers import BookSerializer


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['categories'] = CategoryBooks.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    cart_product_form = CardAddProductForm()

    def get_object(self, queryset=None):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Book.objects.filter(pk=pk)[0]
        return instance

    def get_context_data(self, **kwargs):
        data = super(BookDetailView, self).get_context_data(**kwargs)
        data['categories'] = CategoryBooks.objects.all()
        data['product'] = Book.objects.filter(pk=self.kwargs.get('pk'))
        data['cart_product_form'] = self.cart_product_form
        if self.request.user.is_authenticated:
            data['reviews_form'] = ModelComment(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            new_comment = Review(
                review=request.POST.get('review'),
                author=self.request.user,
                book=self.get_object(),
            )
            new_comment.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    template_name = 'books/book_create.html'
    fields = '__all__'
    success_url = reverse_lazy('book_list')
    login_url = 'account_login'

    permission_required = 'config.books.special_status'


# it's don't use
class CommentViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Review.objects.all()

    def get_serializer_context(self):
        return super(CommentViewSet, self).get_serializer_context(self)
