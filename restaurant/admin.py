from django.contrib import admin
from .models import Category, MenuItem, Cart, CartItem, Order, OrderItem, UserProfile, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_featured', 'total_orders']
    list_filter = ['category', 'is_available', 'is_featured', 'is_vegetarian']
    list_editable = ['is_available', 'is_featured', 'price']
    search_fields = ['name', 'description']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method']
    list_editable = ['status', 'payment_status']
    search_fields = ['order_number', 'user__username']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'subtotal', 'delivery_fee', 'tax', 'total']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'rating', 'created_at']
    list_filter = ['rating']
