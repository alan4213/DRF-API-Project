from django.urls import path
from .import views
urlpatterns = [

path('cart',views.show_cart, name='show_cart'),

path('add_to_cart', views.add_to_cart, name='add_to_cart'),

path('remove_item/<pk>', views.remove_from_cart, name='remove_from_cart'),

path('checkout', views.checkout_cart, name='checkout'),

path('orders', views.show_orders,name='orders'),

path('payment/success/', views.payment_success, name='payment_success'),

path('shipping',views.shipping, name='shipping'),]

