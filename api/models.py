from django.db import models
from django.core.files.storage import default_storage
from django.contrib.postgres.fields import ArrayField


FEATURES = (
    (1, "Core"),
    (2, "Feedback"),
    (3, "Statistics"),
    (4, "In-App Interaction"),
    (5, "AR"),
    (6, "Dynamic Pricing"),
)

PAYMENT_METHODS = (
    ("Cash", "Cash"),
    ("Card", "Card"),
    ("PayPal", "PayPal"),
    ("ApplePay", "ApplePay"),
    ("GooglePay", "GooglePay"),
)


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
    features = ArrayField(models.IntegerField(), default=list, size=6)

    def __str__(self):
        return self.restaurant.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    isFood = models.BooleanField(default=True)

    def __str__(self):
        return self.menu.restaurant.name + " - " + self.name


def upload_to(instance, filename):
    restaurant_name = instance.category.menu.restaurant.name.lower().replace(" ", "_")
    category_name = instance.category.name.lower().replace(" ", "_")
    item_name = instance.name.lower().replace(" ", "_")
    filename = (
        f"{restaurant_name}/{category_name}/{item_name}.{filename.split('.')[-1]}"
    )
    return f"uploads/{filename}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.FileField(
        name="b2StorageFile",
        upload_to=upload_to,
        verbose_name="B2 Storage File",
        storage=default_storage,  # type: ignore
        blank=True,
    )
    alergens = models.TextField(null=True, blank=True)
    aditives = models.TextField(null=True, blank=True)
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





class Order(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    items = models.ManyToManyField(Item, blank=False)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    payment_method = models.CharField(choices=PAYMENT_METHODS, null=False, blank=False)
    tip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.restaurant.name + "-" + self.id + " - " + str(self.total)

cart_status = (
    ("Open", "Open"),
    ("Checkout", "Checkout"),
    ("Paid", "Paid"),
    ("Closed", "Closed"),
)
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Item, blank=False)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(choices=cart_status, null=False, blank=False)

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    number = models.IntegerField(null=False, blank=False)
    seats = models.IntegerField(null=False, blank=False)