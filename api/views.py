import base64
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from .validations import validate_email, validate_password, validate_username
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from api.models import (
    Profile,
    Category,
    Restaurant,
    Menu,
    Item,
    Order,
    Cart,
    Story,
    Table,
    Review,
    HomepageCard,
    HopmePageRow,
    Complaint,
)
from drf_spectacular.utils import extend_schema, extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import action
import re
from django.db import transaction
from datetime import datetime
from django.db import connection
import django_filters as filters
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


class MenuIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id"]
class ProfileSerializer(serializers.ModelSerializer):
    menus = serializers.SerializerMethodField()
    
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_menus(self, obj):
        menus = Menu.objects.filter(restaurant=obj.restaurant)
        serializer = MenuIdSerializer(menus, many=True)
        return serializer.data
    class Meta:
        model = Profile
        fields = ["id", "user", "restaurant", "menus"]

@extend_schema(tags=["Profile"])
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by("id")
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]

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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete"]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",
            "restaurant",
            "features",
            "primary",
            "secondary",
            "font",
            "b2StorageFile",
        ]


@extend_schema(tags=["Menu"])
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by("id")
    serializer_class = MenuSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "put", "post", "delete"]

    @action(methods=["get"], detail=True, url_path="categories", url_name="categories")
    def get_catgories(self, request, pk=None):
        obj = Category.objects.filter(menu=Menu.objects.get(pk=pk))
        serializer = CategorySerializerTotalItems(obj, many=True)
        connection.close()
        return HttpResponse(
            json.dumps(serializer.data), content_type="application/json"
        )

    @action(methods=["get"], detail=True, url_path="stories", url_name="stories")
    def get_stories(self, request, pk=None):
        obj = Story.objects.filter(menu=Menu.objects.get(pk=pk)).order_by("id")
        serializer = StorySerializer(obj, many=True)
        return HttpResponse(
            json.dumps(serializer.data), content_type="application/json"
        )

    @action(methods=["get"], detail=True, url_path="items", url_name="items")
    def get_items(self, request, pk=None):
        response = dict()
        food = dict()
        drinks = dict()
        categories = Category.objects.filter(menu=Menu.objects.get(pk=pk))
        for category in categories:
            if category.isFood:
                items = Item.objects.filter(category=category)
                if items.count() > 0:
                    serializer = ItemSerializer(items, many=True)
                    food[category.name] = serializer.data
                else:
                    print(
                        "WARNING: No items in category: "
                        + category.name
                        + "-"
                        + str(category.id)
                        + " for menu: "
                        + str(pk)
                        + " skipping..."
                    )
            else:
                items = Item.objects.filter(category=category)
                if items.count() > 0:
                    serializer = ItemSerializer(items, many=True)
                    drinks[category.name] = serializer.data
                else:
                    print(
                        "WARNING: No items in category: "
                        + category.name
                        + "-"
                        + str(category.id)
                        + " for menu: "
                        + str(pk)
                        + " skipping..."
                    )
        response["food"] = food
        response["drinks"] = drinks
        serializer = ItemSerializer(items, many=True)
        return HttpResponse(json.dumps(response), content_type="application/json")

    @action(
        methods=["get"],
        detail=True,
        url_path="homepageCards",
        url_name="homepage_cards",
    )
    def get_homepage_cards(self, request, pk=None):
        response = dict()
        rows = HopmePageRow.objects.filter(menu=pk).order_by("order")
        for row in rows:
            row.cards = HomepageCard.objects.filter(row=row).order_by("order")
            serializer = HomepageCardSerializer(row.cards, many=True)
            response[row.title] = serializer.data
        return HttpResponse(json.dumps(response), content_type="application/json")
        # obj = HomepageCard.objects.filter(menu=Menu.objects.get(pk=pk))
        # serializer = HomepageCardSerializer(obj, many=True)
        # return HttpResponse(json.dumps(serializer.data), content_type="application/json")

    @action(methods=["get"], detail=True, url_path="complaints", url_name="complaints")
    def get_complaints(self, request, pk=None):
        obj = Complaint.objects.filter(menu=Menu.objects.get(pk=pk))
        serializer = ComplaintSerializer(obj, many=True)
        return HttpResponse(
            json.dumps(serializer.data), content_type="application/json"
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "menu",
            "isFood",
        ]

class CategorySerializerTotalItems(serializers.ModelSerializer):
    totalItems = serializers.SerializerMethodField()
    def get_totalItems(self, obj):
        return Item.objects.filter(category=obj).count()
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "menu",
            "isFood",
            "totalItems"
        ]



@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "put", "post", "delete"]

    @action(methods=["get"], detail=True, url_path="items", url_name="items")
    def get_items(self, request, pk=None):
        items = Item.objects.filter(category=Category.objects.get(pk=pk))
        serializer = ItemSerializer(items, many=True)
        return HttpResponse(
            json.dumps(serializer.data), content_type="application/json"
        )


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
            "isAvailable",
        ]

    def get_photo(self, obj):
        return obj.b2StorageFile.url

    def create(self, validated_data):
        filename = validated_data["b2StorageFile"].name
        if re.search("^(?!.*\.\.)[\w-]+\.(svg|jpe?g|png|gif|bmp)$", filename) == False:
            raise serializers.ValidationError("Invalid filename")
        return super().create(validated_data)


