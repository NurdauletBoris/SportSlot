from django.shortcuts import render
from .models import Venue, SportType

def venue_list(request):
    venues = Venue.objects.all()
    sport_types = SportType.objects.all()

    # фильтр по виду спорта (?sport=1 в адресе)
    sport_id = request.GET.get('sport')
    if sport_id:
        venues = venues.filter(sport_type_id=sport_id)

    return render(request, 'venues/venue_list.html', {
        'venues': venues,
        'sport_types': sport_types,
        'selected_sport': sport_id,
    })