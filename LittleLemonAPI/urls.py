from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("categories", views.CategoriesView.as_view()),
    path("categories/<int:pk>", views.SingleCategoryView.as_view()),
    path("menu-items", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("orders", views.OrderList.as_view({'get': 'list', 'post': 'create'})),
    path("orders/<int:pk>", views.OrderDetail.as_view()),
    path("secret", views.secret),
    path('api-token-auth', obtain_auth_token),
    path('manager-view', views.manager_view),
    path('groups/manager/users', views.GroupsViewSet.as_view( {'get': 'list', 'post': 'create'})),
    path('groups/manager/users/<int:userId>', views.SingleGroupsView.as_view()),
    path('groups/delivery-crew/users', views.GroupsViewSet.as_view( {'get': 'list', 'post': 'create'})),
    path('groups/delivery-crew/users/<int:userId>', views.SingleGroupsView.as_view()),
    path("cart/menu-items", views.CartView.as_view()),
]