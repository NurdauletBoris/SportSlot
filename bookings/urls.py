from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # --- Аутентификация (Токен алу және өшіру) ---
    path('auth/login/', obtain_auth_token, name='api-login'),
    path('auth/logout/', views.logout_view, name='api-logout'),
    
    # --- Бронирования (CRUD) ---
    # GET (тізім) және POST (жасау)
    path('bookings/', views.BookingListCreateAPIView.as_view(), name='api-booking-list'),
    
    # GET (бір броньды көру), PUT (өзгерту), DELETE (өшіру)
    path('bookings/<int:pk>/', views.BookingDetailAPIView.as_view(), name='api-booking-detail'),
]