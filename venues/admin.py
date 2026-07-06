from django.contrib import admin
from .models import SportType, Venue, Review

admin.site.register(SportType)
admin.site.register(Venue)
admin.site.register(Review)