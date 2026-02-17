from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Sample data — replace with database queries once models are built
CATEGORIES = [
    {'name': 'Vegetables', 'icon': 'basket2', 'count': 45},
    {'name': 'Fruits', 'icon': 'apple', 'count': 32},
    {'name': 'Dairy & Eggs', 'icon': 'egg', 'count': 18},
    {'name': 'Bakery', 'icon': 'bread-slice', 'count': 24},
]

PRODUCTS = [
    {
        'name': 'Organic Mixed Veg Box',
        'producer': 'Severn Vale Farm',
        'price': '12.50',
        'category': 'Vegetables',
        'icon': 'basket2',
        'color': '#2d6a4f',
        'organic': True,
        'description': 'Seasonal selection of freshly harvested organic vegetables.',
    },
    {
        'name': 'Free-Range Eggs (dozen)',
        'producer': 'Chew Valley Hens',
        'price': '4.20',
        'category': 'Dairy & Eggs',
        'icon': 'egg',
        'color': '#e9c46a',
        'organic': True,
        'description': 'Free-range eggs from pasture-raised hens in Chew Valley.',
    },
    {
        'name': 'Sourdough Loaf',
        'producer': 'Hart\'s Bakery',
        'price': '3.80',
        'category': 'Bakery',
        'icon': 'bread-slice',
        'color': '#bc6c25',
        'organic': False,
        'description': 'Hand-crafted sourdough with a 48-hour ferment, baked fresh daily.',
    },
    {
        'name': 'Strawberry Punnet (400g)',
        'producer': 'Yanley Farm',
        'price': '3.50',
        'category': 'Fruits',
        'icon': 'apple',
        'color': '#e76f51',
        'organic': False,
        'description': 'Sweet Bristol-grown strawberries, picked at peak ripeness.',
    },
    {
        'name': 'Raw Organic Honey (340g)',
        'producer': 'Avon Apiaries',
        'price': '7.95',
        'category': 'Pantry',
        'icon': 'droplet-half',
        'color': '#e9a820',
        'organic': True,
        'description': 'Unprocessed wildflower honey from Bristol\'s urban beehives.',
    },
    {
        'name': 'Farmhouse Cheddar (300g)',
        'producer': 'Bath Soft Cheese Co.',
        'price': '5.60',
        'category': 'Dairy & Eggs',
        'icon': 'box',
        'color': '#f4a261',
        'organic': False,
        'description': 'Mature farmhouse cheddar aged for 12 months. Rich and crumbly.',
    },
    {
        'name': 'Heritage Tomatoes (500g)',
        'producer': 'Windmill Hill Farm',
        'price': '2.90',
        'category': 'Vegetables',
        'icon': 'basket2',
        'color': '#d62828',
        'organic': True,
        'description': 'Mixed heritage varieties — sweet, juicy, and full of flavour.',
    },
    {
        'name': 'Apple Juice (750ml)',
        'producer': 'Long Ashton Orchards',
        'price': '3.40',
        'category': 'Fruits',
        'icon': 'cup-straw',
        'color': '#606c38',
        'organic': False,
        'description': 'Pressed from a blend of Bramley and Cox apples, nothing added.',
    },
]

TEAM = [
    {'name': 'Rajib Ale', 'role': 'Full stack Developer', 'color': '#2d6a4f'},
    {'name': 'Thwin Htoo Aung','role': 'Full stack Developer', 'color': '#40916c'},
    {'name': 'Pio Antao', 'role': 'Full stack Developer', 'color': '#e76f51'},
    {'name': 'Saw Amos', 'role': 'Backend Engineer', 'color': '#bc6c25'},
]


def home(request):
    return render(request, 'marketplace/home.html', {
        'categories': CATEGORIES,
        'featured_products': PRODUCTS[:4],
    })


def products(request):
    return render(request, 'marketplace/products.html', {
        'products': PRODUCTS,
        'categories': CATEGORIES,
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
