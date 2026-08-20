from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib import messages
from django.conf import settings
from math import radians, cos, sin, asin, sqrt
from .models import Product, Item, Order, OrderItem, OrderFeedback

@login_required
def submit_feedback(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if hasattr(order, 'feedback'):
        messages.error(request, 'You have already provided feedback for this order.')
        return redirect('order_detail', order_id=order.id)
        
    if request.method == 'POST':
        score = request.POST.get('score')
        comment = request.POST.get('comment', '')
        
        if score:
            OrderFeedback.objects.create(
                order=order,
                buyer=request.user,
                seller=order.seller,
                score=int(score),
                comment=comment
            )
            messages.success(request, 'Thank you for your feedback!')
        else:
            messages.error(request, 'Please provide a rating score.')
            
    return redirect('order_detail', order_id=order.id)
from .forms import ProductForm
from .utils import haversine


def market_index(request):
    if not Item.objects.exists():
        try:
            from seed_items import seed_marketplace_items
            seed_marketplace_items()
        except Exception as e:
            print(f"Auto-seed error: {e}")

    category = request.GET.get('category', 'All')
    if category and category != 'All':
        items = Item.objects.filter(category__iexact=category)
    else:
        items = Item.objects.all()

    return render(request, 'market/index.html', {
        'items': items,
        'selected_category': category,
        'categories': ['All', 'Vegetables', 'Fruits', 'Herbs']
    })

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
        
        # Check if following
        is_following = False
        if request.user.is_authenticated:
            is_following = request.user.following.filter(id=seller.id).exists()
        
        results.append({
            'seller': seller,
            'products': seller_products,
            'distance': round(distance, 1) if distance is not None else None,
            'rating': round(avg_rating, 1) if avg_rating else None,
            'rating_count': seller.received_ratings.count(),
            'is_following': is_following,
            'wishlisted_ids': list(request.user.wishlist.values_list('product_id', flat=True)) if request.user.is_authenticated else []
        })
    
    # Sort by distance
    results.sort(key=lambda x: (x['distance'] is None, x['distance']))
    
    return render(request, 'market/sellers_list.html', {'item': item, 'results': results})

def search_products(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'All')

    if not Item.objects.exists():
        try:
            from seed_items import seed_marketplace_items
            seed_marketplace_items()
        except Exception:
            pass

    items = Item.objects.all()
    if query:
        items = items.filter(name__icontains=query)
    if category and category != 'All':
        items = items.filter(category__iexact=category)

    return render(request, 'market/index.html', {
        'items': items,
        'query': query,
        'selected_category': category,
        'categories': ['All', 'Vegetables', 'Fruits', 'Herbs']
    })

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
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, seller=request.user)
    if request.method == 'POST':
        if order.status == 'confirmed':
            order.status = 'completed'
            order.save()
            messages.success(request, f'Order #{order.id} marked as completed.')
        else:
            messages.error(request, 'Order cannot be marked as completed.')
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


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    """Toggle a product in the user's wishlist."""
    product = get_object_or_404(Product, id=product_id)
    from .models import Wishlist
    
    wish_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        wish_item.delete()
        added = False
    else:
        added = True
        
    return JsonResponse({
        'status': 'success',
        'added': added
    })

@login_required
def wishlist_list(request):
    """View the user's wishlisted items."""
    from .models import Wishlist
    wish_items = Wishlist.objects.filter(user=request.user).select_related('product', 'product__item', 'product__seller')
    return render(request, 'market/wishlist.html', {'wish_items': wish_items})

@login_required
def seller_dashboard(request):
    """A comprehensive dashboard for sellers to track sales and performance."""
    from django.db.models import Sum, Count
    from .models import Order, Product
    
    # Revenue stats
    all_sales = Order.objects.filter(seller=request.user)
    completed_sales = all_sales.filter(status='completed')
    
    total_revenue = completed_sales.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = all_sales.count()
    pending_orders = all_sales.filter(status='pending').count()
    confirmed_orders = all_sales.filter(status='confirmed').count()
    
    active_listings = Product.objects.filter(seller=request.user, is_available=True).count()
    
    # Recent sales
    recent_sales = all_sales.order_by('-created_at')[:10]
    
    # Data for a simple sales chart (last 7 days)
    from datetime import timedelta
    from django.utils import timezone
    
    labels = []
    data = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        labels.append(day.strftime("%b %d"))
        day_sales = completed_sales.filter(created_at__date=day).aggregate(total=Sum('total_amount'))['total'] or 0
        data.append(float(day_sales))

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'active_listings': active_listings,
        'recent_sales': recent_sales,
        'chart_labels': labels,
        'chart_data': data,
    }
    return render(request, 'market/seller_dashboard.html', context)
