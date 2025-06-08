from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
class account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=25)
    phone = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    email = models.EmailField(unique=True)
    aadhar = models.DecimalField(max_digits=12, decimal_places= 0,unique=True)
    acc_num = models.BigAutoField(primary_key=True)
    pin = models.CharField(max_length=6, default="000000")
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    address = models.TextField()
    
    def __str__(self):
        return self.name
    
