from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
import json

from .models import Category, MenuItem, Cart, CartItem, Order, OrderItem, UserProfile, Review
from .forms import RegisterForm, UserProfileForm, CheckoutForm, ReviewForm


def home(request):
    categories = Category.objects.all()
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:8]
    popular_items = MenuItem.objects.filter(is_available=True).order_by('-total_orders')[:6]
    context = {
        'categories': categories,
        'featured_items': featured_items,
        'popular_items': popular_items,
    }
    return render(request, 'restaurant/home.html', context)


def menu(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    filter_veg = request.GET.get('veg')
    filter_spicy = request.GET.get('spicy')

    items = MenuItem.objects.filter(is_available=True)

    if category_slug:
        items = items.filter(category__slug=category_slug)
    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    if filter_veg:
        items = items.filter(is_vegetarian=True)
    if filter_spicy:
        items = items.filter(is_spicy=True)

    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()

    context = {
        'categories': categories,
        'items': items,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'restaurant/menu.html', context)


def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, is_available=True)
    related_items = MenuItem.objects.filter(category=item.category, is_available=True).exclude(pk=pk)[:4]
    reviews = item.reviews.all()
    review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.menu_item = item
            review.save()
            messages.success(request, 'Review submitted!')
            return redirect('item_detail', pk=pk)

    context = {
        'item': item,
        'related_items': related_items,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'restaurant/item_detail.html', context)


@login_required
def cart(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'restaurant/cart.html', {'cart': cart_obj})


@login_required
@require_POST
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, menu_item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{item.name} added to cart!',
            'cart_count': cart_obj.total_items,
        })
    messages.success(request, f'{item.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'menu'))


@login_required
@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 1))

    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    cart_obj = Cart.objects.get(user=request.user)
    return JsonResponse({
        'success': True,
        'subtotal': float(cart_item.subtotal) if quantity > 0 else 0,
        'cart_total': float(cart_obj.total_price),
        'cart_count': cart_obj.total_items,
    })


@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    cart_obj = Cart.objects.get(user=request.user)
    return JsonResponse({
        'success': True,
        'cart_total': float(cart_obj.total_price),
        'cart_count': cart_obj.total_items,
    })


@login_required
def checkout(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)

    if not cart_obj.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    profile = getattr(request.user, 'profile', None)
    initial_data = {}
    if profile:
        initial_data = {
            'delivery_address': profile.address,
            'delivery_city': profile.city,
            'delivery_zip': profile.zip_code,
            'phone': profile.phone,
        }

    form = CheckoutForm(initial=initial_data)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            subtotal = cart_obj.total_price
            delivery_fee = Decimal('3.99')
            tax = subtotal * Decimal('0.08')
            total = subtotal + delivery_fee + tax

            order = Order.objects.create(
                user=request.user,
                delivery_address=form.cleaned_data['delivery_address'],
                delivery_city=form.cleaned_data['delivery_city'],
                delivery_zip=form.cleaned_data['delivery_zip'],
                phone=form.cleaned_data['phone'],
                payment_method=form.cleaned_data['payment_method'],
                special_instructions=form.cleaned_data.get('special_instructions', ''),
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                tax=tax,
                total=total,
                estimated_delivery=timezone.now() + timezone.timedelta(minutes=45),
            )

            for cart_item in cart_obj.items.all():
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity,
                    price=cart_item.menu_item.price,
                )
                cart_item.menu_item.total_orders += cart_item.quantity
                cart_item.menu_item.save()

            cart_obj.items.all().delete()
            messages.success(request, f'Order #{order.order_number} placed successfully!')
            return redirect('order_detail', pk=order.pk)

    subtotal = cart_obj.total_price
    delivery_fee = Decimal('3.99')
    tax = subtotal * Decimal('0.08')
    total = subtotal + delivery_fee + tax

    context = {
        'cart': cart_obj,
        'form': form,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'tax': tax,
        'total': total,
    }
    return render(request, 'restaurant/checkout.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'restaurant/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'restaurant/order_detail.html', {'order': order})


@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=profile_obj)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

    return render(request, 'restaurant/profile.html', {'form': form, 'profile': profile_obj})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created! Welcome to FoodOrder!')
            return redirect('home')
    return render(request, 'registration/register.html', {'form': form})


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('order_detail', pk=pk)
