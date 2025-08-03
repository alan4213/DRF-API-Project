# from django.shortcuts import render,redirect
# from .models import Order,OrderItems
# from django.contrib import messages
# from product.models import Product
# from django.contrib.auth.decorators import login_required
# import razorpay
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseBadRequest, HttpResponse
# from .forms import AddressForm
# import requests
# def show_cart(request):

#     user=request.user

#     customer=user.customer_profile

#     cart_obj, created=Order.objects.get_or_create(order_status=Order.CART_STAGE,owner=customer)


#     previous_orders = Order.objects.filter(
#         owner=customer,
#         order_status__gte=Order.ORDER_CONFIRMED
#     ).exclude(shipping_name__isnull=True).distinct()
    
#     form = AddressForm(instance=cart_obj)

#     context={'cart':cart_obj,'form': form, 'saved_addresses': previous_orders}

#     return render(request, 'cart.html',context)

# @login_required(login_url='show_account')
# def add_to_cart(request):

#     if request.POST:
#         user=request.user

#         customer=user.customer_profile

#         product_id=request.POST.get('product_id')

#         quantity=int(request.POST.get('quantity'))

#         cart_obj,created=Order.objects.get_or_create(order_status=Order.CART_STAGE, owner=customer)

#         product=Product.objects.get(pk=product_id)

#         ordered_item,created=OrderItems.objects.get_or_create(product=product,owner=cart_obj) 
#         if created:
#             ordered_item.quantity=quantity
#             ordered_item.save()
#         else:
#             ordered_item.quantity=ordered_item.quantity+quantity 
#             ordered_item.save() 
#         return redirect('show_cart')
# def remove_from_cart(request,pk): 
    
#     item=OrderItems.objects.get(pk=pk)

#     if request.POST:

#         action = request.POST.get('action')

#         if action == 'increase':
#             item.quantity += 1
#             item.save()
#         elif action == 'decrease':
#             if item.quantity > 1: 
#                 item.quantity -= 1 
#                 item.save()

#             else:
#                 item.delete()
#         elif action=='remove':
#             item.delete()

#     else:
#         if item:
#             item.delete() 
#     return redirect('show_cart')

# def checkout_cart(request):

#     if request.method =="POST":

#         try:

#             user =request.user

#             customer = user.customer_profile

#             total = float(request.POST.get('total'))*100

#             # convert to paise

#             # Initialize Razorpay client

#             client = razorpay.Client (auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             razorpay_order = client.order.create({

#             "amount": int(total),

#             "currency": "INR",

#             "payment_capture": 1,})

#             order_obj = Order.objects.get(owner=customer, order_status=Order.CART_STAGE)

#             order_obj.razorpay_order_id = razorpay_order['id']

#             order_obj.total_price=total/100

#             order_obj.save()

#             context = {


#             "razorpay_order_id": razorpay_order['id'],

#             "razorpay_key": settings.RAZORPAY_KEY_ID,

#             "amount": int(total),

#             "user": user,

#             "customer": customer,
#             }
#             return render(request, "razorpay_checkout.html", context)

#         except Exception as e:

#             messages.error(request, "Unable to initiate payment: "+ str(e))

#             return redirect('show_cart')



# @login_required(login_url='show_account')
# def show_orders(request):
#     user=request.user

#     customer=user.customer_profile

#     all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
#     context={'orders':all_orders}
#     return render(request, 'orders.html', context)


# def payment_success(request):

#     if request.method == "POST":



#         try:

#         #Get Razorpay payment data from the POST request 
#             razorpay_payment_id = request.POST.get('razorpay_payment_id') 
#             razorpay_order_id = request.POST.get('razorpay_order_id') 
#             razorpay_signature = request.POST.get('razorpay_signature')

#             # Verify payment signature

#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             params_dict = {

#             'razorpay_order_id': razorpay_order_id,

#             'razorpay_payment_id': razorpay_payment_id,

#             'razorpay_signature': razorpay_signature}

#             client.utility.verify_payment_signature(params_dict)
#             order_obj = Order.objects.get(razorpay_order_id=razorpay_order_id)

#             order_obj.order_status = Order.ORDER_CONFIRMED

#             order_obj.save()

#             shiprocket_result = create_shiprocket_order(order_obj)


#             return render(request, 'payment_verified.html',{

#             'payment_id': razorpay_payment_id,

#             'order_id': razorpay_order_id,

#             'shiprocket_result': shiprocket_result})

#         except razorpay.errors.SignatureVerificationError:

#             return HttpResponseBadRequest ("Payment verification failed")

#     return HttpResponseBadRequest ("Invalid request")

# def shipping(request):

#     if request.method == 'POST':

#         user = request.user
#         customer= user.customer_profile
#         cart_obj = Order.objects.get(order_status=Order.CART_STAGE, owner=customer)
#         form=AddressForm(request.POST, instance=cart_obj)
#         if form.is_valid():
#             form.save()
#             return redirect('show_cart')
#     else:
#         user = request.user
#         customer= user.customer_profile
#         cart_obj,created = Order.objects.get(order_status=Order.CART_STAGE, owner=customer)
#         form=AddressForm(instance=cart_obj)
#     return render(request, 'cart_content.html', {'form': form})

# def create_shiprocket_order(order):

#     url= "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc" 
#     headers= {"Authorization": f"Bearer {settings.SHIPROCKET_TOKEN}",

#     "Content-Type": "application/json"}

#     payload={

#     "order_id": str(order.id),

#     "order_date": str(order.created_at.date()),

#     "pickup_location": "Primary",

#     "channel_id": "",

