from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib import messages
from django.conf import settings
from math import radians, cos, sin, asin, sqrt
from .models import Product, Item, Order, OrderItem
from .forms import ProductForm
from .utils import haversine


def market_index(request):
    items = Item.objects.all()
    return render(request, 'market/index.html', {'items': items})

def item_sellers(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user_lat = request.user.latitude if request.user.is_authenticated else None
    user_lon = request.user.longitude if request.user.is_authenticated else None
    
    # Find all products for this item
    products = Product.objects.filter(item=item, is_available=True)
    
    # Exclude current user's products if logged in
    if request.user.is_authenticated:
        products = products.exclude(seller=request.user)
    
    # Group by seller
    sellers = set(product.seller for product in products)
    
    results = []
    for seller in sellers:
        # Calculate distance
        distance = None
        if user_lat is not None and user_lon is not None and seller.latitude is not None and seller.longitude is not None:
            distance = haversine(user_lon, user_lat, seller.longitude, seller.latitude)
        
        # Get seller's products for this item
        seller_products = products.filter(seller=seller)
        
        # Get seller's average rating
        avg_rating = seller.received_ratings.aggregate(Avg('score'))['score__avg']
        
        results.append({
            'seller': seller,
            'products': seller_products,
            'distance': round(distance, 1) if distance is not None else None,
            'rating': round(avg_rating, 1) if avg_rating else None,
            'rating_count': seller.received_ratings.count()
        })
    
    # Sort by distance
    results.sort(key=lambda x: (x['distance'] is None, x['distance']))
    
    return render(request, 'market/sellers_list.html', {'item': item, 'results': results})

def search_products(request):
    # Deprecated or redirect to filtered index? 
    # For now, let's keep basic search matching Item name redirects to item_sellers if exact match, or list items
    query = request.GET.get('q')
    if query:
        items = Item.objects.filter(name__icontains=query)
        return render(request, 'market/index.html', {'items': items})
    return redirect('market_index')

@login_required
def product_create(request):
    initial_data = {}
    item_name = request.GET.get('item_name')
    
    if item_name:
        # Try to find the item case-insensitive
        item = Item.objects.filter(name__iexact=item_name).first()
        if item:
            initial_data['item'] = item
            initial_data['description'] = f"Fresh {item.name} from my garden!"

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('market_index')
    else:
        form = ProductForm(initial=initial_data)
    return render(request, 'market/create.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user == product.seller:
        product.delete()
    return redirect('market_index')


@login_required
def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.seller == request.user:
        messages.error(request, "You cannot purchase your own product.")
        return redirect('market_index')
        
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        delivery_address = request.POST.get('delivery_address', '')
        notes = request.POST.get('notes', '')
        payment_method = request.POST.get('payment_method', 'cod')
        
        # Calculate total
        total = product.price * quantity
        
        # Create order
        order = Order.objects.create(
            buyer=request.user,
            seller=product.seller,
            total_amount=total,
            delivery_address=delivery_address,
            notes=notes,
            payment_method=payment_method,
            payment_status='pending'
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price_at_purchase=product.price
        )
        
        # Handle payment method
        if payment_method == 'online':
            # Redirect to payment page for Razorpay
            return redirect('payment_process', order_id=order.id)
        else:
            # COD - direct to order detail
            messages.success(request, f'Order placed successfully! Order #{order.id}')
            return redirect('order_detail', order_id=order.id)
    
    return render(request, 'market/order_create.html', {'product': product})


@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'market/orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user is buyer or seller
    if order.buyer != request.user and order.seller != request.user:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('order_list')
    
    return render(request, 'market/order_detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.buyer != request.user:
        messages.error(request, 'You do not have permission to cancel this order.')
        return redirect('order_list')
        
    if request.method == 'POST':
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Order #{order.id} has been cancelled successfully.')
        else:
            messages.error(request, f'Order #{order.id} cannot be cancelled because its status is {order.status}.')
            
    return redirect('order_detail', order_id=order.id)

@login_required
def payment_process(request, order_id):
    """Handle Razorpay payment processing"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    # Check if already paid
    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('order_detail', order_id=order.id)
    
    # For now, just show payment page (will add Razorpay integration)
    context = {
        'order': order,
        'razorpay_key': getattr(settings, 'RAZORPAY_KEY_ID', 'test_key'),
    }
    return render(request, 'market/payment.html', context)

@login_required
def payment_success(request, order_id):
    """Handle verification of manual P2P UPI payment completion and proof upload"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if request.method == 'POST':
        if not order.seller.upi_id:
            messages.error(request, 'Seller has no UPI ID configured.')
            return redirect('order_detail', order_id=order.id)
            
        # Capture uploaded payment proof
        if 'payment_proof' in request.FILES:
            order.payment_proof = request.FILES['payment_proof']
            
        # Manually confirm internal payment 
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.save()
        
        messages.success(request, 'Payment proof submitted! Your order has been confirmed.')
        return redirect('order_detail', order_id=order.id)
    
    return redirect('order_detail', order_id=order.id)

