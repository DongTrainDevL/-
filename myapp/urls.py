from django.urls import path,re_path
from . import views
from .views import add_to_cart
#from .views import add_to_cart,cart_list
from django.shortcuts import render
from django.conf import settings  
from django.conf.urls.static import static 




urlpatterns = [
    path("", views.home,name="home"),
    path("index", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("userlogin", views.userlogin, name="Userlogin"),
    path("from_register", views.from_register,name="from_register"),
    path("register", views.register),
    path("help", views.help, name="help"),
    path('profile_edit',views.profile_Edit,name="profile_edit"),
    # setting update user

    path('update',views.update_user,name="update"),
    path('food/',views.food,name="food"),

    path('add_to_cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('cart_list/', views.cart_list, name='cart_list'),
    path('remove_item/<int:food_id>/', views.remove_from_cart, name='remove_item'),
    #path('delete-cart-items/', views.delete_cart_items, name='delete_cart_items'),  # URL pattern สำหรับการลบรายการสินค้า
    
    path('confirm_order/',views.confirm_order, name='confirm_order'),
    path('payment',views.payment,name='payment'),
    path('your_order',views.your_order,name="your_order"),

    path('your_order_chef',views.your_order_for_chef,name='your_order_chef'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('confrim_status_order', views.confrim_status_order, name='confrim_status_order'), 

    #path('order_detail_chef', views., name='order_detail_for_chef'),
    path('from_order_detail_chef', views.from_order_detail_for_chef, name='order_detail_chef'),
    path('from_order_detail_for_check_status_order', views.from_order_detail_for_check_status_order, name='from_order_detail_for_check_status_order'),
    path('order_detail_chef/<int:order_id>/', views.order_detail_for_chef, name='order_detail_chef'),
    path('order_management/', views.order_management, name='order_management'),



    path('order_detail',views.order_detail,name='order_detail'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    # URL pattern เพื่อแสดงกราฟรายได้ร้านรายเดือน
    path('plotgrap/', views.from_plotgrap, name='plotgrap'),

    path('calculate_revenue/', views.calculate_revenue, name='calculate_revenue'),



    # URL pattern เพื่อแสดงกราฟรายได้ร้านรายปี
   
]

    
    
    


if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
