from django.urls import path
from .views import HomePageView, AboutPageView, GenrePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('books/category/<str:genre>/', GenrePageView.as_view(),name='genre')
]
