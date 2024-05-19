"""
URL configuration for PlatePalDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from api.views import CategoryViewSet, MenuViewSet, RestaurantViewSet, ItemViewSet, OrderViewSet, TableViewSet, CartViewSet, StoryViewSet, ReviewViewSet, HomepageCardViewSet, HopmePageRowViewSet, UserLogin, UserLogout, UserMe, ProfileViewSet, ComplaintViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'item', ItemViewSet)
router.register(r'order', OrderViewSet)
router.register(r'table', TableViewSet)
router.register(r'cart', CartViewSet)
router.register(r'story', StoryViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'homepage-card', HomepageCardViewSet)
router.register(r'homepage-row', HopmePageRowViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'complaint', ComplaintViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    #path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('me/', UserMe.as_view(), name='me'),
]
