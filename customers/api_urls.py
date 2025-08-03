from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import ObtainAuthToken 
router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/',ObtainAuthToken.as_view()),
    path('api/register/', views.register, name='register')
]
