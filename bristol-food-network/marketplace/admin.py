from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Category, Producer, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'email', 'user']
    search_fields = ['name', 'location']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'producer', 'category', 'price', 'stock', 'organic', 'is_active']
    list_filter = ['category', 'organic', 'is_active']
    search_fields = ['name', 'producer__name']
    list_editable = ['price', 'stock', 'is_active']


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at', 'total']
    inlines = [OrderItemInline]
