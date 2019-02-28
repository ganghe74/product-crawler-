from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('<int:product_id>/subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:subscriber_id>', views.unsubscribe, name='unsubscribe'),
]