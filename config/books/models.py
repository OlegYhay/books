import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import CustomUser


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


# 14.08.2022
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'Новый'
        Paid = 'Оплачено'
        Accepted = 'Принят'
        OnTheWay = 'В пути'
        Delivered = 'Доставлен'

    name = models.CharField(max_length=100, verbose_name='Имя')
    secondname = models.CharField(max_length=100, verbose_name='Фамилия')
    numberphone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')
    fulladdress = models.CharField(max_length=255, verbose_name='Область(республика),город,улица,дом,квартира,индекс:')
    notification = models.BooleanField(verbose_name='СМС уведомление о статусе заказа', default=False)
    Payment = models.ForeignKey('Paymentmethod', on_delete=models.SET_NULL, null=True, verbose_name='Способ оплаты')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Покупатель', blank=True)
    status = models.CharField(max_length=255, default=OrderStatus.NEW, choices=OrderStatus.choices)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        return f'{self.name} {self.secondname}  {self.status}'


class OrderBooks(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='books')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name='Книга')
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    summ = models.PositiveIntegerField(default=0, verbose_name='Сумма')


class Paymentmethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
