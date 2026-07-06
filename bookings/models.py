from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bookings')
    venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.venue} {self.date} {self.start_time}-{self.end_time}'

class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')
    venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'venue')