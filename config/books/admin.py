from django.contrib import admin

# Register your models here.
from .models import Book, Review, CategoryBooks, Author


class ReviewInLine(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInLine,
    ]

    list_display = ("title", 'author', 'price')


admin.site.register(Book, BookAdmin)
admin.site.register(CategoryBooks)
admin.site.register(Author)
admin.site.register(Review)
