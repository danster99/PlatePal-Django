from django.contrib import admin

# Register your models here.
from .models import Restaurant, Menu, Category, Item

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'category', 'isAvailable')
	list_filter = ['category__name']
	search_fields = ('name', 'category__name')

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)

