from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Booking
from .serializers import BookingSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

class BookingListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Осы жерде юзерді тіркейміз
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except DjangoValidationError as e:
                # Егер clean() қате тапса, оны фронтқа жібереміз
                return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Booking, pk=pk, user=user)

    def get(self, request, pk):
        booking = self.get_object(pk, request.user)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk):
        booking = self.get_object(pk, request.user)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(serializer.data)
            except DjangoValidationError as e:
                return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = self.get_object(pk, request.user)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)