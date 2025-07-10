# books/urls.py
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.home), name='home'),
    path('book/<int:pk>/', login_required(views.book_detail), name='book_detail'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'), 
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('create_order/', views.create_order, name='create_order'),
]


