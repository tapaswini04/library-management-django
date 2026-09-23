from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'books/',
        views.book_list,
        name='book_list'
    ),

    path(
        'books/add/',
        views.add_book,
        name='add_book'
    ),

    path(
        'books/edit/<int:id>/',
        views.edit_book,
        name='edit_book'
    ),

    path(
        'books/delete/<int:id>/',
        views.delete_book,
        name='delete_book'
    ),

    path(
        'books/detail/<int:id>/',
        views.book_detail,
        name='book_detail'
    ),

    path(
        'books/borrow/<int:id>/',
        views.borrow_book,
        name='borrow_book'
    ),

    path(
        'books/return/<int:id>/',
        views.return_book,
        name='return_book'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
]