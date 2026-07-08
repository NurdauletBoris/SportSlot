from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Venue, SportType, Review
from bookings.models import Booking, Favorite
from .forms import BookingForm, ReviewForm
from .serializers import VenueSerializer, ReviewSerializer  



def venue_list(request):
    venues = Venue.objects.all()
    sport_types = SportType.objects.all()

    sport_id = request.GET.get('sport')
    if sport_id:
        venues = venues.filter(sport_type_id=sport_id)

    return render(request, 'venues/venue_list.html', {
        'venues': venues,
        'sport_types': sport_types,
        'selected_sport': sport_id,
    })


def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    reviews = venue.reviews.all().order_by('-created_at')

    booking_form = BookingForm()
    review_form = ReviewForm()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, venue=venue).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Сначала войдите в аккаунт.')
            return redirect('login')

        if 'booking_submit' in request.POST:
            booking_form = BookingForm(request.POST)
            booking_form.instance.user = request.user
            booking_form.instance.venue = venue

            if booking_form.is_valid():
                try:
                    booking_form.save()
                    messages.success(request, 'Бронь успешно создана.')
                    return redirect('venue_detail', pk=venue.pk)
                except ValidationError as e:
                    messages.error(request, '; '.join(e.messages))

        elif 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)

            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.venue = venue
                review.save()

                messages.success(request, 'Отзыв успешно добавлен.')
                return redirect('venue_detail', pk=venue.pk)

    return render(request, 'venues/venue_detail.html', {
        'venue': venue,
        'reviews': reviews,
        'booking_form': booking_form,
        'review_form': review_form,
        'is_favorite': is_favorite,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-start_time')
    return render(request, 'venues/my_bookings.html', {
        'bookings': bookings
    })


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Бронь отменена.')

    return redirect('my_bookings')

@login_required
def toggle_favorite(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    favorite = Favorite.objects.filter(user=request.user, venue=venue)

    if favorite.exists():
        favorite.delete()
        messages.success(request, 'Площадка удалена из избранного.')
    else:
        Favorite.objects.create(user=request.user, venue=venue)
        messages.success(request, 'Площадка добавлена в избранное.')

    return redirect('venue_detail', pk=venue.pk)


@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('venue')
    return render(request, 'venues/favorites.html', {
        'favorites': favorites
    })



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_venue_list(request):
    if request.method == 'GET':
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_venue_reviews(request, pk):
    try:
        venue = Venue.objects.get(pk=pk)
    except Venue.DoesNotExist:
        return Response({'error': 'Venue not found'}, status=status.HTTP_404_NOT_FOUND)
        
    reviews = Review.objects.filter(venue=venue)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)