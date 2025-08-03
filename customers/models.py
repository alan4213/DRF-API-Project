from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer (models.Model):

    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE, 'Live'), (DELETE, 'Delete'))

    phone=models.CharField(max_length=10)

    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name="customer_profile")

    delete_status=models.IntegerField(choices=DELETE_CHOICES, default=LIVE)

    name=models.CharField(max_length=100)

    address=models.TextField()

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now_add=True)

    def str (self):

     return self.user.username

