from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        # Юзерді request.user арқылы аламыз, сондықтан оны API арқылы өзгертуге тыйым саламыз
        read_only_fields = ['user', 'created_at']