import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.urls import reverse


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='covers/', blank=True)
    category = models.ForeignKey("CategoryBooks", default='', null=True, on_delete=models.SET_DEFAULT)
    description = models.TextField(default='without decription', null=True)
    agecontrol = models.CharField(default='0+', null=True, max_length=20)
    copyright = models.CharField(max_length=200, default='', null=True)
    ISBN = models.CharField(max_length=33, default='', null=True)
    ispopular = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('special_status', 'Can read all books'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': str(self.pk)})


class Author(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    review = models.CharField(max_length=255, verbose_name='Комментарий')
    date = models.DateTimeField(verbose_name='Дата', auto_now=True)

    def __str__(self):
        return self.review


class CategoryBooks(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
