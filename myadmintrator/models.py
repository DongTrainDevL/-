from django.db import models
from myapp.models import Order,OrderItem,Chef,Food

# Create your models here.
from django.contrib.auth.models import User

# model customer 
class Customer(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    image = models.ImageField(upload_to='image')
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'Name : {self.name}'
    



