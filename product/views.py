from .serializers import *
from .models import Product, SubCategory
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import Q
from django.core import serializers
from UserAuthentication.renderers import JSONRenderer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny, )


# class ProductListView(APIView):
#     permission_classes = (permissions.AllowAny, )
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get(self, request):
#         serializer = ProductSerializer(data=self.queryset, many=True)

#         if(serializer.is_valid()):
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SearchProduct(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def get(self, request, query, format=None):

        # searching matching products from both title,  description, category and subCategory
        queryset = Product.objects.filter(Q(productName__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query) | Q(subCategory__icontains=query))


        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProduct(RetrieveAPIView):
    queryset = Product.objects.all()
    lookup_field = 'productId'
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class FilterProduct(APIView):

    seriaizer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def get(self, request, filterQuery):
        
        queryset = Product.objects.filter(category=filterQuery)

        serializer = self.seriaizer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)