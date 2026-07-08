from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
   
    path('auth/login/', obtain_auth_token, name='api-login'),
    path('auth/logout/', views.logout_view, name='api-logout'),
    
    
    path('bookings/', views.BookingListCreateAPIView.as_view(), name='api-booking-list'),
    
    
    path('bookings/<int:pk>/', views.BookingDetailAPIView.as_view(), name='api-booking-detail'),
]