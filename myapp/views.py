from urllib import request
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from django.http import HttpResponseBadRequest, HttpResponseServerError,HttpResponseNotAllowed,JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login  # import form
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import *
from django.contrib.sessions.models import Session
# import to confirm order
from django.views.decorators.http import require_POST
import json
# get data models apps 
import models
from myadmintrator.models import Customer
# update
from django.template import loader
# import models
from .models import Food,Customer,OrderItem,Cart,CartItem,Order
from .forms import CartForm
import requests
from django.urls import reverse_lazy
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
import pandas as pd
from django.db.models import Sum
#chart 
from datetime import datetime, timedelta
from .utils import calculate_total_revenue


## index
def home(request):
    foods = Food.objects.all()
    orders = Order.objects.all()
    cart_items_count = get_cart_items_count(request)
    return render(request, "home.html",
                  {'foods':foods,
                   'cart_items_count':cart_items_count,
                   'orders':orders})

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "account/login.html")

# Register 
def register(request):
    if request.method == "POST":
        # POST
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        #image = request.FILES.get('image')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "user ใช้ไปแล้ว")
                return redirect("from_register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email ใช้ไปแล้ว")
                return redirect("from_register")
            else:
                myuser = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )
                myuser.save()
            messages.success(request, "Your Accout has been sucessfuly created.")

            return HttpResponseRedirect(reverse("home"))
        else:
            messages.success(request, "Password ไม่ถูกต้อง")
            return render(request, "account/register.html",
                          {'myuser':myuser})
    return render(request, "account/register.html")

def from_register(request):
    return render(request,'account/register.html')

# User login 
def userlogin(request):
    if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       try:
          user = User.objects.get(username=username)
       except:
          messages.warning(request,f"User with { username } does not exits !!")

       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
          auth.login(request, user)
          messages.success(request,'Your are login ')
          return redirect('index')
       else:
          messages.warning(request,f"User  does not exits create account !!")
          return redirect("login")      
    return render(request,'account/login.html')

def logout(request):
    auth.logout(request)
    messages.warning(request,f"Your are logout in. !!")
    return redirect("/")






#test profile 
@login_required
def profile_Edit(request):
    if request.method == 'POST':
        user = request.user
        # Update user attributes based on form data
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            user.profile_picture = profile_picture

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('home')  # Redirect to profile page after successful update
    else:
        return render(request,'account/settings.html')


def update_user(reqeust):
    return render(reqeust,'account/setting_up.html')

def food(reqeust):
    return render(reqeust,'foods/food.html')

# help
def help(request):
    return render(request, "help.html")

# Add to cart 
def add_to_cart(request, food_id):
    if not request.user.is_authenticated:
        return redirect('login')
    food = get_object_or_404(Food, pk=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    try:
        cart_item = CartItem.objects.get(cart=cart, food=food)
        cart_item.quantity += quantity
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, food=food, quantity=quantity, user=request.user)
    return redirect('cart_list')
        
# remove items in cart 
def remove_from_cart(request, food_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        food = Food.objects.get(id=food_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, food=food)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        
    except (Food.DoesNotExist, Cart.DoesNotExist, CartItem.DoesNotExist):
        pass
    return redirect('cart_list')

def cart_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_change = int(request.POST.get('quantity_change'))
        cart_item = get_object_or_404(CartItem, cart=cart, food_id=product_id)
        cart_item.quantity += quantity_change
        cart_item.save()

    total_price = sum(item.food.price * item.quantity for item in cart_items)
    cart_items_count = cart_items.count()
    return render(request, 'cart/cart_item.html', {'cart_items': cart_items, 'total_price': total_price, 'cart_items_count': cart_items_count})

def send_line_notify(message):
    line_token = "GhLHKYYGT3spWMTo4hqEZvNS0uQT13BCHXtUZEVnYTm"
    line_url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + line_token}
    data = {'message': message}
    requests.post(line_url, headers=headers, data=data)

def payment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.food.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        cart.cartitem_set.all().delete()
        messages.success(request,'Payment complate!!')
        return redirect('home')
    cart_items_count = get_cart_items_count(request)
    return render(request, 'payment/pay.html', {'cart_items': cart_items, 'total_price': total_price,
                                             'cart_items_count':cart_items_count})

def confirm_order(request):
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        order = Order.objects.create(user=request.user)
        order_details = ""
        total_price = 0
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(order=order, food=cart_item.food, quantity=cart_item.quantity, user=request.user)
            order_item.total_price = cart_item.food.price * cart_item.quantity
            order_item.save()  # อัปเดต total_price
            order_details += f"{cart_item.food.title} - จำนวน: {cart_item.quantity} - ราคาต่อหน่วย: {cart_item.food.price} บาท\n"
            total_price += order_item.total_price

        cart.cartitem_set.all().delete()
        message = "รายการอาหารที่คุณสั่ง:\n"

        for cart_item in cart_items:
            message += f"ชื่อ: {cart_item.food.title} จำนวน: {cart_item.quantity} ( {cart_item.total_price} ) \n  "
        line_notify_token = "GhLHKYYGT3spWMTo4hqEZvNS0uQT13BCHXtUZEVnYTm"
        line_notify_api = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": "Bearer " + line_notify_token}
        message = f"รายละเอียดการสั่งซื้อ:\nราคารวมทั้งหมด: {total_price} บาท"
        payload = {"message": message}
        response = requests.post(line_notify_api, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, 'Order successfully confirmed!')
            return redirect('home')
        else:
            error_message = "Failed to confirm order. Please try again later."
            return render(request, 'foods/confirm_order.html', {'error_message': error_message})
    else:
        return render(request, 'foods/confirm_order.html', {})

