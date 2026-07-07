from django.urls import path
from . import views

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('venues/<int:pk>/', views.venue_detail, name='venue_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('venues/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
]