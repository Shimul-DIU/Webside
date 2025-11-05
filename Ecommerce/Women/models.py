
    
from django.db import models
# Create your models here.
class Women_info(models.Model):
    orderNumber=models.IntegerField()
    personName=models.CharField(max_length=40)
    phoneNumber=models.IntegerField()
    address=models.CharField(max_length=60)
    productName=models.CharField(max_length=40)

    def __str__(self):
        return f"{self.orderNumber}-{self.personName}-{self.phoneNumber}-{self.address}-{self.productName}"