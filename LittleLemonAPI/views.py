from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

@api_view(['GET', 'POST'])
def menu_items(request):
    return Response('List of menu items', status=status.HTTP_200_OK)

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