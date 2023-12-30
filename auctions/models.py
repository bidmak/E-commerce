from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Bid(models.Model):
    price = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} offered £{self.price}"


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=1000, blank=True, null=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")
    userBid = models.ManyToManyField(User, blank=True, null=True, related_name="user_listings")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingcomment")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"

