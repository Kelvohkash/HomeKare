from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('join-as-a-worker/', views.register_worker, name='register_worker'),
    path('book-service/', views.book_service, name='book_service'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('review/<int:booking_id>/', views.submit_review, name='submit_review'),
    path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('mark-complete/<int:booking_id>/', views.mark_booking_complete, name='mark_booking_complete'),
    path('set-price/<int:booking_id>/', views.set_agreed_price, name='set_agreed_price'),
    path('initiate-payment/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('check-payment-status/<int:booking_id>/', views.check_payment_status, name='check_payment_status'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
]
