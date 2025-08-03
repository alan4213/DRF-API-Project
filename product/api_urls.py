from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/products-simple/', views.product_list_api, name='product-list-simple')]
