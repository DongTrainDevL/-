from django.urls import path
from . import views
from django.conf import settings  
from django.conf.urls.static import static 




urlpatterns = [
    #path("", views.home),
    path("fromloginadmin", views.fromloginadmin, name="fromlogin"),
    path("login_admin_from",views.loginadmin_from,name="login_admin_from"),
    path('mydashboard/',views.mydashboard,name="mydashboard"),
    path('myadmin/',views.myadmin, name='myadmin'),
    path('loginadmin/',views.admin_login, name='admin_login'),
    path('logoutadmin/',views.adminlogout, name='adminlogout'),
    path('member/',views.member, name='member'),
    path('from_member/',views.from_member, name='from_member'),
    path('edit_member/<int:id>/edit/',views.edit_member, name='edit_member'),

    path('fromloginchef',views.fromloginchef,name='fromlogincehf'),
    path('mychef/',views.mydashboard_chef,name="mychef"),
    #path('update_order_status/', views.update_order_status, name='update_order_status'),
   
    path('Order/',views.Order,name="Order"),
    #path('addcustomer/',views.customer,name="addcustomer"),
    path('mydashboardedit/',views.mydashboard_edit,name="mydashboardedit"),
    path("delete/<int:id>", views.delete, name="delete"),
    path('product/', views.product_, name='product'),
    path('formproduct/',views.form_product, name="formproduct"),
    path('addproduct/',views.product_add, name="addproduct"),
    path("delete_product/<int:id>",views.delate_product,name='delete_product'),
    
    path('from_edit_product',views.from_edit_product,name="from_edit_product"), 
    path('product/<int:id>/edit/', views.edit_product, name='edit_product'),
    

    
    #path("update/<int:id>", views.update, name="update"),
    #path("updaterecord/<int:id>", views.updaterecord, name="updaterecord"),
    
 
    
]

