# from django.shortcuts import render,redirect
# from django.contrib.auth import logout
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from django.contrib import messages
# from .models import Customer
# from django.contrib.auth import login
# from django.contrib.auth import logout
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site




# # Create your views here.
# def sign_out(request):
#     logout(request)
#     return redirect('home')
# def show_account(request):


#     context={} 
#     if request.POST and 'register' in request.POST: 
#         context['register']=True 
#         username=request.POST.get('username') 
#         password=request.POST.get('password') 
#         email=request.POST.get('email') 
#         phone=request.POST.get('phone') 
#         address=request.POST.get('address')

#         try:

#             user=User.objects.create_user(username=username, password=password, email=email)

#             user.is_active = False # Keep inactive until email verificz 
#             user.save()

#             customer=Customer.objects.create(name=username,user=user,phone=phone,address=address)



#             # Send verification email

#             current_site = get_current_site(request)

#             mail_subject = 'Activate your Prokart account'

#             message = render_to_string('activation_email.html',{ 
#             'user': user,'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': default_token_generator.make_token(user),
#              })

#             email_msg = EmailMessage(mail_subject, message, to=[email])
#             email_msg.send()

#             success_msg="Reeistration successfull Please check vour email to activate your account"
#             messages.success(request,success_msg)
#         except Exception as e:
#             print(f"Registration error: {str(e)}")

#             error_msg="Registration failed. Username might already exist." 
#             messages.error(request, error_msg)
#     if request.POST and 'login' in request.POST:

#         context['register']=False

#         username=request.POST.get('username')

#         password=request.POST.get('password')

#         user=authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                   login(request, user)
#                   return redirect('home')
#             else:
#                 error_msg="Please activate your account first. Check your email."
#                 messages.error(request, error_msg)
#         else:
#             error_msg="Invalid credentials"
#             messages.error(request, error_msg)
#     return render(request,"account.html",context)

# from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_str


# def activate_account(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))

#         user = User.objects.get(pk=uid)

#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):

#         user = None



#     if user is not None and default_token_generator.check_token(user, token):

#         user.is_active = True

#         user.save()

#         messages.success(request, 'Your account has been activated successfullyl You can now login')
#         return redirect('show_account')
#     else:


#         messages.error(request, 'Activation link is invalid!')
#         return redirect('show_account')
# customers/views.py
from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(delete_status=Customer.LIVE)
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        queryset = Customer.objects.filter(delete_status=Customer.LIVE)
        phone = self.request.query_params.get('phone')
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        return queryset


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'User exists'}, status=400)
    
    user = User.objects.create_user(username=username, password=password)
    Customer.objects.create(name=username, user=user)
    
    return Response({'message': 'User created'})

