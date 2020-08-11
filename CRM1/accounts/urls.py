from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('settings/', views.userSetting, name="user-setting"),
    path('profile/', views.userProfile, name="user-profile"),
    path('products/', views.products, name="products"),
    path('customers/<int:pk>/', views.customers, name="customers"),
    path('order/<int:pk>/', views.createOrder, name="createOrder"),
    path('order/update/<int:pk>/', views.updateOrder, name="updateOrder"),
    path('order/delete/<int:pk>/', views.deleteOrder, name="deleteOrder"),
    path('create_customer/', views.createCustomer, name="createCustomer"),
    path('update_customer/<int:pk>/', views.updateCustomer, name="updateCustomer")
]
