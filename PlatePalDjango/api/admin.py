from django.contrib import admin

# Register your models here.
from .models import Restaurant, Menu, Category, Item

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Item)

