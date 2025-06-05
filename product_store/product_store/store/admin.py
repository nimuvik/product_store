from django.contrib import admin
from django.shortcuts import render
from django.db.models import Avg, Count
from .models import Product, Category, Favorite

def home(request):
    featured_products = Product.objects.filter(stock__gt=0).order_by('-added_date')[:4]
    seasonal_offers = Product.objects.filter(is_seasonal=True).distinct()[:4]
    top_rated_products = Product.objects.filter(rating__gte=4.0).order_by('-rating')[:4]
    category_stats = Category.objects.annotate(avg_rating=Avg('product__rating'))
    search_query = request.GET.get('q', '')
    search_results = Product.objects.filter(name__icontains=search_query) if search_query else []

    context = {
        'featured_products': featured_products,
        'seasonal_offers': seasonal_offers,
        'top_rated_products': top_rated_products,
        'category_stats': category_stats,
        'search_results': search_results,
        'search_query': search_query
    }
    return render(request, 'store/index.html', context)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Favorite)