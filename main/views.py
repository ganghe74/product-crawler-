from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Product, Price, Subscriber
from .forms import SubscribeForm

from datetime import datetime

def index(request):
    return render(request, 'main/index.html', {'product_list': Product.objects.all()})

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
        'recent_price_list': product.price_set.all(),
    }
    return render(request, 'main/detail.html', context)

def subscribe(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.product = product
            subscriber.registration_date = timezone.now()
            subscriber.save()
            return redirect('subscribe', product_id=product_id)
        return redirect('index')
    else:
        p = product.price_set.last().price
        form = SubscribeForm(initial={'min_price':p, 'max_price':p})
        subscriber = product.subscriber_set.all()
        context = {
            'form': form, 
            'product': product,
            'subscribers': subscriber,
        }
    return render(request, 'main/subscribe/subscribe.html', context)

def unsubscribe(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
    product = subscriber.product
    if request.method == 'POST':
        if request.POST.get('email', '') == subscriber.email:
            subscriber.delete()
            return redirect('subscribe', product_id=product.id)
        else:
            return HttpResponse('<h1>WRONG EMAIL!! FUCK YOU!!</h1>')
    context = {
        'product': product,
        'subscriber': subscriber,
    }
    return render(request, 'main/subscribe/unsubscribe.html', context)

def subscribe_detail(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
    context = {
        'subscriber': subscriber,
    }
    return render(request, 'main/subscribe/detail.html', context)