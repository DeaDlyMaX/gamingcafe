from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_prime = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# for rental page 
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    console = models.CharField(max_length=100, default="XBOX")
    days = models.PositiveIntegerField()
    controllers = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    xbaox_avl = models.IntegerField(default=10)
    ps_avl = models.IntegerField(default=10)
    def save(self, *args, **kwargs):
        # Ensure `days` is an integer and set pickup_date to one day after booking_date
        self.days = int(self.days)  # Convert days to integer
        
        if not self.pickup_date:
            self.pickup_date = self.booking_date + timedelta(days=1)
        
        # Set return_date to 'days' after pickup_date
        if self.pickup_date and not self.return_date:
            self.return_date = self.pickup_date + timedelta(days=self.days)
        
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"Booking by {self.user.username} on {self.booking_date}"
    
# Console model to manage individual consoles
# class Console(models.Model):
#     CONSOLE_CATEGORY_CHOICES = [
#         ("XBOX", "Xbox"),
#         ("PS", "PlayStation"),
#     ]

#     console_id = models.AutoField(primary_key=True)  # Unique ID for each console
#     console_category = models.CharField(max_length=10, choices=CONSOLE_CATEGORY_CHOICES)
#     is_available = models.BooleanField(default=True)
#     current_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     rental_start_date = models.DateTimeField(null=True, blank=True)
#     rental_return_date = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.console_category} - {self.console_id} ({'Available' if self.is_available else 'Rented'})"


# # Booking for consoles
# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     console = models.ForeignKey(Console, on_delete=models.CASCADE)
#     days = models.PositiveIntegerField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     booking_date = models.DateTimeField(auto_now_add=True)
#     pickup_date = models.DateTimeField(null=True, blank=True)
#     return_date = models.DateTimeField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         # Ensure `days` is an integer and set pickup_date to one day after booking_date
#         self.days = int(self.days)

#         if not self.pickup_date:
#             self.pickup_date = self.booking_date + timedelta(days=1)

#         # Set return_date to 'days' after pickup_date
#         if self.pickup_date and not self.return_date:
#             self.return_date = self.pickup_date + timedelta(days=self.days)

#         # Update console availability and rental details
#         if self.console.is_available:
#             self.console.is_available = False
#             self.console.current_user = self.user
#             self.console.rental_start_date = self.pickup_date
#             self.console.rental_return_date = self.return_date
#             self.console.save()

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Console Booking by {self.user.username} for {self.console.console_category}"
    
class BookPc(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pc_number = models.PositiveIntegerField(unique=True)  # Unique PC number
    duration = models.PositiveIntegerField()  # Duration in hours
    start_time = models.TimeField()  # Start time
    end_time = models.TimeField()  # Calculated end time
    booked_at = models.DateTimeField(auto_now_add=True)  # Booking timestamp