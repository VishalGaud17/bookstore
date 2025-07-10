from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Cart, CartItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
from django.views.decorators.http import require_POST
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
@login_required
def home(request):
    books = Book.objects.all()
    return render(request, 'main/home.html', {'books': books})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'main/details.html', {'book': book})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'authapp/login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Signup failed. Please check the form.')
    else:
        form = UserCreationForm()
    return render(request, 'authapp/signup.html', {'form': form})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')  # Redirect to cart or back to book page

@login_required
def remove_from_cart(request, book_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, book__id=book_id)
    
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.select_related('book').all()
    total = sum(item.total_price() for item in items)
    return render(request, 'main/cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required
@login_required
def create_order(request):
    try:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.select_related('book').all()
        total = sum(item.total_price() for item in items)

        if total == 0:
            messages.error(request, "Your cart is empty.")
            return redirect('view_cart')

        amount_paise = int(total * 100)  # Razorpay expects amount in paise

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {"user_id": str(request.user.id)}
        })

        return render(request, 'main/payment.html', {
            'payment': payment,
            'key': settings.RAZORPAY_KEY_ID,
            'total': total
        })
    except Exception as e:
        print("Payment creation failed:", e)
        messages.error(request, "Failed to create payment. Try again.")
        return redirect('view_cart')



@login_required
@require_POST
def clear_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.cartitem_set.all().delete()
    return redirect('view_cart')

def payment_cancel(request):
    # Optional: Add a message like "Payment was cancelled"
    return redirect('view_cart')  # Assuming 'cart' is the name of your cart page URL
