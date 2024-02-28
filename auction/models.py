# auction/models.py
from django.db import models
from vendor.models import Vendor, Item
from django.contrib.auth.models import User
from customers.models import Customer
from django.utils import timezone
from django.conf import settings
from djstripe.models import StripeModel



class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.user.username} - {self.item.title}'

class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    end_time = models.DateTimeField()
    winner = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # This could be the bid or direct purchase price
    quantity = models.IntegerField(default=1)  # Optional, based on your needs

class Payment(StripeModel):
    djstripe_owner_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auction_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username} - {self.description}'

class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.item.title}'