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
        'razorpay_key': settings.RAZORPAY_KEY_ID if hasattr(settings, 'RAZORPAY_KEY_ID') else 'test_key',
    }
    return render(request, 'market/payment.html', context)

@login_required
def payment_success(request, order_id):
    """Handle successful payment callback"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if request.method == 'POST':
        # Get Razorpay payment details
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        # TODO: Verify signature with Razorpay
        # For now, just mark as paid
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_order_id = razorpay_order_id
        order.razorpay_signature = razorpay_signature
        order.save()
        
        messages.success(request, 'Payment successful! Your order has been confirmed.')
        return redirect('order_detail', order_id=order.id)
    
    return redirect('order_detail', order_id=order.id)
