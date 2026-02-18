from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from django.db.models import Count

from .models import Category, Product

TEAM = [
    {'name': 'Rajib Ale', 'role': 'Full stack Developer', 'color': '#2d6a4f'},
    {'name': 'Thwin Htoo Aung', 'role': 'Full stack Developer', 'color': '#40916c'},
    {'name': 'Pio Antao', 'role': 'Full stack Developer', 'color': '#e76f51'},
    {'name': 'Saw Amos', 'role': 'Backend Engineer', 'color': '#bc6c25'},
]


def home(request):
    products = Product.objects.filter(is_active=True).select_related('producer', 'category')
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'marketplace/home.html', {
        'categories': categories,
        'featured_products': products[:4],
    })


def products(request):
    all_products = Product.objects.filter(is_active=True).select_related('producer', 'category')
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'marketplace/products.html', {
        'products': all_products,
        'categories': categories,
    })


def about(request):
    return render(request, 'marketplace/about.html', {
        'team': TEAM,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'marketplace/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Bristol Food Network.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'marketplace/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
