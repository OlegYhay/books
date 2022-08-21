from django.contrib import admin

# Register your models here.
from .models import Book, Review, CategoryBooks, Author, Order, OrderBooks, Paymentmethod


class ReviewInLine(admin.TabularInline):
    model = Review


class OrderInLine(admin.TabularInline):
    model = OrderBooks


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderInLine,
    ]


class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInLine,
    ]

    list_display = ("title", 'author', 'price')


admin.site.register(Order, OrderAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(CategoryBooks)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Paymentmethod)
admin.site.register(OrderBooks)
