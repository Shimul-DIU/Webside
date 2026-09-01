from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, Order, OrderItem, Cart, CartItem, Review, Oderinfo, CATEGORY_CHOICES
import json


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    return cart


# ========== HOMEPAGE & PRODUCT LISTING ==========

def display(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    categories = dict(CATEGORY_CHOICES)

    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'Home/index.html', context)


def product_list(request):
    """List all products with filtering and search"""
    products = Product.objects.filter(is_active=True)
    category = request.GET.get('category')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '-created_at')

    # Filtering
    if category:
        products = products.filter(category=category)

    # Search
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # Sorting
    try:
        products = products.order_by(sort)
    except:
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)

    categories = dict(CATEGORY_CHOICES)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
        'selected_sort': sort,
    }
    return render(request, 'Home/products.html', context)


def product_detail(request, product_id):
    """Display detailed product information"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product_id)[:4]
    reviews = product.reviews.all()

    avg_rating = 0
    if reviews.exists():
        avg_rating = sum(r.rating for r in reviews) / reviews.count()

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'Home/product_detail.html', context)


def category_view(request, category):
    """View products by category"""
    products = Product.objects.filter(category=category, is_active=True).order_by('-created_at')

    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)

    categories = dict(CATEGORY_CHOICES)

    context = {
        'products': products,
        'selected_category': category,
        'category_name': categories.get(category, category),
        'categories': categories,
    }
    return render(request, 'Home/category.html', context)


# ========== CART MANAGEMENT ==========

def cart_view(request):
    """Display shopping cart"""
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'total': cart.get_total(),
        'item_count': cart.get_item_count(),
    }
    return render(request, 'Home/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart (AJAX)"""
    try:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            return JsonResponse({'success': False, 'message': 'Invalid quantity'})

        if not product.is_in_stock() or quantity > product.stock:
            return JsonResponse({'success': False, 'message': 'Out of stock'})

        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
            cart_item.save()

        return JsonResponse({
            'success': True,
            'message': f'Added {product.name} to cart',
            'cart_count': cart.get_item_count(),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def update_cart_item(request, item_id):
    """Update cart item quantity"""
    try:
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            cart_item = CartItem.objects.get(id=item_id)

            # Check stock
            if quantity > cart_item.product.stock:
                quantity = cart_item.product.stock

            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()

            return redirect('cart')
    except:
        pass
    return redirect('cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')


def clear_cart(request):
    """Clear entire cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    return redirect('cart')


# ========== CHECKOUT & ORDERS ==========

def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    if request.user.is_authenticated:
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
    else:
        initial_data = {}

    context = {
        'cart': cart,
        'total': cart.get_total(),
        'initial_data': initial_data,
    }
    return render(request, 'Home/checkout.html', context)


@require_POST
def process_order(request):
    """Process checkout and create order"""
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        return JsonResponse({'success': False, 'message': 'Cart is empty'})

    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        bkash_number = request.POST.get('bkash_number', '').strip()  # User's Bkash number

        # Validation
        if not all([name, phone, address, bkash_number]):
            return JsonResponse({'success': False, 'message': 'Please fill all required fields'})

        if len(phone) < 10:
            return JsonResponse({'success': False, 'message': 'Invalid phone number'})

        if len(bkash_number) < 11:
            return JsonResponse({'success': False, 'message': 'Invalid Bkash number'})

        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            bkash_number=bkash_number,
            payment_method='bkash',  # Always Bkash
            status='pending',
            total_price=cart.get_total(),
        )

        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        cart.items.all().delete()

        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully',
            'order_id': order.id,
            'redirect_url': f'/order/success/{order.id}/'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id)

    # Verify user can access this order
    if order.user and order.user != request.user:
        if not request.user.is_staff:
            messages.error(request, 'Unauthorized access')
            return redirect('home')

    items = order.orderitem_set.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'Home/order_success.html', context)


# ========== ORDER MANAGEMENT ==========

@login_required(login_url='login')
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(orders, 10)
    page = request.GET.get('page', 1)
    orders = paginator.get_page(page)

    context = {'orders': orders}
    return render(request, 'Home/order_history.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.orderitem_set.all()

    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'Home/order_detail.html', context)


# ========== AUTHENTICATION ==========

def login_info(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'loging.html')


def registrations(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Validation
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif password != password_confirm:
            messages.error(request, 'Passwords do not match')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')

    return render(request, 'registration.html')


@login_required(login_url='login')
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


# ========== USER PROFILE ==========

@login_required(login_url='login')
def profile(request):
    """User profile page"""
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'user': request.user,
        'recent_orders': recent_orders,
    }
    return render(request, 'Home/profile.html', context)


@login_required(login_url='login')
def update_profile(request):
    """Update user profile"""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request, 'Home/update_profile.html')


# ========== REVIEWS ==========

@login_required(login_url='login')
@require_POST
def add_review(request, product_id):
    """Add review to product"""
    try:
        product = get_object_or_404(Product, id=product_id)

        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not title or not comment:
            return JsonResponse({'success': False, 'message': 'Please fill all fields'})

        # Check if user already reviewed
        existing = Review.objects.filter(product=product, user=request.user).exists()
        if existing:
            return JsonResponse({'success': False, 'message': 'You already reviewed this product'})

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            title=title,
            comment=comment,
        )

        return JsonResponse({'success': True, 'message': 'Review added successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ========== LEGACY - FOR BACKWARD COMPATIBILITY ==========

def order(request):
    """Legacy order view - redirects to new system"""
    name = request.GET.get('name', '')
    img = request.GET.get('img', '')
    tk = request.GET.get('tk', '')

    if request.method == 'POST':
        uname = request.POST.get('name')
        phone = request.POST.get('phoneNumber')
        payment = request.POST.get('payment')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')

        Oderinfo.objects.create(
            name=uname,
            phone=phone,
            payment=payment,
            address=address,
            quantity=quantity
        )
        return redirect('home')

    return render(request, 'Order.html', {'name': name, 'img': img, 'tk': tk})