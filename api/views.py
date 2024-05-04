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
)
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
import re
from django.db import transaction
from datetime import datetime
from django.db import connection
import django_filters as filters
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


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
        ]


@extend_schema(tags=["Menu"])
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by("id")
    serializer_class = MenuSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete"]

    @action(methods=["get"], detail=True, url_path="categories", url_name="categories")
    def get_catgories(self, request, pk=None):
        obj = Category.objects.filter(menu=Menu.objects.get(pk=pk))
        serializer = CategorySerializer(obj, many=True)
        connection.close()
        return HttpResponse(
            json.dumps(serializer.data), content_type="application/json"
        )

    @action(methods=["get"], detail=True, url_path="stories", url_name="stories")
    def get_stories(self, request, pk=None):
        obj = Story.objects.filter(menu=Menu.objects.get(pk=pk))
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
        rows = HopmePageRow.objects.filter(menu=pk)
        for row in rows:
            row.cards = HomepageCard.objects.filter(row=row)
            serializer = HomepageCardSerializer(row.cards, many=True)
            response[row.title] = serializer.data
        return HttpResponse(json.dumps(response), content_type="application/json")
        # obj = HomepageCard.objects.filter(menu=Menu.objects.get(pk=pk))
        # serializer = HomepageCardSerializer(obj, many=True)
        # return HttpResponse(json.dumps(serializer.data), content_type="application/json")


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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "delete"]

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
            "size",
            "b2StorageFile",
            "text",
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
        fields = ["id", "title", "menu", "created_at", "updated_at"]


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
        print("username: ", username, "password: ", password)
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        return user
    
class UserLogin(APIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = UserLoginSerializer
    def post(self, request):
        data = request.data
        assert validate_username(data) 
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.check_user(data)
            login(request, user)
            return HttpResponse(serializer.data, content_type="application/json")
        
class UserLogout(APIView):
    @csrf_exempt
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
class UserMe(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")

# @extend_schema(tags=["User"])
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by("id")
#     serializer_class = UserSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     http_method_names = ["get", "post"]

#     @action(methods=["get"], detail=False, url_path="me", url_name="me")
#     def get_self(self, request):
#             try:
#                 user = get_object_or_404(User, username=request.user)
#             except User.DoesNotExist:
#                 user = None
#             if user is None and request.user.is_authenticated:
#                 response = json.dumps({
#                     "id": user.id,
#                     "email":user.email,
#                     "username": user.username
#                     }, default=str)
#                 return HttpResponse(response, content_type="application/json")
#             else:
#                 return HttpResponse(json.dumps({"status": "fail"}), content_type="application/json", status=401)
    
#     @action(methods=["post"], detail=False, url_path="login", url_name="login")
#     def login(self, request):
#         password = request.data["password"] 
#         print(password)
#         if "username" in request.data:
#             username = request.data["username"]
#         elif "email" in request.data:
#             email = request.data["email"]
#             username = get_object_or_404(User, email=email).username
#         else:
#             return HttpResponse(json.dumps({"status": "fail"}), content_type="application/json")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             response = json.dumps({
#                 "id": user.id,
#                 "email":user.email,
#                 "username": user.username
#             }, default=str)
#             return HttpResponse(response, content_type="application/json")
#         else:
#             return HttpResponse(json.dumps({"status": "fail"}), content_type="application/json", status=401)

    
    # @action(methods=["post"], detail=False, url_path="logout", url_name="logout")
    # def logout(self, request):
    #     logout(request)
    #     return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")