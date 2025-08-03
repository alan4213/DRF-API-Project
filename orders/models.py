from django.db import models
from customers.models import Customer
from product.models import Product

# Create your models here.

class Order(models.Model):

    LIVE=1

    DELETE=0

    DELETE_CHOICES=((LIVE, 'Live'), (DELETE, 'Delete'))

    CART_STAGE=0

    ORDER_CONFIRMED=1

    ORDER_PROCESSED=2

    ORDER_DELIVERED=3

    ORDER_REJECTED=4

    STATUS_CHOICE = (
    (CART_STAGE, 'CART_STAGE'),
    (ORDER_CONFIRMED, 'ORDER_CONFIRMED'),  # Add this line
    (ORDER_PROCESSED, 'ORDER_PROCESSED'), 
    (ORDER_DELIVERED, 'ORDER_DELIVERED'), 
    (ORDER_REJECTED, 'ORDER_REJECTED')
)


    order_status=models.IntegerField(choices=STATUS_CHOICE, default=CART_STAGE)

    owner=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="orders")
    razorpay_order_id=models.CharField(max_length=20, null=True)

    delete_status=models.IntegerField(choices=DELETE_CHOICES, default=LIVE)

    total_price=models.FloatField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now_add=True)

    shipping_name = models.CharField(max_length=100, null=True)

    shipping_phone = models.CharField(max_length=15, null=True)

    shipping_email = models.EmailField(null=True)

    shipping_address = models.TextField(null=True)

    shipping_city = models.CharField(max_length=50, null=True)

    shipping_state = models.CharField(max_length=50, null=True)

    shipping_pincode = models.CharField(max_length=6,null=True)

    shipping_country = models.CharField(max_length=50, default="India", null=True)

    def str (self):
        if self.owner and self.owner.user:
          return "Order-{}-{}".format(self.id, self.owner.user.username)

        else:
          return "order-{}".format(self.id)




class OrderItems (models.Model):

    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='added_carts') 
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')