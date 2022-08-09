from rest_framework import serializers
from rest_framework import  mixins , generics
from rest_framework.viewsets import ModelViewSet

from .models import Book


class BookSerializer(ModelViewSet):
    class Meta:
        model = Book
        fields = '__all__'