def get_cart_items_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = sum(item.quantity for item in cart.cartitem_set.all())
        return cart_items_count
    return 0

@login_required
def your_order(request):
    try:
        latest_order = Order.objects.filter(user=request.user).latest('date_ordered')
        if latest_order.complete:
            return render(request, 'Order/your_order.html')
        return render(request, 'Order/your_order.html', {'latest_order': latest_order})
    except ObjectDoesNotExist:
        return render(request, 'Order/your_order.html')  


def order_detail(request):
    if not request.user.is_authenticated:
        return redirect("login")
    latest_order = Order.objects.filter(user=request.user).latest('date_ordered')
    order_items = OrderItem.objects.filter(order=latest_order)
    return render(request, 'Order/order_detial.html', {'latest_order': latest_order, 'order_items': order_items})
    
    
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.warning(request, 'Order does not exist.')
        return redirect('order_detail')
    order.complete = True
    order.save()
    order.delete()
    message = f"Order ID: {order_id} has been cancelled."
    send_line_notify(message)
    messages.success(request, 'Order has been cancelled successfully.')
    return redirect('order_detail')
    

#chef
def your_order_for_chef(request):
    if request.user.groups.filter(name='Chef').exists():
        latest_order = Order.objects.filter(status='cooking').latest('date_ordered')
        return render(request, 'chef/your_order_for_chef.html', {'latest_order': latest_order})
    else:
        latest_order = Order.objects.filter(user=request.user).latest('date_ordered')
        return render(request, 'Order/your_order.html', {'latest_order': latest_order})

def confrim_status_order(request):
    return render(request,'chef/confrim_status_order.html')

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['success', 'cancel']:
            order.status = new_status
            order.save()

            if new_status == 'success':
                order.complete = True
                order.save()
                messages.success(request, f"Order {order_id} has been marked as 'Success'.")
                return redirect(reverse_lazy('home'))
            else:
                messages.info(request, f"Order {order_id} is now {new_status}.")
                return redirect(reverse_lazy('order_detail_chef', kwargs={'order_id': order_id}))
        elif new_status in ['finished', 'cooking']:
            order.status = new_status
            order.save()
            messages.info(request, f"Order {order_id} is now {new_status}.")
            return redirect(reverse_lazy('order_detail_chef', kwargs={'order_id': order_id}))
        else:
            messages.error(request, "Invalid status.")
            return redirect(reverse_lazy('your_order_for_chef'))


    elif request.method == 'GET' and request.GET.get('status') == 'success':
        order.status = 'success'
        order.save()
        order.complete = True
        order.save()

        messages.success(request, f"Order {order_id} has been marked as 'Success'.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Invalid request method.")
        return redirect(reverse_lazy('your_order_for_chef'))
    
def order_detail_for_chef(request, order_id):
    latest_order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=latest_order)
    status_param = request.GET.get('status')
    if status_param == 'success':
        latest_order.status = 'success'
        latest_order.save()
        messages.success(request, f"Order {order_id} has been updated to 'Success'.")
        return redirect(reverse_lazy('order_detail_chef', kwargs={'order_id': order_id}))
    return render(request, 'chef/order_detail_for_chef.html', {'latest_order': latest_order, 'order_items': order_items})
    
def from_order_detail_for_chef(request):
    if not request.user.is_authenticated:
        return redirect("login")
    latest_order = Order.objects.filter(status='cooking').latest('date_ordered')
    order_items = OrderItem.objects.filter(order=latest_order)
    return render(request, 'chef/order_detail_for_chef.html', {'latest_order': latest_order, 'order_items': order_items})

def from_order_detail_for_check_status_order(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if Order.objects.filter(status='cooking').exists():
        latest_order = Order.objects.filter(status='cooking').latest('date_ordered')
        order_items = OrderItem.objects.filter(order=latest_order)
        return render(request, 'chef/check_order_status.html', {'latest_order': latest_order, 'order_items': order_items})
    else:
        messages.info(request, "No orders are currently being cooked.")
        return redirect(reverse_lazy('home'))

def order_management(request):
    orders = Order.objects.filter(status__in=['cooking', 'finished'])
    return render(request, 'chef/order_management.html', {'orders': orders})

def from_plotgrap(request):
    today = datetime.now()
    start_date = today - timedelta(days=30) 
    orders = OrderItem.objects.filter(order__date_ordered__gte=start_date)
    daily_sales_data = {}
    for order_item in orders:
        order_date = order_item.order.date_ordered.strftime('%Y-%m-%d')
        daily_sales_data[order_date] = daily_sales_data.get(order_date, 0) + order_item.total_price
    sorted_daily_sales = sorted(daily_sales_data.items())
    total_revenue_monthly = sum(order_item.total_price for order_item in orders)
    food_revenue = OrderItem.objects.values('food__title').annotate(total_revenue=Sum('total_price'))

    context = {
        'daily_sales': sorted_daily_sales,
        'total_revenue_monthly': total_revenue_monthly,
        'food_revenue': food_revenue,
    }
    return render(request, 'plotgrap.html', context)

def calculate_revenue(request):
    list_data_food_id = []
    total_revenue = calculate_total_revenue()
    context = {
        'total_revenue': total_revenue,
        'list_data_food_id':list_data_food_id,
    }
    return render(request, 'total_revenue.html', context)

