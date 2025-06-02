"""
URL configuration for online_shopping_supermarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from groceryapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('index/', index, name="index"),
    path('about/', about, name="about"),
    path('main/', main, name="main"),
    path('admin-login/', adminLogin, name="admin_login"),
    path('adminhome/', adminHome, name="adminhome"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    path('add-category/', add_category, name="add_category"),
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pid>/', edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', delete_category, name="delete_category"),
    path('add-product/', add_product, name='add_product'),
    path('view-product/', view_product, name='view_product'),
    path('edit-product/<int:pid>/', edit_product, name="edit_product"),
    path('delete-product/<int:pid>/', delete_product, name="delete_product"),
    path('registration/', registration, name="registration"),
    path('userlogin/', userlogin, name="userlogin"),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('profile/', profile, name="profile"),
    path('logout/', logoutuser, name="logout"),
    path('change-password/', change_password, name="change_password"),
    path('user-product/<int:pid>/', user_product, name="user_product"),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('incredecre/<int:pid>/', incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    path('booking/', booking, name="booking"),
    path('my-order/', myOrder, name="myorder"),
    path('user-order-track/<int:pid>/', user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),
    path('user-feedback/', user_feedback, name="user_feedback"),
    path('manage-feedback/', manage_feedback, name="manage_feedback"),
    path('delete-feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
    path('payment/', payment, name="payment"), 
    path('payment/verify/',verify_payment, name='verify_payment'),
    path('manage-order/', manage_order, name="manage_order"),
    path('delete-order/<int:pid>/', delete_order, name="delete_order"), 
    path('admin-order-track/<int:pid>/', admin_order_track, name="admin_order_track"),
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
    path('mark-feedback-read/<int:pid>/', mark_feedback_read, name='mark_feedback_read'),
    path('contact/', contact, name="contact"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



