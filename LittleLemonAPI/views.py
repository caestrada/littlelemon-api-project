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

from rest_framework import viewsets


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
    
class SingleCategoryView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ['category__title']

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)

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
    
# @api_view(['POST', 'DELETE'])
# @permission_classes([IsAdminUser])
# def managers(request):
#     username = request.data.get('username')
#     if username:
#         user = get_object_or_404(User, username=username)
#         managers = Group.objects.get(name='Manager')

#         if request.method == 'POST':
#             managers.user_set.add(user)
#         elif request.method == 'DELETE':
#             managers.user_set.remove(user)
#         return Response({"message": "ok"})
    
#     return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

class ManagersViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        managers = Group.objects.get(name='Manager')
        return Response([user.username for user in managers.user_set.all()], status=status.HTTP_200_OK)

    def create(self, request):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return Response({"message": "User added to managers group"})
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.remove(user)
            return Response({"message": "User removed from managers group"})
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)