from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Product, Price

def index(request):
    return render(request, 'main/index.html', {'product_list': Product.objects.all()})

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'main/detail.html', {'product': product})