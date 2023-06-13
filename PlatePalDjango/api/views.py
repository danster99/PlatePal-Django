from tkinter import Menu
from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from api.models import Category, Restaurant, Menu, Item
from drf_spectacular.utils import extend_schema

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
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

class MenuSerializer(serializers.HyperlinkedModelSerializer):
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

class CategorySerializer(serializers.HyperlinkedModelSerializer):
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

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Item
		fields = [
			"id",
			"name",
			"price",
			"category",
			"description",
			"image",
			"alergens",
			"isVegan",
			"spiceLvl",
			"nutriValues",
		]

@extend_schema(tags=["Item"])
class ItemViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all().order_by("id")
	serializer_class = ItemSerializer
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly]