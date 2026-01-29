from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, HeroContent, Booking, Review, Worker, Category
from .forms import WorkerRegistrationForm, ReviewForm, CustomSignupForm

def index(request):
    hero = HeroContent.objects.first()
    categories = Category.objects.all()
    services = Service.objects.all().select_related('category')
    context = {
        'hero': hero,
        'categories': categories,
        'services': services
    }
    return render(request, 'web/index.html', context)

@login_required
def register_worker(request):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.user = request.user
            worker.save()
            messages.success(request, f"Welcome to the team, {worker.full_name}! Your application has been received. Our recruitment team will review your details and contact you within 48 hours for verification.")
            return redirect('worker_dashboard')
    else:
        # Pre-fill name and phone if available
        initial = {}
        if hasattr(request.user, 'profile'):
            initial['full_name'] = f"{request.user.first_name} {request.user.last_name}".strip()
            initial['phone_number'] = request.user.profile.phone_number
        form = WorkerRegistrationForm(initial=initial)
    
    return render(request, 'web/register_worker.html', {'form': form})

@login_required
@require_POST
def set_agreed_price(request, booking_id):
    worker = getattr(request.user, 'worker_profile', None)
    if not worker:
        return JsonResponse({'status': 'error', 'message': 'Access denied'}, status=403)
        
    booking = get_object_or_404(Booking, id=booking_id, assigned_worker=worker)
    price = request.POST.get('agreed_price')
    
    if price:
        booking.agreed_price = price
        booking.save()
        messages.success(request, f"Price for {booking.service.title} set to KES {price}.")
    
    return redirect('worker_dashboard')

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@require_POST
def book_service(request):
    service_id = request.POST.get('service_id')
    name = request.POST.get('name')
    location = request.POST.get('location')
    phone = request.POST.get('phone')
    contact_pref = request.POST.get('contact_preference', 'email')
    
    try:
        service = Service.objects.get(id=service_id)
        booking = Booking.objects.create(
            service=service,
            user=request.user if request.user.is_authenticated else None,
            customer_name=name,
            customer_phone=phone,
            location=location,
            contact_preference=contact_pref
        )
        return JsonResponse({'status': 'success', 'booking_id': booking.id})
    except Service.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Service not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'web/my_bookings.html', {'bookings': bookings})

@login_required
@require_POST
def submit_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if already reviewed
    if hasattr(booking, 'review'):
        messages.error(request, "You have already reviewed this service.")
        return redirect('my_bookings')
    
    # Check if assigned
    if not booking.assigned_worker:
        messages.error(request, "Cannot review a booking that hasn't been assigned to a worker.")
        return redirect('my_bookings')

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.booking = booking
        review.worker = booking.assigned_worker
        review.user = request.user
        review.save()
        messages.success(request, f"Thank you for your feedback on {booking.assigned_worker.full_name}'s work!")
    else:
        messages.error(request, "There was an error with your review submission.")
    
    return redirect('my_bookings')

@login_required
def worker_dashboard(request):
    # Check if user is a worker
    if not hasattr(request.user, 'worker_profile'):
        messages.error(request, "You are not registered as a worker.")
        return redirect('register_worker')
    
    worker = request.user.worker_profile
    active_jobs = Booking.objects.filter(assigned_worker=worker, status__in=['assigned', 'matching']).order_by('-created_at')
    completed_jobs = Booking.objects.filter(assigned_worker=worker, status='completed').order_by('-updated_at')
    
    # Stats
    total_jobs = completed_jobs.count()
    # Calculate revenue (ensure agreed_price is not None)
    total_revenue = sum(job.agreed_price for job in completed_jobs if job.agreed_price)
    avg_rating = worker.internal_rating

    context = {
        'worker': worker,
        'active_jobs': active_jobs,
        'completed_jobs': completed_jobs,
        'total_jobs': total_jobs,
        'total_revenue': total_revenue,
        'avg_rating': avg_rating
    }
    return render(request, 'web/worker_dashboard.html', context)

@login_required
@require_POST
def mark_booking_complete(request, booking_id):
    worker = getattr(request.user, 'worker_profile', None)
    if not worker:
        messages.error(request, "Access denied.")
        return redirect('index')
        
    booking = get_object_or_404(Booking, id=booking_id, assigned_worker=worker)
    booking.status = 'completed'
    booking.save()
    messages.success(request, "Job marked as complete! The customer has been notified to review and pay.")
    return redirect('worker_dashboard')

