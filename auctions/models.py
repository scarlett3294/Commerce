from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Auction(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_auctions")

class Bid(models.Model):
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    date_created = models.DateTimeField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    