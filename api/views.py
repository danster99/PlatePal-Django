import json
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from api.models import Category, Restaurant, Menu, Item, Order, Cart, Story, Table, Review
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
import re
from django.db import transaction
from datetime import datetime
from django.db import connection
import django_filters as filters



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
		connection.close()
		return HttpResponse(json.dumps(serializer.data), content_type="application/json")
	
	@action(methods=['get'], detail=True, url_path='stories', url_name='stories')
	def get_stories(self, request, pk=None):
		obj = Story.objects.filter(menu=Menu.objects.get(pk=pk))
		serializer = StorySerializer(obj, many=True)
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
			"table",
			"restaurant",
			"time_at_table",
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
			"seats"
		]

@extend_schema(tags=["Table"])
class TableViewSet(viewsets.ModelViewSet):
	queryset = Table.objects.all().order_by("id")
	serializer_class = TableSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get','post', 'delete']

	@action(methods=['post'], detail=True, url_path='new_cart', url_name='new_cart')
	def createCart(self, request, pk=None):
		table = Table.objects.get(pk=pk)
		try:
			cart = Cart.objects.get(table=table)
			if cart.status == "Closed":
				cart.empty()
			return HttpResponse(json.dumps(model_to_dict(cart), default=str), content_type="application/json")
		except Cart.DoesNotExist:
			cart = Cart.objects.create(table=table)
			table.cart = cart
			table.save()
			return HttpResponse(json.dumps(model_to_dict(cart), default=str), content_type="application/json")
	

class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model= Cart
		fields = [
			"id",
			"items",
			"total",
			"table",
			"status",
			"table",
			"created_at",
			"closed_at"
		]
@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ModelViewSet):
	queryset = Cart.objects.all().order_by("id")
	serializer_class = CartSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get','post', 'delete', 'put']

	@action(methods=['put'], detail=True, url_path='add_item', url_name='add_item')
	@transaction.atomic
	def addItem(self, request, pk=None):
		cart = Cart.objects.get(pk=pk)
		if cart.status != "Open":
			raise serializers.ValidationError("Cart is not open")
		item = Item.objects.get(pk=request.data["item"])
		cart.items.append(item.id)
		cart.total += item.price
		cart.save()
		return HttpResponse(json.dumps(model_to_dict(cart), default=str), content_type="application/json")
	
	@action(methods=['put'], detail=True, url_path='remove_item', url_name='remove_item')
	@transaction.atomic
	def removeItem(self, request, pk=None):
		cart = Cart.objects.get(pk=pk)
		if cart.status != "Open":
			raise serializers.ValidationError("Cart is not open")
		item = Item.objects.get(pk=request.data["item"])
		if item.id in cart.items:
			cart.items.remove(item.id)
			cart.total -= item.price
			cart.save()
			return HttpResponse(json.dumps(model_to_dict(cart), default=str), content_type="application/json")
		else:
			raise serializers.ValidationError("Item not in cart")
		
	@action(methods=['post'], detail=True, url_path='checkout', url_name='checkout')
	@transaction.atomic
	def checkout(self, request, pk=None):
		cart = Cart.objects.get(pk=pk)
		cart.status = "Checkout"
		cart.save()
		return HttpResponse(json.dumps(model_to_dict(cart), default=str), content_type="application/json")
	
	@action(methods=['post'], detail=True, url_path='close', url_name='close')
	@transaction.atomic
	def pay(self, request, pk=None):
		cart = Cart.objects.get(pk=pk)
		cart.closed_at = datetime.now(cart.created_at.tzinfo)
		cart.status = "Closed"
		cart.save()
		table = Table.objects.get(cart=cart)
		start = cart.created_at
		end = cart.closed_at
		tat = (end-start).total_seconds() / 60
		Order.objects.create(
			restaurant=table.restaurant,
			table=table,
			items=cart.items,
			total=cart.total,
			payment_method=request.data["payment_method"],
			tip=request.data["tip"],
			time_at_table= tat
		)
		connection.close()
		return HttpResponse(json.dumps(model_to_dict(cart), default=str), content_type="application/json")
	

class StorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Story
		fields = [
			"id",
			"menu",
			"title",
			"description",
			"b2StorageFile",
			"active",
			"created_at",
		]

	def create(self, validated_data):
		filename = validated_data["b2StorageFile"].name
		if( re.search("^(?!.*\.\.)[\w-]+\.(svg|jpe?g|png|gif|bmp)$", filename) == False):
			raise serializers.ValidationError("Invalid filename")
		return super().create(validated_data)

	
@extend_schema(tags=["Story"])
class StoryViewSet(viewsets.ModelViewSet):
	queryset = Story.objects.all().order_by("id")
	serializer_class = StorySerializer 
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'post', 'delete', 'put']


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = [
			"id",
			"menu",
			"rating_food",
			"rating_drinks",
			"rating_service",
			"rating_experience",
			"comment",
			"created_at",
	]
		
class ReviewFilter(filters.FilterSet):
	# menu = filters.NumberFilter(field_name="menu")
	class Meta:
		model = Review
		fields = {"menu":["exact"]}
@extend_schema(tags=["Review"])
class ReviewViewSet(viewsets.ModelViewSet):
	queryset = Review.objects.all().order_by("id")
	serializer_class = ReviewSerializer
	filterset_class = ReviewFilter
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	http_method_names = ['get', 'post', 'delete', 'put']
