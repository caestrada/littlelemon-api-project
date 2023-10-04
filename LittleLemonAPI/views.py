from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class OrderList(APIView):
    def get(self, request):
        return Response('List of orders', status=status.HTTP_200_OK)

    def post(self, request):
        return Response('Order created', status=status.HTTP_201_CREATED)
    
class OrderDetail(APIView):
    def get(self, request, pk):
        return Response('Order detail with id ' + str(pk), status=status.HTTP_200_OK)

    def put(self, request, pk):
        return Response('Order updated', status=status.HTTP_200_OK)

    def delete(self, request, pk):
        return Response('Order deleted', status=status.HTTP_204_NO_CONTENT)