from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from books.models import Book


def index(request: HttpRequest) -> HttpResponse:
    all_books = Book.objects.all()
    context = {'books': all_books}
    return render(request, 'index.html', context)
