from django.contrib import admin
from .models import Book, Category, Picture, Author, Exchange

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(Author)
admin.site.register(Exchange)