from django.shortcuts import render
from Home.models import Product

def hinfo(request):
    # Show featured/hot offers
    featured_products = Product.objects.filter(is_featured=True, is_active=True).order_by('-created_at')
    hot_offers = Product.objects.filter(is_active=True).order_by('price')[:10]  # Cheapest items as "hot offers"

    context = {
        'featured_products': featured_products,
        'hot_offers': hot_offers,
    }
    return render(request, 'Hotoffers/hotoffer.html', context)