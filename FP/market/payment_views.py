import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order

@login_required
def payment_process(request, order_id):
    """Handle Razorpay payment processing"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    # Check if already paid
    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'razorpay_key': settings.RAZORPAY_KEY_ID if hasattr(settings, 'RAZORPAY_KEY_ID') else 'test_key',
    }
    return render(request, 'market/payment.html', context)

@login_required
def payment_success(request, order_id):
    """Handle successful payment callback with signature verification"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        # Verify signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            # Signature is valid, mark as paid
            order.payment_status = 'paid'
            order.status = 'confirmed'
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_order_id = razorpay_order_id
            order.razorpay_signature = razorpay_signature
            order.save()
            
            messages.success(request, 'Payment successful! Your order has been confirmed.')
        except Exception as e:
            messages.error(request, f'Payment verification failed: {e}')
            order.payment_status = 'failed'
            order.save()
            
        return redirect('order_detail', order_id=order.id)
    
    return redirect('order_detail', order_id=order.id)
