from django.contrib import admin
from .models import Member,Food,Customer,Order,OrderItem,Cart,CartItem,Chef


# Register your models here.

class registerAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email','show_image']
    


admin.site.register(Member)
#admin.site.register(registerAdmin)
admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Chef)

