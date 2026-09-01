from .models import Cart

def cart_context(request):
    """Add cart count to all templates"""
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass
    elif request.session.session_key:
        try:
            cart = Cart.objects.get(session_id=request.session.session_key)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass

    return {'cart_count': cart_count}
