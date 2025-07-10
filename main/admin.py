from django.contrib import admin
from .models import Book, Cart, CartItem

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'published_date')
    search_fields = ('title', 'author')
