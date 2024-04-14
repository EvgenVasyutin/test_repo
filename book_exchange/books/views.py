from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from books.models import Book, Category
from django.contrib.auth import authenticate, login, logout
from books.forms import SignUpForm
from django.contrib import messages


def index(request: HttpRequest) -> HttpResponse:
    all_books = Book.objects.all()
    context = {'books': all_books}
    return render(request, 'index.html', context)


def categories(request: HttpRequest) -> HttpResponse:
    all_categories = Category.objects.all()
    context = {'all_categories': all_categories}
    return render(request, 'categories.html', context)


def register(request: HttpRequest) -> HttpResponse:
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, ('Ви успішно зареєструвалися! Ласкаво просимо!')
            )
            return redirect('index')
    context = {'form': form}

    return render(request, 'register.html', context)


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Ви увійшли в систему!')
            return redirect('index')
        else:
            messages.success(
                request, ('Під час входу сталася помилка. Повторіть спробу..')
            )
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, ('Ви успішно вийшли з системи!'))
    return redirect('index')
