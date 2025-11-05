from django.db import models

# Create your models here.
class Bloginfo(models.Model):
    date=models.DateField()
    location=models.CharField(max_length=40)
    vehicle=models.CharField(max_length=40)
    friends=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.date}-{self.location}-{self.vehicle}-{self.friends}"