#     "comment": "Test Order",

#     "billing_customer_name": order.shipping_name,

#     "billing_last_name": "",

#     "billing_address": order.shipping_address,
#     "billing_address_2": "",

#     "billing_city": order.shipping_city,
#     "billing_pincode": order.shipping_pincode,
#     "billing_state": order.shipping_state,
#     "billing_country": order.shipping_country,
#     "billing_email": order.shipping_email,
#     "billing_phone": order.shipping_phone,

#     "shipping_is_billing": True,

#     "order_items": [{



#     "name": item.product.title,

#     "sku": f"SKU-{item.product.id}",

#     "units": item.quantity,

#     "selling_price": float(item.product.price),

#     "discount": "",

#     "hsn": 441122
#     }
#     for item in order.order_items.all()
#     ],

#     "payment_method": "Prepaid",

#     "shipping_charges": 0,

#     "giftwrap_charges": 0,

#     "transaction_charges": 0,

#     "total_discount": 0,

#     "sub_total": float(order.total_price),

#     "length": 10,

#     "breadth": 10,

#     "height": 10,

#     "weight": 0.5

#     }
#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()  # Raise an exception for 4XX/5XX responses
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Shiprocket API Error: {str(e)}")
#         if 'response' in locals():
#             print(f"Response: {response.text}")
#             return {"error": str(e), "details": response.text}
#         return {"error": str(e)}
# Add these imports at the top
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItems
from product.models import Product
# Add these classes at the end
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(
            owner=self.request.user.customer_profile,
            delete_status=Order.LIVE
        ).exclude(order_status=Order.CART_STAGE)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    customer = request.user.customer_profile
    cart, created = Order.objects.get_or_create(
        order_status=Order.CART_STAGE,
        owner=customer
    )
    serializer = OrderSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart_api(request):
    customer = request.user.customer_profile
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    
    cart, created = Order.objects.get_or_create(
        order_status=Order.CART_STAGE,
        owner=customer
    )
    
    product = Product.objects.get(pk=product_id)
    item, created = OrderItems.objects.get_or_create(
        product=product,
        owner=cart
    )
    
    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity
    item.save()
    
    return Response({'message': 'Item added to cart'})
@api_view(['POST'])  # Only accepts POST requests
@permission_classes([IsAuthenticated])  # Must be logged in
def update_cart_item(request):
    item_id = request.data.get('item_id')  # Get item ID from request data
    quantity = int(request.data.get('quantity'))  # Get new quantity as integer
    
    try:
        item = OrderItems.objects.get(  # Find the specific cart item
            pk=item_id,  # With this ID
            owner__owner=request.user.customer_profile,  # Belongs to current user
            owner__order_status=Order.CART_STAGE  # In cart (not confirmed order)
        )
        
        if quantity > 0:  # If quantity is positive
            item.quantity = quantity  # Update quantity
            item.save()  # Save changes to database
            return Response({'message': 'Item updated'})  # Success response
        else:  # If quantity is 0 or negative
            item.delete()  # Remove item from cart
            return Response({'message': 'Item removed'})  # Success response
            
    except OrderItems.DoesNotExist:  # If item not found
        return Response({'error': 'Item not found'}, status=404)  # Error response
@api_view(['DELETE'])  # Only accepts DELETE requests
@permission_classes([IsAuthenticated])  # Must be logged in
def remove_cart_item(request, item_id):  # item_id comes from URL parameter
    try:
        item = OrderItems.objects.get(  # Find the cart item
            pk=item_id,  # With this ID
            owner__owner=request.user.customer_profile,  # Belongs to current user
            owner__order_status=Order.CART_STAGE  # In cart stage
        )
        item.delete()  # Remove item from database
        return Response({'message': 'Item removed from cart'})  # Success response
        
    except OrderItems.DoesNotExist:  # If item not found
        return Response({'error': 'Item not found'}, status=404)  # Error response
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    customer = request.user.customer_profile
    print(f"DEBUG CHECKOUT: Customer = {customer}")
    
    try:
        cart = Order.objects.get(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        print(f"DEBUG CHECKOUT: Found cart = {cart}, status = {cart.order_status}")
        
        # Calculate total
        total = sum(item.product.price * item.quantity for item in cart.order_items.all())
        print(f"DEBUG CHECKOUT: Calculated total = {total}")
        
        # Update cart to confirmed order
        cart.order_status = Order.ORDER_CONFIRMED
        cart.total_price = total
        cart.save()
        
        print(f"DEBUG CHECKOUT: After save - status = {cart.order_status}")
        
        return Response({
            'message': 'Order placed successfully',
            'order_id': cart.id,
            'total': total
        })
        
    except Order.DoesNotExist:
        print("DEBUG CHECKOUT: No cart found!")
        return Response({'error': 'Cart is empty'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    customer = request.user.customer_profile
    
    # Debug: Get ALL orders first
    all_orders = Order.objects.filter(owner=customer)
    print(f"DEBUG: All orders for customer {customer}: {list(all_orders)}")
    
    # Check each order status
    for order in all_orders:
        print(f"DEBUG: Order {order.id}: status={order.order_status}, delete_status={order.delete_status}")
    
    # Original filtering
    orders = Order.objects.filter(
        owner=customer,
        delete_status=Order.LIVE
    ).exclude(order_status=Order.CART_STAGE).order_by('-created_at')
    
    print(f"DEBUG: Filtered orders: {list(orders)}")
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    customer = request.user.customer_profile
    
    try:
        order = Order.objects.get(
            id=order_id,
            owner=customer,
            delete_status=Order.LIVE
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
