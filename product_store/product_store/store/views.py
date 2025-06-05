from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from .models import Product, Category

def home(request):
    featured_products = Product.objects.filter(stock__gt=0).order_by('-added_date')[:4]
    seasonal_offers = Product.objects.filter(is_seasonal=True).distinct()[:4]
    top_rated_products = Product.objects.filter(rating__gte=4.0).order_by('-rating')[:4]
    category_stats = Category.objects.annotate(avg_rating=Avg('product__rating'))
    search_query = request.GET.get('q', '')

    if search_query:
        search_results = Product.objects.filter(name__icontains=search_query)
        if search_results.exists():
            return redirect('product_detail', product_id=search_results.first().id)

    context = {
        'featured_products': featured_products,
        'seasonal_offers': seasonal_offers,
        'top_rated_products': top_rated_products,
        'category_stats': category_stats,
        'search_query': search_query
    }
    return render(request, 'store/index.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'store/category_list.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/category_detail.html', context)

def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        return redirect('category_detail', category_id=category.id)
    context = {
        'category': category
    }
    return render(request, 'store/category_edit.html', context)

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')

def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Category.objects.create(name=name, description=description)
        return redirect('category_list')
    return render(request, 'store/category_add.html')