from django.db import models
from django.core.exceptions import ValidationError
from userAuth.models import User
from datetime import timedelta, datetime
from enum import Enum

class BookingStatus(Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    REJECTED = 'REJECTED'

class Futsal(models.Model):
    FUTSAL_TYPES = [
        ('5A', '5-A-Side'),
        ('7A', '7-A-Side'),
        ('6A', '6-A-Side'),
        # Add more futsal types as needed
    ]
    
    name = models.CharField(max_length=100)
    images = models.ImageField( default="football-bg.jpg")
    futsal_type = models.CharField(max_length=2, choices=FUTSAL_TYPES)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    open_time = models.TimeField()
    close_time = models.TimeField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Validate image URLs or paths if needed
        # ...

        super().save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    futsal = models.ForeignKey(Futsal, on_delete=models.CASCADE)
    booking_date = models.DateField(default=datetime.today)
    booking_time = models.TimeField(null=True)
    book_time = models.PositiveIntegerField(default=1)  # Booking duration in hours
    # show only status without class
    status = models.CharField(max_length=10, choices=[(tag.value, tag.value) for tag in BookingStatus], default=BookingStatus.PENDING.value) 
    def __str__(self):
        status_value = self.status.value if isinstance(self.status, BookingStatus) else self.status
        return f"{self.user.username}'s Booking at {self.futsal.name} on {self.booking_date.strftime('%d-%m-%Y')} at {self.booking_time.strftime('%I:%M %p')} for {self.book_time} hours, Status: {status_value.upper()}"
