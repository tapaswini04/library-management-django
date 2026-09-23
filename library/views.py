from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.utils import timezone

from .models import Book


def home(request):
    return redirect('login')


# ---------------- SIGN UP ----------------

def signup(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = UserCreationForm()

    return render(
        request,
        'library/signup.html',
        {'form': form}
    )


# ---------------- LOGIN ----------------

def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('dashboard')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'library/login.html',
        {'form': form}
    )


# ---------------- DASHBOARD ----------------

@login_required
def dashboard(request):

    books = Book.objects.all()

    total_books = books.count()

    available_books = books.filter(
        is_borrowed=False
    ).count()

    borrowed_books = books.filter(
        is_borrowed=True
    ).count()

    total_categories = books.values(
        'category'
    ).distinct().count()

    average_price = books.aggregate(
        Avg('price')
    )['price__avg']

    if average_price is None:
        average_price = 0

    return render(
        request,
        'library/dashboard.html',
        {
            'books': books,
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_categories': total_categories,
            'average_price': round(average_price, 2),
        }
    )


# ---------------- BOOK LIST + SEARCH ----------------

@login_required
def book_list(request):

    books = Book.objects.all()

    search = request.GET.get(
        'search',
        ''
    )

    category = request.GET.get(
        'category',
        ''
    )

    if search:

        books = books.filter(
            title__icontains=search
        ) | books.filter(
            author__icontains=search
        )

    if category:

        books = books.filter(
            category=category
        )

    categories = Book.objects.values_list(
        'category',
        flat=True
    ).distinct()

    return render(
        request,
        'library/book_list.html',
        {
            'books': books,
            'categories': categories,
            'search': search,
            'selected_category': category,
        }
    )


# ---------------- ADD BOOK ----------------

@login_required
def add_book(request):

    if request.method == 'POST':

        Book.objects.create(

            title=request.POST.get('title'),

            author=request.POST.get('author'),

            category=request.POST.get('category'),

            price=request.POST.get('price')
        )

        return redirect('book_list')

    return render(
        request,
        'library/add_book.html'
    )


# ---------------- EDIT BOOK ----------------

@login_required
def edit_book(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    if request.method == 'POST':

        book.title = request.POST.get(
            'title'
        )

        book.author = request.POST.get(
            'author'
        )

        book.category = request.POST.get(
            'category'
        )

        book.price = request.POST.get(
            'price'
        )

        book.save()

        return redirect('book_list')

    return render(
        request,
        'library/edit_book.html',
        {'book': book}
    )


# ---------------- DELETE BOOK ----------------

@login_required
def delete_book(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    book.delete()

    return redirect('book_list')


# ---------------- BOOK DETAILS ----------------

@login_required
def book_detail(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    return render(
        request,
        'library/book_detail.html',
        {'book': book}
    )


# ---------------- BORROW BOOK ----------------

@login_required
def borrow_book(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    if not book.is_borrowed:

        book.is_borrowed = True

        book.borrowed_by = request.user

        book.borrowed_date = timezone.now().date()

        book.save()

    return redirect(
        'book_list'
    )


# ---------------- RETURN BOOK ----------------

@login_required
def return_book(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    book.is_borrowed = False

    book.borrowed_by = None

    book.borrowed_date = None

    book.save()

    return redirect(
        'book_list'
    )


# ---------------- LOGOUT ----------------

def logout_view(request):

    logout(request)

    return redirect('login')