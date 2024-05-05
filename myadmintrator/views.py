from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
# from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import  login,authenticate,logout  # import form 
from django.contrib import messages 
from .models import *
from django.contrib.auth.models import User, auth,Group
from django.contrib.auth.decorators import login_required
# get data models 
from myadmintrator.models import Customer
from myapp.models import Food,Member,OrderItem,Chef,Cart
from django.contrib.auth.hashers import make_password
import requests

# Create your views here.

# Admin
def fromloginadmin(request):
    return render(request, "Ad_login.html")  

def loginadmin_from(request):
    return render(request,'Ad_login.html')

def mydashboard(request):
    members = User.objects.filter(is_superuser=False)
    return render(request,'mydashboard/dash_base.html',{'members':members})


# mydashboard edit
def mydashboard_edit(reqeust):
    return render(reqeust,'mydashboard/dash_base_edit.html')

# login 
def myadmin(request):
    
    return render(request,'mydashboard/dashboard.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, f"User with username '{username}' does not exist.")
            return redirect('admin-myadmintrator:login_admin_from')
        # Authenticate the user
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user is either an admin, an owner, or a chef
            if user.is_superuser or user.groups.filter(name='Owner').exists():
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('admin-myadmintrator:mydashboard')
            elif user.groups.filter(name='Chef').exists():
                # Allow chefs to access the dashboard
                login(request, user)
                messages.success(request, 'chef Login successful.')
                return redirect('admin-myadmintrator:mychef')
            else:
                messages.warning(request, "You are not authorized to access this page.")
                return redirect('admin-myadmintrator:login_admin_from')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect('admin-myadmintrator:login_admin_from')
    return render(request, 'owner_login.html')

    
def adminlogout(request):
    logout(request)
    messages.success(request,'Your logout in .!!')
    return redirect('/')

# management chef restuarant
def fromloginchef(request):
    return render(request,'chef_login.html') # แสดงข้อความต้อนรับหลังจาก login สำเร็จ

# member 
def member(request):
    members = User.objects.filter(is_superuser=False)
    return render(request,'member.html',
                  {'members':members})

def from_member(request):
    return render(request,'member_edit.html')


def edit_member(request, id):
    # Get the user object to edit
    user = User.objects.get(pk=id)  # Assuming your user model is named 'User', please replace it with your actual user model
    
    if request.method == 'POST':
        # Update user attributes based on form data
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            user.profile_picture = profile_picture

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('myadmintrator:edit_member', id=id)  # Redirect to profile page after successful update
    else:
        return render(request, 'member_edit.html', {'user': user})


def delete(request, id):
    members = User.objects.get(pk=id)
    members.delete()
    members = User.objects.filter(is_superuser=False)
    print('display members after no delete : ',members)
    return render(request,'member.html',{
        'members':members,
    })

def form_product(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            price = float(request.POST['price'])  # แปลงค่าราคาเป็น float
            image = request.FILES.get('image')
            
            # สร้างอาหารใหม่
            new_food = Food(title=title, price=price, image=image)
            new_food.save()
            
            return redirect('myadmintrator:product')
        except Exception as e:
            # จัดการข้อผิดพลาดในการสร้างอาหารใหม่
            error_message = "An error occurred while adding the new food item. Please try again."
            return render(request, 'add_product.html', {'error_message': error_message})
    else:
        all_foods = Food.objects.all()
        return render(request, 'product_.html', {'all_foods': all_foods})
 
# Order 
def Order(request):
      # Query to get all orders
    orders = OrderItem.objects.all()
    return render(request, 'Order.html', {
                                          'orders':orders})

 #Product Foods
def product_(request):
    all_foods = Food.objects.all()
    return render(request, 'product_.html', {'all_foods': all_foods})

def product_add(request):
    all_foods = Food.objects.all()
    return render(request, 'add_product.html', {'all_foods': all_foods})


    
    
 #Delate product
def delate_product(reqeust,id):
    try:
        product_obj = Food.objects.get(pk=id)
        product_obj.delete()
        print('Delete scessfully !!')
    except:
        messages.error('not Delete product')
    # Redirect to product listing page
    return redirect('admin-myadmintrator:product')


# from link url  product 
def from_edit_product(request):
    product = Food.objects.all()
    return render(request, 'edit_product.html',{'product':product})


# Edit product 
def edit_product(request, id): 
    product = Food.objects.get(pk=id)  # Get the product by ID
    if request.method == 'POST':
        title = request.POST['title']
        image = request.FILES.get('image')
        popularity = request.POST['popularity']
        status = request.POST['status']
        
        # Update product fields
        product.title = title
        product.popularity = popularity 
        product.status = status

        if image:
            product.image = image
        product.popularity = popularity 
        product.status = status 

        
        # Save the updated product
        product.save()
        
        return redirect('myadmintrator:product')  # Redirect to product listing page
    else:
        return render(request, 'edit_product.html', {'product': product})



def mydashboard_chef(request):
    return render(request, 'mydashboard/mychef.html',)




