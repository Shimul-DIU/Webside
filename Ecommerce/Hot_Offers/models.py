from django.db import models

# Create your models here.
class demo(models.Model):
    customerid=models.IntegerField()
    customerName=models.CharField(max_length=20)
    location=models.CharField(max_length=13)
    phone=models.IntegerField()