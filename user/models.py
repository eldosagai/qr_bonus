from django.db import models
from django.contrib.auth.models import AbstractUser

Status = (
        ('1', 'Waiter'),
        ('0', 'Client'),
    )


class User(AbstractUser):
    phonenumber = models.CharField(max_length=50, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    activated = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=Status, default='0')
    
    def __str__(self):
        return self.phonenumber
    

class Restaurant(models.Model):
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant')
    
    def __str__(self):
        return self.name
    

class Bonuses(models.Model):
    amount = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bonus")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_bonus")
    
    def increment_bonuses(self, amount):
        self.amount+=amount
        self.save()
        
    def decrement_bonuses(self, amount):
        if self.amount > 0:
            self.amount-=amount
        self.save()