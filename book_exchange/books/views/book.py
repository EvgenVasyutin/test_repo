from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from books.models import Book
from books.forms import BookForm, PictureForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request: HttpRequest) -> HttpResponse:
    all_books = Book.objects.all()
    context = {'books': all_books}
    return render(request, 'index.html', context)


@login_required()
def book_create(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    book_form = BookForm(request.POST or None)
    pic_form = PictureForm(request.POST, request.FILES)
    if request.method == 'POST':
        if book_form.is_valid() and pic_form.is_valid():
            pic = pic_form.save()
            pic.save()
            book = book_form.save(commit=False)
            book.owner = request.user
            book.picture = pic
            book.save()
            messages.success(
                request,
                ('Ви успішно створили книгу на обмін!'),
            )
            return redirect('profile', request.user.id)
    else:
        book_form = BookForm()
        pic_form = PictureForm()
    context = {'book_form': book_form, 'pic_form': pic_form}
    return render(request, 'book_create.html', context)


@login_required()
def book_delete(
    request: HttpRequest, book_id: int
) -> HttpResponse | HttpResponseRedirect:
    book = Book.objects.get(pk=book_id)
    if request.user.id == book.owner.id:
        book.delete()
        messages.success(request, ('Книга успішно видалена!'))
        return redirect('profile', request.user.id)
    else:
        messages.success(
            request, ('Ви не можете видалити книгу іншого користувача!')
        )
        return redirect('profile', request.user.id)
