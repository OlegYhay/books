from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet

from cart.cart import Cart
from cart.forms import CardAddProductForm
from .forms import ModelComment, ModelOrder
from .models import Book, CategoryBooks, Review, Order, OrderBooks
from .serializers import BookSerializer
from django.db.models import Q

from .service import send_mails
from .tasks import send_spam_email


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


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        result = Book.objects.filter(
            Q(title__icontains=query) | Q(title__icontains=query)
        )
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(SearchResultsListView, self).get_context_data(**kwargs)
        if len(data['book_list']) == 0:
            data['mistake'] = 'Ничего не найдено!'
        return data


class OrderCreate(CreateView):
    model = Order
    template_name = 'order/order_create.html'
    form_class = ModelOrder
    success_url = reverse_lazy('cart:created_order')

    # Установка user по текущему пользователю
    def form_valid(self, form):
        fields = form.save(commit=False)
        usermodel = get_user_model()
        fields.user = usermodel.objects.get(pk=self.request.user.pk)
        fields.save()
        cart = self.get_cart()
        booksic = cart['cart']
        for key, value in booksic.items():
            print(value)
            orderbooks = OrderBooks.objects.create(
                orderid=Order.objects.get(pk=fields.id),
                book=value['product'],
                count=value['quantity'],
                price=float(value['price']),
                summ=float(value['total_price']),
            )
            orderbooks.save()
        # delete cart
        cart = Cart(self.request)
        send_spam_email.delay(form.instance.email,fields.pk)
        cart.clean()
        return super().form_valid(form)

    def get_cart(self):
        cart = Cart(self.request)
        products_ids = cart.cart.keys()
        products = Book.objects.filter(id__in=products_ids)
        sum = 0
        for product in products:
            cart.cart[str(product.id)]['product'] = product
            cart.cart[str(product.id)]['total_price'] = float(cart.cart[str(product.id)]['quantity']) * float(
                cart.cart[str(product.id)]['price'])
            sum += cart.cart[str(product.id)]['total_price']
        return {'cart': cart.cart, 'itogsumm': sum}

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        products_ids = cart.cart.keys()
        products = Book.objects.filter(id__in=products_ids)
        sum = 0
        info = self.get_cart()
        data['cart'] = info['cart']
        data['itogsumm'] = info['itogsumm']
        return data


class OrderCreated(TemplateView):
    template_name = 'order/success.html'
