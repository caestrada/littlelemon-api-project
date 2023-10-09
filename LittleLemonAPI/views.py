from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer

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

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)



class OrderList(viewsets.ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        if self.request.user.is_superuser or request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.groups.filter(name="Delivery crew").exists():
            orders = Order.objects.all().filter(delivery_crew=self.request.user) 
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Customer's orders
        orders =  Order.objects.all().filter(user=self.request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message:": "Cart is empty"})
        
        data = request.data.copy()
        total = self.__get_total_price(self.request.user)
        data["total"] = total
        data["user"] = self.request.user.id
        from datetime import datetime
        current_date = datetime.now().date()
        data["date"] = current_date.strftime('%Y-%m-%d')
        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id=item["menuitem_id"],
                    price=item["price"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"]
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete()

            result = order_serializer.data.copy()
            result["total"] = total
            return Response(order_serializer.data)
        else:
            # If the serializer is not valid, return errors
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def __get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item["price"]
        return total



class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Manager or superuser
        if (self.request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return super().update(request, *args, **kwargs)

        # Delivery crew (PATCH)
        partial = kwargs.get('partial', False)
        if partial and 'status' in request.data and self.request.user.groups.filter(name="Delivery crew").exists():
            return super().update(request, *args, **kwargs)
        
        # Customer
        return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, *args, **kwargs):
        if (self.request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return super().destroy(request, *args, **kwargs)
        
        return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)



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



class GroupsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __get_group(self, url_path):
        group = "Manager" if "manager" in url_path else "Delivery crew"
        return group

    def list(self, request):
        group = self.__get_group(request.path)

        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            managers = Group.objects.get(name=group)
            return Response([user.username for user in managers.user_set.all()], status=status.HTTP_200_OK)
        
        return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        group = self.__get_group(request.path)
        if not request.user.groups.filter(name=group).exists() and not request.user.is_superuser:
            return Response({"message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name=group)
            managers.user_set.add(user)
            return Response({"message": f"User added to {group} group"})
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)



class SingleGroupsView(generics.DestroyAPIView):
    def __get_group(self, url_path):
        group = "Manager" if "manager" in url_path else "Delivery crew"
        return group

    def destroy(self, request, userId):
        group = self.__get_group(request.path)
        user = get_object_or_404(User, id=userId)
        if user:
            managers = Group.objects.get(name=group)
            managers.user_set.remove(user)
            return Response({"message": f"User removed from {group} group"})
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response({'message': 'Cart emptied'})