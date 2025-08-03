from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/cart/', views.get_cart, name='get-cart'),
    path('api/add-to-cart/', views.add_to_cart_api, name='add-to-cart'),
    path('api/cart/update/', views.update_cart_item, name='update_cart_item'),
    path('api/cart/item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('api/checkout/', views.checkout, name='checkout'),
    path('api/order-history/', views.order_history, name='order-history'),  # Changed this
    path('api/orders/<int:order_id>/', views.order_detail, name='order-detail'),
]
