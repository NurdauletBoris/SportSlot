from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class SportType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=200)
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE, related_name='venues')
    address = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.venue} — {self.rating}'