from django.urls import path
from .views import HomePageView, AboutPageView, GenrePageView, MyOrderListView, MyOrderDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('books/category/<str:genre>/', GenrePageView.as_view(), name='genre'),
    path('my_orders/', MyOrderListView.as_view(), name='my_orders'),
    path('my_orders/<int:pk>/', MyOrderDetailView.as_view(), name='order_detail'),
]
