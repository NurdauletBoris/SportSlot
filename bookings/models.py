from django.db import models
from django.core.exceptions import ValidationError

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
    
    def clean(self):
        
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError('Время окончания должно быть позже времени начала.')

        
        overlapping = Booking.objects.filter(
            venue=self.venue,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk).exclude(status='cancelled')

        if overlapping.exists():
            raise ValidationError('Этот слот уже занят. Выберите другое время.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')
    venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'venue')