from django.urls import path
from . import views
urlpatterns = [
    path("categories/", views.CategoriesView.as_view()),
    path("menu-items/", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("orders", views.OrderList.as_view()),
    path("orders/<int:pk>", views.OrderDetail.as_view()),
]