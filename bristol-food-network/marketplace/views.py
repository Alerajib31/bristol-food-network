from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from django.db.models import Count

from .models import Category, Product, CustomerProfile, Cart, CartItem
from .forms import CustomerRegistrationForm

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


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    return render(request, 'marketplace/product_detail.html', {'product': product})


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
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')
            user.save()
            CustomerProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
                delivery_address=form.cleaned_data.get('delivery_address', ''),
                postcode=form.cleaned_data.get('postcode', ''),
            )
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Bristol Food Network.')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'marketplace/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ── Cart views ────────────────────────────────────────────────────────────────

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cart_items.select_related('product__producer')
    return render(request, 'marketplace/cart.html', {'cart': cart, 'items': items})


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'"{product.name}" added to your basket.')
    next_url = request.POST.get('next', 'products')
    return redirect(next_url)


@login_required
@require_POST
def update_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f'"{name}" removed from your basket.')
    return redirect('cart')
