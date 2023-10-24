import json
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from api.models import Category, Restaurant, Menu, Item, Order, Cart, Table
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
import re

class RestaurantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Restaurant
		fields = [
			"id",
			"name",
			"address",
			"phone",
			"website",
		]

@extend_schema(tags=["Restaurant"])
class RestaurantViewSet(viewsets.ModelViewSet):
	queryset = Restaurant.objects.all().order_by("id")
	serializer_class = RestaurantSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'post', 'delete']

class MenuSerializer(serializers.ModelSerializer):
	class Meta:
		model = Menu
		fields = [
			"id",
			"restaurant",
			"features",
		]

@extend_schema(tags=["Menu"])
class MenuViewSet(viewsets.ModelViewSet):
	queryset = Menu.objects.all().order_by("id")
	serializer_class = MenuSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'post', 'delete']

	@action(methods=['get'], detail=True, url_path='categories', url_name='categories')
	def get_catgories(self, request, pk=None):
		obj = Category.objects.filter(menu=Menu.objects.get(pk=pk))
		serializer = CategorySerializer(obj, many=True)
		return HttpResponse(json.dumps(serializer.data), content_type="application/json")

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = [
			"id",
			"name",
			"menu",
			"isFood",
		]

@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all().order_by("id")
	serializer_class = CategorySerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'post', 'delete']

	@action(methods=['get'], detail=True, url_path='items', url_name='items')
	def get_items(self, request, pk=None):
		items = Item.objects.filter(category=Category.objects.get(pk=pk))
		serializer = ItemSerializer(items, many=True)
		return HttpResponse(json.dumps(serializer.data), content_type="application/json")

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = [
			"id",
			"name",
			"price",
			"category",
			"description",
			"b2StorageFile",
			"alergens",
			"aditives",
			"isVegan",
			"isDairyFree",
			"isGlutenFree",
			"spiceLvl",
			"nutriValues",
			"isAvailable"
		]

	def create(self, validated_data):
		filename = validated_data["b2StorageFile"].name
		if( re.search("^(?!.*\.\.)[\w-]+\.(svg|jpe?g|png|gif|bmp)$", filename) == False):
			raise serializers.ValidationError("Invalid filename")
		return super().create(validated_data)

	
@extend_schema(tags=["Item"])
class ItemViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all().order_by("id")
	serializer_class = ItemSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'post', 'delete', 'put']

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model= Order
		fields = [
			"id",
			"items",
			"total",
			"payment_method",
			"tip",
		]

@extend_schema(tags=["Order"])
class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all().order_by("id")
	serializer_class = OrderSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'post', 'delete']


class TableSerializer(serializers.ModelSerializer):
	class Meta:
		model= Table
		fields = [
			"id",
			"restaurant",
			"number",
			"seats",
			"cart"
		]

@extend_schema(tags=["Table"])
class TableViewSet(viewsets.ModelViewSet):
	queryset = Table.objects.all().order_by("id")
	serializer_class = TableSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get','post', 'delete']

	@action(methods=['post'], detail=True, url_path='new_cart', url_name='cart')
	def createCart(self, request, pk=None):
		table = Table.objects.get(pk=pk)
		print(table)
		try:
			cart = table.cart
			if cart.status == "Closed":
				cart = Cart.objects.create()
				cart.save()
				table.cart = cart
				table.save()
				return HttpResponse(json.dumps(model_to_dict(cart)), content_type="application/json")
			else:
				raise serializers.ValidationError("An open cart already exists")
		except Cart.DoesNotExist:
			print("Cart does not exist")
			cart = Cart.objects.create()
			cart.save()
			table.cart = cart
			table.save()
			return HttpResponse(json.dumps(model_to_dict(cart)), content_type="application/json")

	

class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model= Cart
		fields = [
			"id",
			"items",
			"total",
			"status",
			"table"
		]
@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ModelViewSet):
	queryset = Cart.objects.all().order_by("id")
	serializer_class = CartSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get','post', 'delete']

	@action(methods=['put'], detail=True, url_path='cart', url_name='cart')
	def addItem(self, request, pk=None):
		cart = Cart.objects.get(pk=pk)
		item = Item.objects.get(pk=request.data["item"])
		cart.items.add(item)
		cart.total += item.price
		cart.save()
		return HttpResponse(json.dumps(model_to_dict(cart)), content_type="application/json")
	
	@action(methods=['put'], detail=True, url_path='cart', url_name='cart')
	def removeItem(self, request, pk=None):
		cart = Cart.objects.get(pk=pk)
		item = Item.objects.get(pk=request.data["item"])
		if item in cart.items.all():
			cart.items.remove(item)
			cart.total -= item.price
			cart.save()
			return HttpResponse(json.dumps(model_to_dict(cart)), content_type="application/json")
		else:
			raise serializers.ValidationError("Item not in cart")