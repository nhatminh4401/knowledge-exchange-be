from django.db import models

# Create your models here.

class User(models.Model):
    User_ID = models.AutoField(primary_key=True)
    User_Name = models.CharField(max_length=50)
    User_Email = models.CharField(max_length=50)
    User_Password = models.CharField(max_length=50)
    User_Phone = models.CharField(max_length=50)
    User_Address = models.CharField(max_length=50)
    User_Created_Date = models.CharField(max_length=50)
    User_Updated_Date = models.CharField(max_length=50)
