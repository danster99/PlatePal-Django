from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from api.models import Category, Restaurant, Menu, Item
from drf_spectacular.utils import extend_schema
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
	http_method_names = ['get']

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
	http_method_names = ['get']

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
	http_method_names = ['get']

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
	http_method_names = ['get']