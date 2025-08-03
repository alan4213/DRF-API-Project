# from django.shortcuts import render
# from django.core.paginator import Paginator
# from .models import Product


# def index(request):

#     featured_products=Product.objects.order_by('priority')[:4] 
#     latest_products=Product.objects.order_by('-id')[:4]
#     context={'featured_products':featured_products, 'latest_products':latest_products} 
#     return render(request,'index.html',context)
# def detail_products(request,pk):
#     product=Product.objects.get(pk=pk)
#     return render(request, 'products_details.html',{'prod_detail':product})
# def list_products(request):

#     page=1
#     query = request.GET.get('q', '') # Get search query if request.GET:
#     if request.GET:
#      page=request.GET.get('page', 1)
#     if query:
#        product_list = Product.objects.filter(
#            title_icontains=query).order_by('priority')

#     else:

#         product_list=Product.objects.order_by('priority') 
#         product_paginator = Paginator(product_list, 2) 
#         product_list=product_paginator.get_page(page) 
#         context={'products_1':product_list, 'query': query,'total_results': product_paginator.count}
#         return render(request, 'products.html', context)
# def products(request):
#     return render(request, 'products.html')

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter  # Add this import
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read for all, write for auth
    queryset = Product.objects.filter(delete_status=Product.LIVE)
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        queryset = Product.objects.filter(delete_status=Product.LIVE)
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset
@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.filter(delete_status=Product.LIVE)[:10]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)




