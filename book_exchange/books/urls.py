from django.urls import path
from . import views

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
)
from django.urls import path

from books.views import index, register, logout_user, login_user, categories

urlpatterns = [
    path('', view=index, name='index'),
    path('category/', view=categories, name='category'),
    path('register/', view=register, name='register'),
    path('login/', view=login_user, name='login'),
    path('logout/', view=logout_user, name='logout'),
]
