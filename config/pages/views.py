from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from books.models import Book, CategoryBooks, Order, OrderBooks
from news.models import Article


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        books = Book.objects.filter(ispopular=True)
        context['books'] = books
        context['categories'] = CategoryBooks.objects.all()
        lastarticles = Article.objects.order_by('-date')[:3]
        context['articles'] = lastarticles
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


class MyOrderListView(LoginRequiredMixin, ListView):
    template_name = 'order/my_orders.html'
    context_object_name = 'orders'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyOrderListView, self).get_context_data(**kwargs)
        context['mistake'] = ''
        if Order.objects.filter(user=self.request.user).count() == 0:
            print('mistake')
            context['mistake'] = 'У вас нет заказов.'
        return context

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return orders


class MyOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MyOrderDetailView, self).get_context_data(**kwargs)
        context['books'] = OrderBooks.objects.filter(orderid=self.object.pk)
        sum = 0
        for i in context['books']:
            sum += i.summ
        context['summ'] = sum

        return context
