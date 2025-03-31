from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_price = models.DecimalField(decimal_places=2, max_digits=10)
    end_time = models.DateTimeField()

    def is_active(self):
        return self.end_time > timezone.now()

    def current_price(self):
        last_bid = Bid.objects.filter(auction=self).order_by('-created_at').first()
        return last_bid.price if last_bid is not None else self.start_price

    def __str__(self):
        return f'{self.user} - {self.name}'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} bids {self.price} on {self.created_at.strftime("%d %B %Y")} at {self.created_at.strftime("%H:%M:%S")}'
