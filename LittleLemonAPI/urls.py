from django.urls import path
from . import views
urlpatterns = [
    path('menu-items/', views.menu_items),
    path("orders", views.OrderList.as_view()),
    path("orders/<int:pk>", views.OrderDetail.as_view()),

]