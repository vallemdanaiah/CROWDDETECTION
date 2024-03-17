from django.db import models
#from datetime import datetime
#from django.utils import timezone
import datetime

# Create your models here.

class UserRegisterModel(models.Model):
    id = models.AutoField(primary_key=True)
    email =models.CharField(max_length=100)
    password =models.CharField(max_length=100)
    username =models.CharField(max_length=100)
    mobile =models.CharField(max_length=100)
    dob =models.DateField()
    gender =models.CharField(max_length=100)
    address =models.CharField(max_length=100)
    status =models.CharField(max_length=100)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "registrations"

class uploadvideo(models.Model):
    video=models.FileField(blank=False,null=False)