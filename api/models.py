from django.db import models
from multiselectfield import MultiSelectField

FEATURES =  ((1, 'Core'),
            (2, 'Feedback'),
            (3, 'Statistics'),
            (4, 'In-App Interaction'),
            (5, 'AR'),
            (6, 'Dynamic Pricing'),)

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    features = MultiSelectField(choices=FEATURES, max_length=10)
    def __str__(self):
        return self.restaurant.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    isFood = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    alergens = models.TextField(null=True, blank=True)
    isVegan = models.BooleanField(default=False)
    isDairyFree = models.BooleanField(default=False)
    isGlutenFree = models.BooleanField(default=False)
    spiceLvl = models.IntegerField(default=0)
    nutriValues = models.JSONField(null=True, blank=True)
    clicks24h = models.IntegerField(default=0)
    clicks7d = models.IntegerField(default=0)
    clicks30d = models.IntegerField(default=0)
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return self.name
