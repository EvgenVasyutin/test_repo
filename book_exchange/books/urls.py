from django.urls import path

from books.views import (
    index,
    register,
    logout_user,
    login_user,
    categories,
    category_detail,
    profile,
    book_create,
)

urlpatterns = [
    path('', view=index, name='index'),
    path('category/', view=categories, name='category'),
    path(
        'category_detail/<int:category_id>',
        view=category_detail,
        name='category_detail',
    ),
    path('create_book/', view=book_create, name='book_create'),
    path('profile/<int:user_id>', view=profile, name='profile'),
    path('register/', view=register, name='register'),
    path('login/', view=login_user, name='login'),
    path('logout/', view=logout_user, name='logout'),
]
