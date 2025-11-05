from django.db import models

# Create your models here.
class  Oderinfo(models.Model):
    name=models.CharField(max_length=20)
    phone=models.CharField(max_length=15)
    payment=models.CharField(max_length=10)
    address=models.CharField(max_length=55)
    quantity=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.phone}{self.payment} - {self.address} - {self.quantity}"