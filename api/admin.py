from django.contrib import admin

# Register your models here.
from .models import Restaurant, Menu, Category, Item, Order, Table, Cart, Story, Review, HomepageCard, HopmePageRow, Profile

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'category', 'isAvailable')
	list_filter = ['category__name']
	search_fields = ('name', 'category__name')

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(Table)
admin.site.register(Cart)
admin.site.register(Story)
admin.site.register(Review)
admin.site.register(HomepageCard)
admin.site.register(HopmePageRow)
admin.site.register(Profile)