@extend_schema(tags=["Item"])
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("id")
    serializer_class = ItemSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            try:
                user = User.objects.get(username=self.request.user)
            except  User.DoesNotExist:
                user = None
            print(user)
            self.permission_classes = [permissions.IsAuthenticated,]
        return super(ItemViewSet, self).get_permissions()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete"]


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "restaurant", "number", "seats"]


@extend_schema(tags=["Table"])
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("id")
    serializer_class = TableSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete"]

    @action(methods=["post"], detail=True, url_path="new_cart", url_name="new_cart")
    def createCart(self, request, pk=None):
        table = Table.objects.get(pk=pk)
        try:
            cart = Cart.objects.get(table=table)
            if cart.status == "Closed":
                cart.empty()
            return HttpResponse(
                json.dumps(model_to_dict(cart), default=str),
                content_type="application/json",
            )
        except Cart.DoesNotExist:
            cart = Cart.objects.create(table=table)
            table.cart = cart
            table.save()
            return HttpResponse(
                json.dumps(model_to_dict(cart), default=str),
                content_type="application/json",
            )


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total",
            "table",
            "status",
            "table",
            "created_at",
            "closed_at",
        ]


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("id")
    serializer_class = CartSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]

    @action(methods=["put"], detail=True, url_path="add_item", url_name="add_item")
    @transaction.atomic
    def addItem(self, request, pk=None):
        cart = Cart.objects.get(pk=pk)
        if cart.status != "Open":
            raise serializers.ValidationError("Cart is not open")
        item = Item.objects.get(pk=request.data["item"])
        cart.items.append(item.id)
        cart.total += item.price
        cart.save()
        return HttpResponse(
            json.dumps(model_to_dict(cart), default=str),
            content_type="application/json",
        )

    @action(
        methods=["put"], detail=True, url_path="remove_item", url_name="remove_item"
    )
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
            return HttpResponse(
                json.dumps(model_to_dict(cart), default=str),
                content_type="application/json",
            )
        else:
            raise serializers.ValidationError("Item not in cart")

    @action(methods=["post"], detail=True, url_path="checkout", url_name="checkout")
    @transaction.atomic
    def checkout(self, request, pk=None):
        cart = Cart.objects.get(pk=pk)
        cart.status = "Checkout"
        cart.save()
        return HttpResponse(
            json.dumps(model_to_dict(cart), default=str),
            content_type="application/json",
        )

    @action(methods=["post"], detail=True, url_path="close", url_name="close")
    @transaction.atomic
    def pay(self, request, pk=None):
        cart = Cart.objects.get(pk=pk)
        cart.closed_at = datetime.now(cart.created_at.tzinfo)
        cart.status = "Closed"
        cart.save()
        table = Table.objects.get(cart=cart)
        start = cart.created_at
        end = cart.closed_at
        tat = (end - start).total_seconds() / 60
        Order.objects.create(
            restaurant=table.restaurant,
            table=table,
            items=cart.items,
            total=cart.total,
            payment_method=request.data["payment_method"],
            tip=request.data["tip"],
            time_at_table=tat,
        )
        connection.close()
        return HttpResponse(
            json.dumps(model_to_dict(cart), default=str),
            content_type="application/json",
        )


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
        if re.search("^(?!.*\.\.)[\w-]+\.(svg|jpe?g|png|gif|bmp)$", filename) == False:
            raise serializers.ValidationError("Invalid filename")
        return super().create(validated_data)


@extend_schema(tags=["Story"])
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by("id")
    serializer_class = StorySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]


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
        fields = {"menu": ["exact"]}


@extend_schema(tags=["Review"])
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("id")
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]


class HomepageCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageCard
        fields = [
            "id",
            "title",
            "row",
            "order",
            "size",
            "b2StorageFile",
            "active",
            "links_to",
            "created_at",
        ]


@extend_schema(tags=["HomepageCard"])
class HomepageCardViewSet(viewsets.ModelViewSet):
    queryset = HomepageCard.objects.all().order_by("id")
    serializer_class = HomepageCardSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]


class HopmePageRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = HopmePageRow
        fields = ["id", "title", "menu", "created_at", "updated_at", "order"]


@extend_schema(tags=["HopmePageRow"])
class HopmePageRowViewSet(viewsets.ModelViewSet):
    queryset = HopmePageRow.objects.all().order_by("id")
    serializer_class = HopmePageRowSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]

    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def check_user(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        return user
    
class UserLogin(APIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = UserLoginSerializer
    def post(self, request):
        try:
            data = request.data
            assert validate_username(data) 
            assert validate_password(data)
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid():
                user = serializer.check_user(data)
                login(request, user)
                retUser = User.objects.get(username=user)
                response = json.dumps({
                    "id": retUser.id, 
                    "email": retUser.email, 
                    "username": retUser.username,
                    "firstName": retUser.first_name,
                    "lastName": retUser.last_name,
                    "isStaff": retUser.is_staff}, default=str)
                return HttpResponse(response, content_type="application/json") 
        except:
            return HttpResponse(status=403)
        
class UserLogout(APIView):
    authentication_classes = []
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
class UserMe(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        response = {}
        response["profile"] = ProfileSerializer(Profile.objects.get(user=request.user)).data
        response["profile"]["user"] = serializer.data
        print(response)
        return HttpResponse(json.dumps(response["profile"]), content_type="application/json")

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ["id", "menu", "table", "title", "description", "created_at"]

@extend_schema(tags=["Complaint"])
class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().order_by("id")
    serializer_class = ComplaintSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete", "put"]
