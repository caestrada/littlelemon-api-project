from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


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
    
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "This is a secret message!"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        return Response({"message": "Only Managers could see this!"})
    else:
        return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data.get('username')
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response({"message": "ok"})
    
    return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)