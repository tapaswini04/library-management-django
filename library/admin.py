from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'author',
        'category',
        'price',
        'is_borrowed',
        'borrowed_by',
        'borrowed_date',
    )

    list_filter = (
        'category',
        'is_borrowed',
    )

    search_fields = (
        'title',
        'author',
    )