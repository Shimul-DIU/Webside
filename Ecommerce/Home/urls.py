from django.urls import path
from . import views

urlpatterns = [
    # Homepage & Products
    path('', views.display, name='home'),
    path('products/', views.product_list, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category>/', views.category_view, name='category'),

    # Cart Management
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.process_order, name='process_order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # Authentication
    path('login/', views.login_info, name='login'),
    path('register/', views.registrations, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # User Profile
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),

    # Reviews
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),

    # Legacy
    path('order/', views.order, name='order_legacy'),
]
