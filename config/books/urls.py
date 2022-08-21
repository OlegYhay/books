from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BookListView, BookDetailView, BookCreateView, CommentViewSet, SearchResultsListView, OrderCreate

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('book/<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]
