from django.db import models

# Create your models here.
class Productinfo(models.Model):
    name=models.CharField(max_length=20)
    phone=models.IntegerField()
    address=models.CharField(max_length=55)
    quantity=models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.quantity}"