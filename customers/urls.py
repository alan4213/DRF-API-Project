from django.urls import path
from . import views
urlpatterns=[path('account',views.show_account,name='show_account'),
             path('logout', views.sign_out, name='logout'),
             path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),]

