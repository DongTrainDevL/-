from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils.html import format_html
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your models here.

# list user member
class Member(models.Model):
    # id == PK
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()

    # return admin.py
    def __str__(self):
        return f"filed {self.first_name}"
    

# models.py

class UserProfile:
    def __init__(self, user_id, first_name, last_name, email, profile_picture=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.profile_picture = profile_picture

    def update_profile(self, first_name=None, last_name=None, email=None, profile_picture=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        if profile_picture:
            self.profile_picture = profile_picture

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# cart 
class Customer(models.Model):
      user = models.OneToOneField(User,on_delete=models.CASCADE)
      name = models.CharField(max_length=250)
      email = models.CharField(max_length=250, null=True)

      def __str__(self):
          return self.name

class Food(models.Model):
      title = models.CharField(max_length=100)
      price = models.FloatField()
      status_food = models.BooleanField(default=False, null=True,blank=False)
      image = models.ImageField(upload_to='image')
      popularity = models.IntegerField(default=0)
      status = models.CharField(max_length=10, default='normal')  # เพิ่มฟิลด์สถานะสินค้า


      def __str__(self):
        return f'{self.title}'
      
      def show_image(self):
         return format_html('<img src="' + self.images.url +'" height="40px" >')
      show_image.allow_tag = True
      
      
      
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'name : {self.user}'

      
class Order(models.Model):
    
    #date_oreded = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(auto_now_add=True)  # เพิ่มแอตทริบิวต์ date_ordered ในโมเดล Order
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=250, null=True)
    #quantity = models.IntegerField(default=0 ,null=True, blank=True)
    #food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # เพิ่มฟิลด์สถานะของคำสั่ง
    STATUS_CHOICES = [
        ('cooking', 'Cooking'),
        ('success', 'Success'),
        ('finished', 'Finished'),
        ('out', 'Out (Cancel)'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cooking')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # เพิ่มฟิลด์ total_price

    

    def __str__(self):
        return f"Order ID: {self.id}, User: {self.user.username}, Date Ordered: {self.date_ordered}"
    
      
class OrderItem(models.Model):
     food = models.ForeignKey(Food, on_delete=models.CASCADE)
     order = models.ForeignKey(Order ,on_delete=models.CASCADE)
     
     # ForeignKey 
     quantity = models.IntegerField(default=0 ,null=True, blank=True)
     date_added = models.DateTimeField(auto_now_add=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     status = models.CharField(max_length=10, default='success')  # เพิ่มฟิลด์สถานะอาหาร
     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # เพิ่มฟิลด์ total_price

     def save(self, *args, **kwargs):
        self.total_price = self.food.price * self.quantity  # คำนวณ total_price จากราคาของอาหาร * จำนวน
        super().save(*args, **kwargs)
     
     
     



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.food.name} in cart of {self.cart.user.username}"

class Chef(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.username
