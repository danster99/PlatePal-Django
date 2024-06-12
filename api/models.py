from datetime import datetime
from django.db import models
from django.core.files.storage import default_storage
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

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

def upload_logo_to(instance, filename):
    restaurant_name = instance.name.lower().replace(" ", "_")
    filename = f"{restaurant_name}/logo.{filename.split('.')[-1]}"
    return f"uploads/{filename}"

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    logo = models.FileField(
        name="b2StorageFile",
        upload_to=upload_logo_to,
        verbose_name="B2 Storage File",
        storage=default_storage,  # type: ignore
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

def upload_background_to(instance, filename):
    restaurant_name = instance.restaurant.name.lower().replace(" ", "_")
    filename = f"{restaurant_name}/background.{filename.split('.')[-1]}"
    return f"uploads/{filename}"

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    features = ArrayField(models.IntegerField(), default=list, size=6)
    primary = models.CharField(max_length=100, null=False, blank=True, default="#f5c636")
    secondary = models.CharField(max_length=100, null=False, blank=True, default="#f5c636")
    font = models.CharField(max_length=100, null=True, blank=True)
    backgroundImage = models.FileField(
        name="b2StorageFile",
        upload_to=upload_background_to,
        verbose_name="B2 Storage File",
        storage=default_storage,  # type: ignore
        default="https://f004.backblazeb2.com/file/platepal/background.png",
        blank=True,
    )

    def __str__(self):
        return self.restaurant.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
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
    name = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    photo = models.FileField(
        name="b2StorageFile",
        upload_to=upload_to,
        verbose_name="B2 Storage File",
        storage=default_storage,  # type: ignore
        blank=True,
    )
    weight = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


cart_status = (
    ("Open", "Open"),
    ("Checkout", "Checkout"),
    ("Closed", "Closed"),
)

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)
    number = models.IntegerField(null=False, blank=False)
    seats = models.IntegerField(null=False, blank=False)

class Cart(models.Model):
    items = ArrayField(models.IntegerField(), default=list)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0)
    status = models.CharField(choices=cart_status, null=False, default="Open")
    table = models.OneToOneField(Table, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def empty(self):
        self.items.clear()
        self.total = 0
        self.status = "Open"
        self.created_at = datetime.now()
        self.closed_at = None
        self.save()

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    items = ArrayField(models.IntegerField(), default=list)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    payment_method = models.CharField(choices=PAYMENT_METHODS, null=False, blank=False)
    tip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    time_at_table = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.restaurant.name + "-" + self.id + " - " + str(self.total)


def upload_to_story(instance, filename):
    restaurant_name = instance.menu.restaurant.name.lower().replace(" ", "_")
    menu_id = instance.menu.id
    name = instance.title.lower().replace(" ", "_")
    filename = (
        f"{restaurant_name}/{menu_id}/{name}.{filename.split('.')[-1]}"
    )
    return f"stories/{filename}"



class Story(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True)
    photo = models.FileField(
        name="b2StorageFile",
        upload_to=upload_to_story,
        verbose_name="B2 Storage File",
        storage=default_storage,  # type: ignore
        blank=True,
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.menu.restaurant.name + "-" + self.title
    

class Review(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    rating_food = models.IntegerField(null=False, blank=False)
    rating_drinks = models.IntegerField(null=False, blank=False)
    rating_service = models.IntegerField(null=False, blank=False)
    rating_experience = models.IntegerField(null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.menu.restaurant.name + "-reviewID-" + self.id
    

class HopmePageRow(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, default=-1)
    order = models.IntegerField(null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
def upload_to_card(instance, filename):
    restaurant_name = instance.row.menu.restaurant.name.lower().replace(" ", "_")
    menu_id = instance.row.menu.id
    name = instance.title.lower().replace(" ", "_")
    filename = (
        f"{restaurant_name}/{menu_id}/{name}.{filename.split('.')[-1]}"
    )
    return f"homepage_cards/{filename}"

card_size = (
    ("s", "S"),
    ("m", "M"),
    ("l", "L"),
    ("xl", "XL"),
)

class HomepageCard(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    row = models.ForeignKey(HopmePageRow, on_delete=models.CASCADE, default=-1)
    size = models.CharField(choices=card_size, null=False, blank=False)
    photo = models.FileField(
        name="b2StorageFile",
        upload_to=upload_to_card,
        verbose_name="B2 Storage File",
        storage=default_storage,  # type: ignore
        blank=True,
    )
    order= models.IntegerField(null=False, blank=False, default=0)
    active = models.BooleanField(default=True)
    links_to = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Complaint(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

