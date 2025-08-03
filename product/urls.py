from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='home'),
    path('index.html',views.index,name='home_html'),
    path('products_details/<pk>', views.detail_products, name='detail_products'),
    path('products', views.list_products, name='product_list'),
    path('products_list',views.list_products,name='products')
]
