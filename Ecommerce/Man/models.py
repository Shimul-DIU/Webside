from django.db import models

# Create your models here.
class Man_info(models.Model):
    orderNumber=models.IntegerField()
    personName=models.CharField(max_length=40)
    phoneNumber=models.IntegerField()
    address=models.CharField(max_length=60)
    productName=models.CharField(max_length=40)