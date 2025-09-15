from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def all_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_individual(request, prodid):
    product = get_object_or_404(Product, id=prodid)
    return render(request, 'individual_product.html', {'product': product})