@require_POST
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    phone = request.POST.get('phone_number')
    amount = booking.agreed_price 
    
    if not amount:
        return JsonResponse({'status': 'error', 'message': 'Price not set for this service'}, status=400)

    print(f"Initiating Payment for Booking {booking_id} - {phone} - {amount}")
    from .utils.mpesa import DarajaClient
    from .models import Payment
    import os

    client = DarajaClient()
    # Use environment variable for callback URL or default to a placeholder
    callback_url = os.getenv('MPESA_CALLBACK_URL', 'https://mydomain.com/mpesa-callback/')
    
    print(f"Calling Daraja STK Push...")
    response = client.stk_push(phone, amount, callback_url)
    print(f"Daraja Response: {response}")
    
    if response.get('ResponseCode') == '0':
        # Update existing payment record if it exists, otherwise create new
        Payment.objects.update_or_create(
            booking=booking,
            defaults={
                'amount': amount,
                'phone_number': phone,
                'checkout_request_id': response.get('CheckoutRequestID'),
                'status': 'pending'
            }
        )
        return JsonResponse({
            'status': 'success', 
            'message': 'STK Push initiated successfully! Please enter your M-Pesa PIN on your phone.'
        })
    else:
        # Safaricom often returns 'errorMessage' and 'errorCode' for API faults
        error_msg = response.get('CustomerMessage') or response.get('message') or response.get('errorMessage') or 'Failed to initiate STK Push.'
        error_code = response.get('errorCode') or response.get('ResponseCode')
        
        full_error = f"{error_msg}"
        if error_code:
            full_error += f" (Code: {error_code})"
            
        return JsonResponse({
            'status': 'error', 
            'message': full_error
        }, status=500)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def mpesa_callback(request):
    import json
    import traceback
    from .models import Payment, Booking
    
    try:
        print("----- M-PESA CALLBACK RECEIVED -----")
        body_str = request.body.decode('utf-8')
        print(f"Callback Body: {body_str}")
        
        data = json.loads(body_str)
        stk_callback = data.get('Body', {}).get('stkCallback', {})
        result_code = stk_callback.get('ResultCode')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        
        print(f"Processing Callback for CheckoutID: {checkout_request_id}, ResultCode: {result_code}")
        
        payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()
        
        if payment:
            # ResultCode can be int 0 or str '0', handle both
            if str(result_code) == '0':
                # Success
                callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                transaction_code = ""
                for item in callback_metadata:
                    if item.get('Name') == 'MpesaReceiptNumber':
                        transaction_code = item.get('Value')
                        break
                
                print(f"Payment Success! Receipt: {transaction_code}")
                payment.status = 'completed'
                payment.transaction_code = transaction_code
                payment.save()
                
                booking = payment.booking
                booking.is_paid = True
                booking.save()
            else:
                # Failed
                print(f"Payment Failed/Cancelled. Code: {result_code}")
                payment.status = 'failed'
                payment.save()
        else:
            print(f"ERROR: Payment record not found for CheckoutID: {checkout_request_id}")
            
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        print(f"CRITICAL CALLBACK ERROR: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def check_payment_status(request, booking_id):
    from .models import Payment, Booking
    from .utils.mpesa import DarajaClient
    
    payment = get_object_or_404(Payment, booking__id=booking_id, booking__user=request.user)
    
    if payment.status != 'pending':
        return JsonResponse({'status': 'success', 'message': f'Payment is already {payment.status}.', 'payment_status': payment.status})
        
    client = DarajaClient()
    response = client.query_stk_status(payment.checkout_request_id)
    
    # ResultCode 0 means success
    result_code = response.get('ResultCode')
    
    if result_code == '0':
        payment.status = 'completed'
        # The query response doesn't always contain the receipt number, but let's check
        # Usually STK Query returns basic result.
        payment.save()
        
        booking = payment.booking
        booking.is_paid = True
        booking.save()
        
        messages.success(request, "Payment confirmed! Thank you.")
        return JsonResponse({'status': 'success', 'message': 'Payment confirmed successfully.', 'payment_status': 'completed'})
    elif result_code:
        # Some other code means failure/cancelled
        payment.status = 'failed'
        payment.save()
        return JsonResponse({'status': 'error', 'message': response.get('ResultDesc', 'Payment failed.'), 'payment_status': 'failed'})
    else:
        # No result code yet (still pending in Safaricom system)
        return JsonResponse({'status': 'pending', 'message': 'Payment is still being processed. Please wait a moment.'})
